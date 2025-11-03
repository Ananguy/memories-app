import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.api

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def check_cloudinary_files():
    try:
        # Get all resources
        result = cloudinary.api.resources(type='upload', max_results=50)
        resources = result.get('resources', [])

        print(f"Total files in Cloudinary: {len(resources)}")

        # Show recent files (last 10)
        print("\nRecent files:")
        for resource in resources[:10]:
            print(f"  - {resource['public_id']}.{resource['format']} (uploaded: {resource['created_at']})")

        # Check for files that might be from your app (not samples)
        app_files = [r for r in resources if not r['public_id'].startswith(('cld-sample', 'samples/'))]
        print(f"\nFiles uploaded by your app: {len(app_files)}")
        for resource in app_files[:10]:
            print(f"  - {resource['public_id']}.{resource['format']} (uploaded: {resource['created_at']})")

        return resources
    except Exception as e:
        print(f"Error checking Cloudinary: {str(e)}")
        return []

if __name__ == "__main__":
    check_cloudinary_files()
