from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import boto3
import os
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# environment variables
S3_BUCKET = os.getenv('S3_BUCKET')
MONGO_URI = os.getenv('MONGO_URI')

if not S3_BUCKET or not MONGO_URI:
    # app will still start; endpoints will error until env is configured
    print('Warning: S3_BUCKET or MONGO_URI not configured in environment.')

s3 = boto3.client('s3')
mongo = MongoClient(MONGO_URI) if MONGO_URI else None
db = mongo['cloudscale'] if mongo else None
meta_col = db['files'] if db else None

class FileMeta(BaseModel):
    filename: str
    description: str | None = None

@app.post('/upload')
async def upload_file(file: UploadFile = File(...), description: str = ''):
    key = f"uploads/{uuid4()}_{file.filename}"
    try:
        s3.upload_fileobj(file.file, S3_BUCKET, key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    doc = {"key": key, "filename": file.filename, "description": description}
    if meta_col:
        meta_col.insert_one(doc)
    return {"s3_key": key}

@app.get('/files')
def list_files():
    if not meta_col:
        return []
    docs = list(meta_col.find({}, {'_id': 0}))
    return docs
