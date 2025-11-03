from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import uuid
import boto3
from botocore.exceptions import NoCredentialsError
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

# AWS S3 Configuration
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_REGION = os.getenv('S3_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=S3_REGION
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
        # List objects in S3 bucket
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        files = []
        if 'Contents' in response:
            # Sort by last modified, most recent first
            files = sorted([obj['Key'] for obj in response['Contents']], key=lambda x: response['Contents'][[obj['Key'] for obj in response['Contents']].index(x)]['LastModified'], reverse=True)
    except NoCredentialsError:
        flash('AWS credentials not available ❌')
        files = []
    except Exception as e:
        flash(f'Error loading files: {str(e)} ❌')
        files = []
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file uploads to S3"""
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
            try:
                # Upload to S3
                s3_client.upload_fileobj(file, S3_BUCKET, unique_filename)
                uploaded_count += 1
            except NoCredentialsError:
                flash('AWS credentials not available ❌')
                return redirect(url_for('index'))
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
    """Delete selected file from S3"""
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=filename)
        flash(f'{filename} deleted successfully 🗑️')
    except NoCredentialsError:
        flash('AWS credentials not available ❌')
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


# Vercel deployment
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
