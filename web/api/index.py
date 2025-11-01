import os
import sys

# Set default environment variables for Vercel if not set
os.environ.setdefault('USERNAME', 'ananb')
os.environ.setdefault('PASSWORD', 'MICKKY')
os.environ.setdefault('SECRET_KEY', 'fallback_secret_key_for_vercel')

# Import the Flask app from app.py
from app import app

# Vercel expects the Flask app to be named 'app'
# This file serves as the entry point for Vercel serverless functions

def handler(event, context):
    """
    Vercel serverless function handler for Flask app.
    Converts Vercel event format to WSGI environ and back.
    """
    # Convert Vercel event to WSGI environ manually
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'SCRIPT_NAME': '',
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', {}) and '&'.join([f"{k}={v}" for k, v in event.get('queryStringParameters', {}).items()]) or '',
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': str(len(event.get('body', ''))),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '443',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': event.get('body', ''),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    # Add headers to environ
    for header_name, header_value in event.get('headers', {}).items():
        environ[f'HTTP_{header_name.upper().replace("-", "_")}'] = header_value

    # Handle the request
    response_data = {}

    def start_response(status, headers, exc_info=None):
        response_data['status'] = status
        response_data['headers'] = headers

    # Call the Flask app
    response_body = app(environ, start_response)

    # Convert response to Vercel format
    status_code = int(response_data['status'].split()[0])
    headers = dict(response_data['headers'])

    # Handle response body
    if isinstance(response_body, list):
        body = b''.join(response_body).decode('utf-8')
    else:
        body = response_body

    return {
        'statusCode': status_code,
        'headers': headers,
        'body': body
    }
