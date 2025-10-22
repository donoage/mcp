#!/bin/bash

# Railway Deployment Script for Market Query AI

echo "🚀 Market Query AI - Railway Deployment"
echo "========================================"
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Railway CLI"
        echo "Please install it manually: npm install -g @railway/cli"
        exit 1
    fi
fi

echo "✅ Railway CLI found"
echo ""

# Check if logged in
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "Please log in to Railway..."
    railway login
    if [ $? -ne 0 ]; then
        echo "❌ Failed to log in to Railway"
        exit 1
    fi
fi

echo "✅ Authenticated with Railway"
echo ""

# Check if project is initialized
if [ ! -f ".railway" ] && [ ! -d ".railway" ]; then
    echo "🎯 Initializing Railway project..."
    railway init
    if [ $? -ne 0 ]; then
        echo "❌ Failed to initialize Railway project"
        exit 1
    fi
fi

echo "✅ Railway project initialized"
echo ""

# Set environment variables
echo "🔧 Setting environment variables..."
echo ""
echo "Please enter your API keys (or press Enter to skip if already set):"
echo ""

read -p "Anthropic API Key (or press Enter to skip): " ANTHROPIC_KEY
if [ ! -z "$ANTHROPIC_KEY" ]; then
    railway variables set ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
    echo "✅ Anthropic API key set"
fi

read -p "Polygon.io API Key (or press Enter to skip): " POLYGON_KEY
if [ ! -z "$POLYGON_KEY" ]; then
    railway variables set POLYGON_API_KEY="$POLYGON_KEY"
    echo "✅ Polygon API key set"
fi

echo ""
echo "📋 Current environment variables:"
railway variables
echo ""

# Deploy
echo "🚀 Deploying to Railway..."
railway up

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Your app is now live!"
    echo "📊 View logs: railway logs"
    echo "🔗 Open app: railway open"
    echo ""
    echo "To view your app URL, run: railway open"
else
    echo ""
    echo "❌ Deployment failed"
    echo "📋 Check logs: railway logs"
    exit 1
fi

