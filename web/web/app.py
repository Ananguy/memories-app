from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

# Folder for uploaded files
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mkv'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Password configuration from environment variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

if not USERNAME or not PASSWORD:
    raise ValueError("USERNAME and PASSWORD must be set in environment variables")

PASSWORD_HASH = generate_password_hash(PASSWORD)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@login_required
def index():
    """Show upload form + gallery"""
    files = sorted(os.listdir(app.config['UPLOAD_FOLDER']), key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file uploads"""
    if 'file' not in request.files:
        flash('No file part in the form ❌')
        return redirect(url_for('index'))

    files = request.files.getlist('file')

    if not files or all(file.filename == '' for file in files):
        flash('No file selected ⚠️')
        return redirect(url_for('index'))

    uploaded_count = 0
    for file in files:
        if file and allowed_file(file.filename):
            # Generate unique filename to prevent overwriting
            name, ext = os.path.splitext(secure_filename(file.filename))
            unique_filename = f"{uuid.uuid4().hex}_{name}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(save_path)
            uploaded_count += 1

    if uploaded_count > 0:
        flash(f'{uploaded_count} file(s) uploaded successfully 💖')
    else:
        flash('No valid files uploaded ❌')
    return redirect(url_for('index'))


@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    """Delete selected file"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'{filename} deleted successfully 🗑️')
    else:
        flash('File not found ❌')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session['logged_in'] = True
            flash('Login successful! 💖')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password ❌')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Handle logout"""
    session.pop('logged_in', None)
    flash('Logged out successfully 👋')
    return redirect(url_for('login'))


# Vercel deployment
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
