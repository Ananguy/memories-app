# Our Memories Forever 💖

A beautiful, romantic photo and video gallery web application built with Flask. Perfect for storing and sharing precious memories with your loved one.

## Features

- 🔐 **Secure Authentication**: Password-protected access with environment variables
- 📸 **Photo & Video Upload**: Support for images (PNG, JPG, JPEG, GIF) and videos (MP4, MOV, AVI, MKV)
- 🎨 **Multiple Themes**: Light mode, dark mode, and romantic mode with floating hearts
- 🎵 **Background Music**: Romantic music playback in rom mode with volume controls
- 🖼️ **Lightbox Gallery**: Click to view full-size images and videos
- 📥 **Download Support**: Download media files directly from the gallery
- 🗑️ **File Management**: Delete unwanted files with confirmation
- 📱 **Responsive Design**: Works beautifully on desktop and mobile devices

## Setup

1. **Clone or download** the project files

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Edit `.env` with your desired credentials:
     ```
     USERNAME=LOVE
     PASSWORD=MICKKY
     SECRET_KEY=your_random_secret_key_here
     ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   - Open your browser and go to `http://localhost:5000`
   - Login with your configured username and password

## Deployment

### Environment Variables
Make sure to set these environment variables on your hosting platform:

- `USERNAME`: Your login username
- `PASSWORD`: Your login password
- `SECRET_KEY`: A random string for Flask session security

### File Permissions
Ensure the web server has write permissions to the `static/uploads/` directory for file uploads.

## Security Notes

- Change the default credentials in `.env`
- Use a strong, random `SECRET_KEY`
- The `.env` file is gitignored to prevent credential leaks
- Uploaded files are stored in `static/uploads/` - consider backup strategies

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with themes and animations
- **Security**: Werkzeug password hashing, Flask sessions
- **Environment**: python-dotenv for configuration

## Customization

- **Themes**: Modify colors in `static/css/style.css`
- **Music**: Replace `static/music/love-story.mp3` with your favorite song
- **Branding**: Update titles and messages in templates
- **File Types**: Add more extensions to `ALLOWED_EXTENSIONS` in `app.py`

## License

This project is created with ❤️ for personal use. Feel free to customize and share with your loved ones!

---

*Built with love for preserving beautiful memories* 💕
