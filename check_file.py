import os, sys, requests
import cloudinary, cloudinary.api, cloudinary.utils
from dotenv import load_dotenv

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

fn = sys.argv[1]                      # hal. abcd1234.jpg
base, ext = fn.rsplit('.', 1)

print("--- Admin API lookup (image) ---")
for pid in (base, fn):
    try:
        r = cloudinary.api.resource(pid, resource_type='image')
        print("FOUND    ", pid, r.get('format'), r.get('bytes'))
    except Exception as e:
        print("NOT FOUND", pid, "|", e)

print("--- Admin API lookup (raw) ---")
try:
    r = cloudinary.api.resource(fn, resource_type='raw')
    print("FOUND    ", fn)
except Exception as e:
    print("NOT FOUND", fn, "|", e)

print("--- Signed URL test ---")
url, _ = cloudinary.utils.cloudinary_url(
    base, resource_type='image', type='upload',
    format=ext, sign_url=True, secure=True)
r = requests.get(url, timeout=20)
print(r.status_code, r.headers.get('x-cld-error'))
print(url)