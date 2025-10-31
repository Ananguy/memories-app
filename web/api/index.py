import os
# Set default environment variables for Vercel if not set
os.environ.setdefault('USERNAME', 'ananb')
os.environ.setdefault('PASSWORD', 'MICKKY')
os.environ.setdefault('SECRET_KEY', 'fallback_secret_key_for_vercel')

from flask import Flask
import app as flask_app

# Vercel expects the Flask app to be named 'app'
# This file serves as the entry point for Vercel serverless functions

app = flask_app.app

def handler(event, context):
    # Handle Vercel serverless function calls
    return app(event, context)
