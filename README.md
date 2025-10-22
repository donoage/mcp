# Market Query AI

A beautiful web application for querying financial markets using AI. Built with Polygon.io MCP server, Claude 4, and Pydantic AI.

## Features

- 🤖 AI-powered financial analysis using Claude 4
- 📊 Real-time market data from Polygon.io
- 💬 Interactive chat interface with WebSocket support
- 🎨 Modern, Polygon.io-inspired UI design
- 🚀 Ready for Railway deployment

## Tech Stack

- **Backend**: FastAPI + Python 3.11
- **AI**: Anthropic Claude 4 Sonnet via Pydantic AI
- **Data**: Polygon.io MCP Server
- **Frontend**: Vanilla JavaScript + WebSockets
- **Styling**: Custom CSS with modern design

## Prerequisites

- Python 3.10+
- Anthropic API key
- Polygon.io API key

## Local Development

1. **Clone the repository**
   ```bash
   cd ~/Projects/mcp/market-query-app
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your keys:
   ```
   ANTHROPIC_API_KEY=your_key_here
   POLYGON_API_KEY=your_key_here
   PORT=8000
   ```

5. **Run the application**
   ```bash
   python app.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Open in browser**
   
   Navigate to `http://localhost:8000`

## Railway Deployment

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   cd ~/Projects/mcp/market-query-app
   railway init
   ```

4. **Set environment variables**
   ```bash
   railway variables set ANTHROPIC_API_KEY=your_key_here
   railway variables set POLYGON_API_KEY=your_key_here
   ```

5. **Deploy**
   ```bash
   railway up
   ```

## Usage Examples

Try asking questions like:

- "What is the latest price of Tesla?"
- "Compare Apple and Microsoft performance over the last year"
- "Get the market sentiment for NVIDIA based on recent news"
- "Look back from today to five years ago. Return the total return on investment for Microsoft"
- "Consider an investment between Meta, Amazon, and Google. Which one is the best bet based on returns, earnings, latest news, and market sentiment"

## Project Structure

```
market-query-app/
├── app.py                 # FastAPI application with WebSocket support
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment variables
├── railway.json          # Railway configuration
├── Procfile              # Process file for deployment
├── runtime.txt           # Python version specification
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Modern UI styling
│   └── js/
│       └── app.js        # WebSocket client logic
└── templates/
    └── index.html        # Main HTML template
```

## Features in Detail

### AI-Powered Analysis
- Uses Claude 4 Sonnet for advanced reasoning
- Breaks down complex queries into logical subtasks
- Provides structured, markdown-formatted responses

### Real-Time Data
- Access to Polygon.io's institutional-grade market data
- Stock prices, historical data, news, and more
- Automatic handling of stock splits and adjustments

### Modern UI
- Inspired by Polygon.io's design language
- Dark theme optimized for financial data
- Responsive design for mobile and desktop
- Real-time status indicators
- Smooth animations and transitions

### WebSocket Communication
- Real-time bidirectional communication
- Live status updates during query processing
- Automatic reconnection on disconnect
- Message history for context-aware conversations

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude 4 | Yes |
| `POLYGON_API_KEY` | Your Polygon.io API key | Yes |
| `PORT` | Port to run the server on | No (default: 8000) |

## Troubleshooting

### WebSocket Connection Issues
- Ensure your firewall allows WebSocket connections
- Check that the PORT environment variable matches your server configuration
- For Railway deployment, ensure the domain is correctly configured

### API Rate Limits
- Polygon.io free tier has rate limits
- Consider upgrading your plan for production use
- Implement caching if needed

### MCP Server Issues
- Ensure `uvx` is installed (comes with `uv`)
- Check that the Polygon.io MCP server version is compatible
- Review logs for specific error messages

## License

MIT License - feel free to use this project for your own purposes.

## Disclaimer

This tool provides AI-generated financial analysis. Always verify information before making investment decisions. The outputs may not always be accurate and should not be treated as financial advice.

## Credits

- Built with [Polygon.io](https://polygon.io/)
- Powered by [Anthropic Claude 4](https://www.anthropic.com/)
- Using [Pydantic AI](https://ai.pydantic.dev/)
- Inspired by the [Polygon.io MCP Server tutorial](https://polygon.io/blog/querying-financial-markets-with-the-polgon-io-mcp-server-claude-4-and-pydantic-ai)

