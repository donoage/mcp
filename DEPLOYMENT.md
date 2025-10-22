# Railway Deployment Guide

## Quick Deploy to Railway

### Prerequisites
- Railway account (sign up at https://railway.app)
- Railway CLI installed: `npm install -g @railway/cli`

### Step 1: Initialize Railway Project

```bash
cd ~/Projects/mcp/market-query-app
railway login
railway init
```

### Step 2: Set Environment Variables

Set your API keys in Railway:

```bash
railway variables set ANTHROPIC_API_KEY=your-anthropic-api-key-here
railway variables set POLYGON_API_KEY=your-polygon-api-key-here
```

Alternatively, you can set them in the Railway dashboard:
1. Go to your project on https://railway.app
2. Click on your service
3. Go to "Variables" tab
4. Add:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `POLYGON_API_KEY`: Your Polygon.io API key

### Step 3: Deploy

```bash
railway up
```

Or connect your GitHub repository:
1. Push your code to GitHub
2. In Railway dashboard, click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect the configuration and deploy

### Step 4: Get Your URL

After deployment, Railway will provide you with a public URL like:
```
https://your-app-name.up.railway.app
```

## Alternative: Deploy via GitHub

1. **Push to GitHub:**
   ```bash
   cd ~/Projects/mcp/market-query-app
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/market-query-app.git
   git push -u origin main
   ```

2. **Connect to Railway:**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables in the dashboard

3. **Railway will automatically:**
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Run the command from `Procfile`
   - Assign a public URL

## Configuration Files

The project includes these Railway configuration files:

- **`railway.json`**: Railway-specific configuration
- **`Procfile`**: Defines the start command
- **`runtime.txt`**: Specifies Python version
- **`requirements.txt`**: Python dependencies

## Troubleshooting

### Issue: Build fails
- Check that all dependencies are in `requirements.txt`
- Verify Python version compatibility (3.11+)

### Issue: App crashes on startup
- Check environment variables are set correctly
- View logs in Railway dashboard
- Ensure `uv` is available (it should be installed automatically)

### Issue: WebSocket connection fails
- Railway automatically handles WebSocket upgrades
- Check that your Railway URL uses `wss://` for WebSocket connections

### Issue: Slow responses
- First request may be slow as MCP server initializes
- Consider upgrading Railway plan for better performance

## Monitoring

View logs in real-time:
```bash
railway logs
```

Or view in the Railway dashboard under the "Deployments" tab.

## Updating Your Deployment

To update your deployed app:

```bash
railway up
```

Or if using GitHub integration, just push to your main branch:
```bash
git add .
git commit -m "Update"
git push
```

## Cost Considerations

- Railway offers a free tier with $5 credit per month
- This app should run comfortably within the free tier for moderate usage
- Monitor usage in the Railway dashboard
- API costs (Anthropic + Polygon.io) are separate

## Security Notes

- Never commit `.env` file (it's in `.gitignore`)
- Always use Railway's environment variables for secrets
- Rotate API keys if they're ever exposed
- Consider adding authentication for production use

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Polygon.io Support: https://polygon.io/contact
- Anthropic Docs: https://docs.anthropic.com

