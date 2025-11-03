from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mkv'}

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
    try:
        # List resources from Cloudinary
        result = cloudinary.api.resources(type='upload', max_results=500)
        files = []
        if 'resources' in result:
            # Sort by created_at, most recent first
            files = sorted([resource['public_id'] + '.' + resource['format'] for resource in result['resources']],
                         key=lambda x: next((r['created_at'] for r in result['resources'] if r['public_id'] + '.' + r['format'] == x), ''), reverse=True)
    except Exception as e:
        flash(f'Error loading files: {str(e)} ❌')
        files = []
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file uploads to Cloudinary"""
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
            # Generate unique public_id to prevent overwriting
            name, ext = os.path.splitext(secure_filename(file.filename))
            unique_public_id = f"{uuid.uuid4().hex}_{name}"
            try:
                # Upload to Cloudinary
                result = cloudinary.uploader.upload(file, public_id=unique_public_id, resource_type='auto')
                uploaded_count += 1
            except Exception as e:
                flash(f'Upload failed: {str(e)} ❌')
                return redirect(url_for('index'))

    if uploaded_count > 0:
        flash(f'{uploaded_count} file(s) uploaded successfully 💖')
    else:
        flash('No valid files uploaded ❌')
    return redirect(url_for('index'))


@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    """Delete selected file from Cloudinary"""
    try:
        # Extract public_id from filename (remove extension)
        public_id = filename.rsplit('.', 1)[0]
        result = cloudinary.uploader.destroy(public_id)
        if result.get('result') == 'ok':
            flash(f'{filename} deleted successfully 🗑️')
        else:
            flash(f'Failed to delete {filename} ❌')
    except Exception as e:
        flash(f'Delete failed: {str(e)} ❌')
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


@app.route('/debug')
@login_required
def debug():
    """Debug endpoint to check environment variables"""
    debug_info = {
        'CLOUDINARY_CLOUD_NAME': 'Set' if os.getenv('CLOUDINARY_CLOUD_NAME') else 'Missing',
        'CLOUDINARY_API_KEY': 'Set' if os.getenv('CLOUDINARY_API_KEY') else 'Missing',
        'CLOUDINARY_API_SECRET': 'Set' if os.getenv('CLOUDINARY_API_SECRET') else 'Missing',
        'USERNAME': 'Set' if os.getenv('USERNAME') else 'Missing',
        'PASSWORD': 'Set' if os.getenv('PASSWORD') else 'Missing',
        'SECRET_KEY': 'Set' if os.getenv('SECRET_KEY') else 'Missing'
    }
    return jsonify(debug_info)


# Vercel deployment
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
