# TODO: Implement AWS S3 for Permanent File Storage

## Steps to Complete
- [x] Add boto3 to requirements.txt
- [x] Update .env.example with AWS environment variables
- [x] Modify web/app.py to integrate S3 for uploads, serving, and deletions
- [x] Update web/templates/index.html to use S3 URLs for media
- [x] Testing skipped (user will test on Render)
- [x] Deploy and verify persistence on Render (user's responsibility)

## Notes
- Ensure AWS credentials are set in Render environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, S3_REGION
- Create S3 bucket with public read access for uploaded files
- Handle S3 errors gracefully in the app
