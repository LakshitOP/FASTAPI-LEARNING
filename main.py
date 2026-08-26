import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from imagekitio import ImageKit
from imgbb_sdk import imgbb_upload, ImgBBError
load_dotenv()

app = FastAPI()
IMGBB_API_KEY = str(os.getenv("IMGBB_API_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = ImageKit(
    private_key=os.environ.get("IMAGEKIT_PRIVATE_KEY"),
)
# url_endpoint=os.environ.get("IMAGEKIT_URL_ENDPOINT")

a = []


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
        # Read file contents
        contents = await file.read()
        
        # Upload to ImgBB
        response = imgbb_upload(
            key=IMGBB_API_KEY,
            image=contents,
            name=str(file.filename)
        )

        a.append({
            "Original Name": str(file.filename),
            "File URL": response["data"]["url"],
        })
        
        return {
            "success": True,
            "url": response["data"]["url"],
            "delete_url": response["data"]["delete_url"],
            "width": response["data"]["width"],
            "height": response["data"]["height"]
        }


@app.get("/files")
async def get_files():
    return {"files": a}