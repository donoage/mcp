# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Navigate to Project
```bash
cd ~/Projects/mcp/market-query-app
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Start the Server
```bash
python app.py
```

### Step 4: Open in Browser
Open http://localhost:8000

### Step 5: Try a Query
Type in the input box:
```
What is the latest price of Tesla?
```

Click "Analyze" or press Cmd+Enter

---

## 🌐 Deploy to Railway (3 Minutes)

### Option A: Using the Script
```bash
./deploy.sh
```
Follow the prompts!

### Option B: Manual Commands
```bash
# Login
railway login

# Initialize
railway init

# Set variables (use your actual keys)
railway variables set ANTHROPIC_API_KEY=your-anthropic-api-key-here
railway variables set POLYGON_API_KEY=your-polygon-api-key-here

# Deploy
railway up

# Get URL
railway open
```

---

## 🎯 Example Queries to Try

**Simple Price Check**
```
Get the latest price of Apple
```

**Comparison**
```
Compare the performance of Tesla and Ford over the last 6 months
```

**Market Analysis**
```
What is the market sentiment for NVIDIA based on recent news?
```

**Investment Analysis**
```
Consider an investment between Meta, Amazon, and Google. Which one is the best bet based on returns and earnings?
```

**Historical Data**
```
Look back from today to five years ago. Return the total return on investment for Microsoft
```

---

## 🛠️ Troubleshooting

**Server won't start?**
```bash
# Make sure you're in the right directory
cd ~/Projects/mcp/market-query-app

# Activate virtual environment
source venv/bin/activate

# Check Python version (should be 3.11+)
python --version

# Reinstall dependencies if needed
pip install -r requirements.txt
```

**WebSocket not connecting?**
- Check browser console (F12)
- Make sure server is running
- Try refreshing the page

**Slow responses?**
- First query is always slower (initialization)
- Subsequent queries are faster
- Complex queries take longer

---

## 📱 Using the Interface

### Query Input
- Type your question in the textarea
- Click "Analyze" button or press **Cmd+Enter** (Mac) / **Ctrl+Enter** (Windows)
- Use example query buttons for inspiration

### Response Display
- Results appear in formatted markdown
- "Tools Used" section shows which APIs were called
- Click "Clear" to start a new conversation

### Status Indicator
- **Green dot**: Connected and ready
- **Red dot**: Disconnected
- **Yellow dot**: Processing

---

## 🔑 API Keys

Configure your API keys in the `.env` file:

**Anthropic API Key**: Get yours at https://console.anthropic.com/

**Polygon API Key**: Get yours at https://polygon.io/

To set them, edit the `.env` file or copy from `.env.example`.

---

## 📖 More Information

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Project Details**: See `PROJECT_SUMMARY.md`

---

## 🆘 Need Help?

1. Check the logs in your terminal
2. Review the troubleshooting section in `README.md`
3. Check Railway logs: `railway logs`
4. Verify API keys are correct in `.env`

---

**That's it! You're ready to query financial markets with AI! 🎉**

