# Stock King - Deployment Guide

## Quick Deploy Options

### Option 1: Railway (Recommended - Free)
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect the Python app and deploy it
6. Your app will be available at `https://your-app-name.railway.app`

### Option 2: Heroku (Free tier discontinued, but still works)
1. Install Heroku CLI
2. Run these commands:
```bash
heroku create stock-king-app
git add .
git commit -m "Deploy Stock King"
git push heroku main
```

### Option 3: Render (Free tier available)
1. Go to [Render.com](https://render.com)
2. Connect your GitHub repository
3. Select "Web Service"
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && python api/production_server.py`
5. Deploy!

## Manual Setup

### Backend Deployment
1. The backend is configured to run on Railway/Heroku
2. Database will be created automatically on first run
3. S&P 500 data will be populated automatically

### Frontend
The frontend is embedded in the HTML file and will be served by the backend.

## Environment Variables
No additional environment variables needed - everything is configured for production.

## Testing
After deployment, test these endpoints:
- `GET /` - Main application
- `GET /health` - Health check
- `GET /tickers` - S&P 500 tickers
- `GET /analysis/{ticker}` - Stock analysis

## Troubleshooting
- Check logs in your hosting platform
- Ensure all dependencies are in requirements.txt
- Verify the database is being created properly
