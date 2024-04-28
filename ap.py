from flask import Flask, render_template, request, redirect, url_for, session,g,  flash ,Response,jsonify
# from werkzeug.security import generate_password_hash
import sqlite3
import redis
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from landmark_detection import *
from generate_frame import *
import redis
app = Flask(__name__)
app.secret_key = '123345'
redis_client = redis.Redis(host='localhost', port=6000, db=0)
DATABASE = 'dbtest.db'
# 创建一个装饰器来检查用户是否登录
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to view this page.', 'error')
            return redirect(url_for('home'))  # 或者重定向到登录页面
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This line is crucial
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    # cursor.execute('DROP TABLE IF EXISTS users')
    # cursor.execute('DROP TABLE IF EXISTS video_status')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS video_status(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_name VARCHAR(255) NOT NULL,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users (id))
                   ''')
    db.commit()
    db.close()
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/video_page')
@login_required
def video_page():
    return render_template('videos.html')

@app.route('/video_detail')
@login_required
def video_detail():
    return render_template('video-detail.html')
    
@app.route('/profile')
@login_required

def profile():
    user_id = session.get('user_id')
    if user_id is None:
        flash("You need to be logged in to view this page.", "error")
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()
    user = cursor.execute('SELECT username, email FROM users WHERE id = ?', (user_id  ,)).fetchone()
    videos = cursor.execute('SELECT video_name, status FROM video_status WHERE user_id = ?', (user_id,)).fetchall()
    db.close()
    if user:
        return render_template('profile.html', user=user ,video_status= videos)
    else:
        flash("User not found.", "error")
    return render_template('profile.html')
@app.route('/demo')
def test():
    return render_template('detection-page.html')
@app.route('/detect')
@login_required
def detect():
    video_title = request.args.get('title', 'Default Title')  # 如果没有提供标题，使用默认标题

    return render_template('Detection.html', title=video_title)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        username_or_email = request.form['username']
        password = request.form['password']
        
        user = cursor.execute('SELECT * FROM users WHERE username = ? OR email =?', (username_or_email,username_or_email)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']  # Log in the user
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')
        
        db.close()

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db = get_db()
            cursor = db.cursor()
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']  # Get the confirm password data
            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return redirect(url_for('register'))
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
            user_id = cursor.lastrowid #获取新用户的 ID
            initialize_video_status(user_id, cursor)  # 初始化视频状态
            db.commit() 
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            error_info = str(e)
            if 'UNIQUE constraint failed: users.username' in error_info:
                flash('This username is already taken. Please choose another one.', 'error')
            elif 'UNIQUE constraint failed: users.email' in error_info:
                flash('This email is already registered. Please use another email.', 'error')
            else:
                flash('An unexpected error occurred. Please try again.', 'error')
            return redirect(url_for('register'))
        finally:
            if db:
                db.close()
    return render_template('index.html')
def initialize_video_status(user_id, cursor):
    default_status = "Pending"
    video_ids = os.listdir(DATA_PATH) # 根据实际情况调整
    for video_id in video_ids:
        cursor.execute('INSERT INTO video_status (video_name, user_id ,status) VALUES (?, ?, ?)', (video_id,user_id, default_status))

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # 移除session中的用户ID
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/detection')
def video():
    # camera_type = request.args.get('camera_type', 'webcam')
    return Response(generate_frames(redis_client), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_results')
@login_required
def get_results():
    video_title = request.args.get('title', 'Default Title')
    latest_result = redis_client.get('latest_result')
    confidence = redis_client.get('confidence')
    if confidence:
        confidence = float(confidence.decode('utf-8'))
    
    if latest_result is not None:
        latest_result = latest_result.decode('utf-8')
        
        if latest_result == video_title:
            db = get_db()
            cursor = db.cursor()
            # try:
                # 更新数据库状态为'Completed'
            cursor.execute("UPDATE video_status SET status='Completed' WHERE video_name=? AND user_id=?", (video_title, session['user_id']))
            db.commit()
            return jsonify({'result': latest_result, 'confidence':confidence, 'message': 'Detection successful and status updated!', 'status': 'success'})
            db.close()
        else:
        #     # 如果结果不匹配，返回失败状态
            return jsonify({'result': latest_result, 'confidence': confidence})
    else:
        # 如果没有结果可用
        return jsonify({'result': '','confidence': confidence})
@app.route('/get_resultsdemo')
def get_result():
    latest_results = redis_client.get('joinlatest_result')
    print("Sending latest result to frontend:", latest_results)  # 添加打印语句以确认
    return jsonify({'result': latest_results.decode('utf-8')})

@app.route('/reset_result')
def reset_result():
    redis_client.set('latest_result', '')  # 设置回初始值
    redis_client.set('joinlatest_result', '')  # 设置回初始值
    return jsonify({'status': 'success', 'message': 'Result has been reset to initial state.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)
