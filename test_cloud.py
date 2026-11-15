# test_cloud.py
import os, uuid, io, requests
import cloudinary, cloudinary.uploader, cloudinary.utils
from dotenv import load_dotenv

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

def upload(data: bytes, ext: str):
    base = uuid.uuid4().hex
    new_filename = f"{base}.{ext}"
    stream = io.BytesIO(data)
    if ext in IMAGE_EXTS:
        cloudinary.uploader.upload(stream, public_id=base,
            resource_type='image', type='upload')
    else:
        cloudinary.uploader.upload(stream, public_id=new_filename,
            resource_type='raw', type='upload')
    return new_filename

def signed_file_url(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

    if ext in IMAGE_EXTS:
        base = filename.rsplit('.', 1)[0]

        # BAGONG format: public_id walang extension
        new_url, _ = cloudinary.utils.cloudinary_url(
            base, resource_type='image', type='upload',
            format=ext, sign_url=True, secure=True)

        # LUMANG format: public_id may extension (uuid.png)
        old_url, _ = cloudinary.utils.cloudinary_url(
            filename, resource_type='image', type='upload',
            format=ext, sign_url=True, secure=True)

        for candidate in (new_url, old_url):
            try:
                r = requests.head(candidate, timeout=5, allow_redirects=True)
                if r.status_code == 200:
                    return candidate
            except Exception:
                pass
        return new_url   # kung wala talagang nahanap

    url, _ = cloudinary.utils.cloudinary_url(
        filename, resource_type='raw', type='upload',
        sign_url=True, secure=True)
    return url

def check(label, filename):
    url = signed_file_url(filename)
    r = requests.get(url, timeout=20)
    print(f"{label}: {r.status_code} {r.headers.get('content-type')}")
    print(f"   {url}")
    if r.status_code != 200:
        print("   x-cld-error:", r.headers.get('x-cld-error'))

# 1x1 PNG
PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d49444154789c6360f8cfc0f01f0005000201a52f6f8b0000000049454e44ae426082")
# minimal PDF
PDF = (b"%PDF-1.1\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
       b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
       b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
       b"trailer<</Root 1 0 R>>\n%%EOF")

check("PNG", upload(PNG, 'png'))
check("PDF", upload(PDF, 'pdf'))