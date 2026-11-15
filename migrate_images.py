import os
import cloudinary, cloudinary.api, cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
cursor = None
renamed = 0

while True:
    res = cloudinary.api.resources(
        resource_type='image', type='upload',
        max_results=500, next_cursor=cursor
    )
    for r in res['resources']:
        pid = r['public_id']
        ext = pid.rsplit('.', 1)[-1].lower() if '.' in pid else ''
        if ext in IMAGE_EXTS:
            new_pid = pid.rsplit('.', 1)[0]
            try:
                cloudinary.uploader.rename(pid, new_pid, resource_type='image')
                renamed += 1
                print(f"OK   {pid} -> {new_pid}")
            except Exception as e:
                print(f"FAIL {pid}: {e}")
    cursor = res.get('next_cursor')
    if not cursor:
        break

print(f"Tapos. Na-rename: {renamed}")