# CloudScale MLOps Pipeline - Ready-to-Run Repo (Skeleton)

## Overview
Minimal, reproducible skeleton of the CloudScale MLOps Pipeline project described in the deliverable. This repo contains a FastAPI service for file upload + metadata (S3 + MongoDB), an AWS Lambda handler example, an evaluation script for CLIP/FID, a GitLab CI example, and helper files.

**NOTE:** This is a lightweight skeleton meant to demonstrate architecture and reproducibility. Some evaluation dependencies (PyTorch, CLIP, pytorch-fid) are heavy and must be installed in an environment with GPU or sufficient CPU/RAM.

## Structure
```
.
├─ README.md
├─ .env.example
├─ requirements.txt
├─ Dockerfile
├─ .gitlab-ci.yml
├─ app/
│  └─ main.py
├─ lambda_handler.py
└─ eval/
   └─ eval_cli.py
```

## Quickstart (local)
1. Copy `.env.example` to `.env` and fill in values (S3_BUCKET, MONGO_URI, AWS credentials).
2. Create a Python virtualenv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the FastAPI app:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Upload a file:
   ```bash
   curl -F "file=@path/to/file.pdf" -F "description=demo" http://localhost:8000/upload
   ```
5. List files:
   ```bash
   curl http://localhost:8000/files
   ```

## Deploy
- Use the provided `.gitlab-ci.yml` as an example to build, test, and deploy containers.
- AWS Lambda: `lambda_handler.py` is a minimal example that writes event bodies to S3.

## Evaluation
- `eval/eval_cli.py` computes FID and CLIP similarity for two image folders. Install the heavy dependencies only when needed.

## Proof artifacts you can add
- `demo.mp4`, pipeline screenshots, S3 listings, MongoDB sample exports, SageMaker logs.

