@echo off
REM GCP Cloud Run Deployment Script for Backend

echo ============================================
echo Deploying Backend to Google Cloud Run
echo ============================================
echo.

REM Check if user is logged in
echo [1/5] Checking authentication...
gcloud auth list

echo.
echo [2/5] Current project:
gcloud config get-value project

echo.
echo ============================================
echo IMPORTANT: Set your environment variables
echo ============================================
echo.
set /p GEMINI_KEY="Enter your Gemini API Key: "
set /p MONGO_URI="Enter your MongoDB URI: "
set /p FRONTEND_URL="Enter your frontend URL (press Enter for https://private-knowledge-qa-sage.vercel.app): "

if "%FRONTEND_URL%"=="" set FRONTEND_URL=https://private-knowledge-qa-sage.vercel.app

echo.
echo [3/5] Deploying to Cloud Run...
echo Region: us-central1
echo Service: private-knowledge-qa-backend
echo.

gcloud run deploy private-knowledge-qa-backend ^
  --source . ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars GEMINI_API_KEY=%GEMINI_KEY% ^
  --set-env-vars MONGODB_URI=%MONGO_URI% ^
  --set-env-vars CORS_ORIGINS=%FRONTEND_URL%

echo.
echo [4/5] Getting service URL...
gcloud run services describe private-knowledge-qa-backend --region us-central1 --format="value(status.url)"

echo.
echo ============================================
echo [5/5] Deployment Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Copy the service URL above
echo 2. Use it in your frontend .env:
echo    REACT_APP_BACKEND_URL=YOUR_SERVICE_URL
echo 3. Deploy frontend to Vercel
echo 4. Update CORS_ORIGINS with frontend URL
echo.
pause
