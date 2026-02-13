# Deployment Guide

This guide covers deploying the Private Knowledge Q&A application to various hosting platforms.

## Recommended Deployment Architecture

**Frontend**: Vercel or Netlify (free tier available)  
**Backend**: Railway, Render, or Fly.io (free tier available)  
**Database**: MongoDB Atlas (free tier available)  
**Vector Store**: Runs on backend server (FAISS persists to disk)

## Prerequisites

- [ ] Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- [ ] GitHub account for repository
- [ ] MongoDB Atlas account ([Sign up](https://www.mongodb.com/cloud/atlas/register))

## Step 1: MongoDB Atlas Setup

1. Create a free cluster on MongoDB Atlas
2. Create a database user with read/write permissions
3. Whitelist `0.0.0.0/0` (allow from anywhere) in Network Access
4. Get your connection string: `mongodb+srv://username:password@cluster.mongodb.net/knowledge_qa`

## Step 2: Backend Deployment (Railway)

### Option A: Railway (Recommended)

1. **Create Railway Account**: https://railway.app
2. **Create New Project** → Deploy from GitHub repo
3. **Add Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/knowledge_qa
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   PORT=8000
   ```
4. **Set Build Command**: Leave empty (Railway auto-detects)
5. **Set Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. **Set Root Directory**: `backend`
7. **Deploy** and note your backend URL (e.g., `https://your-app.railway.app`)

### Option B: Render

1. **Create Render Account**: https://render.com
2. **New Web Service** → Connect GitHub repo
3. **Settings**:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables** (same as Railway)
5. **Deploy** and note your backend URL

### Option C: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Create `Dockerfile` in `backend/`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
   ```
3. Deploy:
   ```bash
   cd backend
   fly launch
   fly secrets set GEMINI_API_KEY=xxx MONGODB_URI=xxx CORS_ORIGINS=xxx
   fly deploy
   ```

## Step 3: Frontend Deployment (Vercel)

### Option A: Vercel (Recommended)

1. **Create Vercel Account**: https://vercel.com
2. **Import Project** → Select your GitHub repo
3. **Framework Preset**: Create React App
4. **Root Directory**: `frontend`
5. **Environment Variables**:
   ```
   REACT_APP_BACKEND_URL=https://your-backend.railway.app
   ```
6. **Deploy** → Note your frontend URL (e.g., `https://your-app.vercel.app`)
7. **Update Backend CORS**: Go back to Railway/Render and update `CORS_ORIGINS` to include your Vercel URL

### Option B: Netlify

1. **Create Netlify Account**: https://netlify.com
2. **New Site from Git** → Connect repo
3. **Build Settings**:
   - **Base Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Publish Directory**: `frontend/build`
4. **Environment Variables**: Same as Vercel
5. **Deploy**

## Step 4: Update CORS

After deploying frontend, update backend's `CORS_ORIGINS`:

**Railway/Render Dashboard**:
```
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
```

Redeploy backend if needed.

## Step 5: Verify Deployment

1. Visit your frontend URL
2. Check Status page - all services should show "healthy"
3. Upload a test document
4. Ask a question
5. Verify sources are displayed

## Troubleshooting

### Backend won't start
- Check logs for missing environment variables
- Verify MongoDB connection string is correct
- Ensure Gemini API key is valid

### CORS errors
- Verify `CORS_ORIGINS` includes your frontend URL
- Check for trailing slashes (don't include them)
- Restart backend after changing CORS settings

### Uploads not working
- Ensure backend has write permissions (most platforms support this by default)
- FAISS data persists to `/app/data` on backend server

### MongoDB connection fails
- Check if IP whitelist includes `0.0.0.0/0`
- Verify database user has correct permissions
- Test connection string with `mongosh`

### Gemini API errors
- Verify API key is correct
- Check quota limits (free tier: 15 RPM)
- Review error logs for rate limiting

## Cost Estimates

**Free Tier (Perfect for MVP)**:
- Railway: 500 hours/month free
- Vercel: Unlimited hobby projects
- MongoDB Atlas: 512MB storage free
- Gemini: 15 RPM, 1500 RPD free

**Production (Estimated)**:
- Railway: $5-10/month for backend
- Vercel: Free (or $20/month Pro)
- MongoDB Atlas: $0-9/month (depends on usage)
- Gemini: $0.50-5/month (typical usage)

Total: ~$5-25/month for production deployment

## Alternative: Docker (Local/Self-Hosted)

Create `docker-compose.yml` in root:

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MONGODB_URI=mongodb://mongodb:27017/knowledge_qa
      - CORS_ORIGINS=http://localhost:3000
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8000

volumes:
  mongo-data:
```

Run: `docker-compose up --build`

## Environment Variables Checklist

### Backend
- [x] `GEMINI_API_KEY` - From Google AI Studio
- [x] `MONGODB_URI` - MongoDB Atlas connection string
- [x] `CORS_ORIGINS` - Frontend URL(s), comma-separated
- [x] `PORT` - (Auto-set by Railway/Render)

### Frontend
- [x] `REACT_APP_BACKEND_URL` - Backend API URL

## Post-Deployment

1. **Test thoroughly**: Upload, ask, delete, check status
2. **Monitor logs**: Watch for errors in first 24 hours
3. **Set up alerts**: Most platforms offer free monitoring
4. **Document URLs**: Save backend + frontend URLs for submission

## Keeping It Live

- Railway free tier sleeps after inactivity (wakes on request)
- Vercel never sleeps
- MongoDB Atlas free tier never expires
- To prevent sleep: Set up a cron job to ping your backend every 10 minutes

## Submission Checklist

- [ ] Frontend deployed and accessible
- [ ] Backend deployed and accessible
- [ ] Status page shows all services healthy
- [ ] Can upload document successfully
- [ ] Can ask question and see sources
- [ ] GitHub repo pushed with all code
- [ ] All documentation files present
- [ ] No API keys in code
- [ ] .env.example files in place
