# GCP Cloud Run Deployment Guide

## Prerequisites

1. **Google Cloud Account**: Sign up at https://cloud.google.com/
2. **GCP Project**: Create a new project in GCP Console
3. **gcloud CLI**: Install from https://cloud.google.com/sdk/docs/install

---

## Step 1: Install and Configure gcloud CLI

### Install gcloud (Windows)
Download and run the installer from:
https://cloud.google.com/sdk/docs/install

### Login and Set Project
```bash
# Login to GCP
gcloud auth login

# Set your project ID (replace with your project ID)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## Step 2: Build and Deploy to Cloud Run

### Option A: Deploy with One Command (Easiest)

From the `backend` directory:

```bash
cd backend

gcloud run deploy private-knowledge-qa-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_API_KEY \
  --set-env-vars MONGODB_URI=YOUR_MONGODB_URI \
  --set-env-vars CORS_ORIGINS=https://your-frontend-url.vercel.app
```

**Note**: Replace:
- `YOUR_GEMINI_API_KEY` with your actual Gemini API key
- `YOUR_MONGODB_URI` with your MongoDB Atlas connection string
- `https://your-frontend-url.vercel.app` with your actual frontend URL (after deploying frontend)

### Option B: Build Docker Image Manually

```bash
cd backend

# Build the image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/private-knowledge-qa-backend

# Deploy to Cloud Run
gcloud run deploy private-knowledge-qa-backend \
  --image gcr.io/YOUR_PROJECT_ID/private-knowledge-qa-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_API_KEY \
  --set-env-vars MONGODB_URI=YOUR_MONGODB_URI \
  --set-env-vars CORS_ORIGINS=https://your-frontend-url.vercel.app
```

---

## Step 3: Get Your Backend URL

After deployment, Cloud Run will give you a URL like:
```
https://private-knowledge-qa-backend-XXXXXX-uc.a.run.app
```

**Save this URL** - you'll need it for:
1. Frontend environment variables
2. Testing your API

---

## Step 4: Test Your Deployment

```bash
# Test health endpoint
curl https://YOUR_CLOUD_RUN_URL/api/status/health

# Expected response: JSON with service statuses
```

---

## Step 5: Update Environment Variables Later (if needed)

```bash
gcloud run services update private-knowledge-qa-backend \
  --region us-central1 \
  --set-env-vars CORS_ORIGINS=https://your-new-frontend.vercel.app
```

---

## Important Notes

### CORS Configuration
After deploying the frontend, you MUST update the backend's CORS_ORIGINS:

```bash
gcloud run services update private-knowledge-qa-backend \
  --region us-central1 \
  --set-env-vars CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### Costs
- **Cloud Run**: Free tier includes 2 million requests/month
- **Container Registry**: First 500 MB free
- For this project, you should stay in free tier

### Persistent Storage
**Important**: Cloud Run containers are stateless. Your FAISS vector store will reset on each deployment.

**Solutions**:
1. Store FAISS index in Google Cloud Storage (requires code changes)
2. Accept that it resets (documents in MongoDB will persist, just re-embed them)
3. For submission demo, this is fine - MongoDB keeps the documents

---

## Troubleshooting

### Build Fails
```bash
# Check build logs
gcloud builds list
gcloud builds log BUILD_ID
```

### Deployment Fails
```bash
# Check Cloud Run logs
gcloud run services logs tail private-knowledge-qa-backend --region us-central1
```

### Connection Issues
- Verify MongoDB IP whitelist allows 0.0.0.0/0
- Check environment variables are set correctly
- Ensure CORS_ORIGINS matches frontend URL exactly

---

## Quick Deployment Checklist

- [x] Created Dockerfile
- [x] Created .dockerignore
- [ ] Install gcloud CLI
- [ ] Login and set project: `gcloud auth login`
- [ ] Enable APIs (Run, Container Registry, Cloud Build)
- [ ] Deploy backend: `gcloud run deploy...`
- [ ] Get backend URL from output
- [ ] Test health endpoint
- [ ] Deploy frontend (use backend URL in frontend env)
- [ ] Update backend CORS with frontend URL

---

## After Deployment

1. **Copy your backend URL** from the deployment output
2. **Use it in frontend `.env`**:
   ```env
   REACT_APP_BACKEND_URL=https://your-backend-xxxxx.run.app
   ```
3. **Deploy frontend to Vercel**
4. **Update backend CORS** with frontend URL
5. **Test the full application**

---

**Estimated Time**: 15-20 minutes (including first-time GCP setup)
