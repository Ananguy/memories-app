import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def test_cloudinary_connection():
    try:
        # Test API connection by listing resources
        result = cloudinary.api.resources(type='upload', max_results=10)
        print(f"Cloudinary connection successful!")
        print(f"Cloud Name: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
        print(f"Files in account: {len(result.get('resources', []))}")

        if 'resources' in result:
            for resource in result['resources'][:5]:  # Show first 5
                print(f"  - {resource['public_id']}.{resource['format']}")

        return True
    except Exception as e:
        print(f"Cloudinary connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_cloudinary_connection()
