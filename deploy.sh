#!/bin/bash

echo "🚀 Deploying Stock King to the web..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Stock King app"
fi

echo "✅ Ready for deployment!"
echo ""
echo "🌐 Choose your deployment platform:"
echo "1. Railway (Recommended - Free): https://railway.app"
echo "2. Heroku: https://heroku.com"
echo "3. Render: https://render.com"
echo ""
echo "📋 Steps:"
echo "1. Push your code to GitHub"
echo "2. Connect your GitHub repo to your chosen platform"
echo "3. Deploy!"
echo ""
echo "🔗 Your app will be available at a public URL that anyone can access!"

# Check if we can push to GitHub
if git remote -v | grep -q origin; then
    echo ""
    echo "📤 Pushing to GitHub..."
    git add .
    git commit -m "Deploy Stock King - Production ready"
    git push origin main
    echo "✅ Pushed to GitHub! Now you can deploy from your platform."
else
    echo ""
    echo "⚠️  No GitHub remote found. Please:"
    echo "1. Create a new repository on GitHub"
    echo "2. Run: git remote add origin https://github.com/yourusername/yourrepo.git"
    echo "3. Run: git push -u origin main"
fi
