#!/usr/bin/env python3
"""
Custom Lightweight MCP Server for Polygon.io
Only includes stock market tools (no options, forex, or crypto)
Reduces token usage by ~40-50%
"""

import os
import sys
import json
import asyncio
from typing import Any, Sequence
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

# Get API key from environment
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
BASE_URL = "https://api.polygon.io"

# Initialize MCP server
app = Server("polygon-stocks-only")

# HTTP client for API calls
http_client = httpx.AsyncClient(timeout=30.0)


async def call_polygon_api(endpoint: str, params: dict = None) -> dict:
    """Make API call to Polygon.io"""
    if params is None:
        params = {}
    params["apiKey"] = POLYGON_API_KEY
    
    url = f"{BASE_URL}{endpoint}"
    response = await http_client.get(url, params=params)
    response.raise_for_status()
    return response.json()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools - STOCK MARKET ONLY"""
    return [
        Tool(
            name="get_stock_price",
            description="Get the current/latest stock price for a ticker symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL, TSLA, MSFT)"
                    }
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_previous_close",
            description="Get previous day's OHLC (open, high, low, close) for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol"
                    },
                    "adjusted": {
                        "type": "boolean",
                        "description": "Adjusted for splits (default: true)"
                    }
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_aggregates",
            description="Get historical price bars/candles for a stock over a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker"},
                    "multiplier": {"type": "integer", "description": "Size of timespan (e.g., 1)"},
                    "timespan": {"type": "string", "description": "Size of time window: minute, hour, day, week, month, quarter, year"},
                    "from_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "to_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                    "adjusted": {"type": "boolean", "description": "Adjusted for splits"}
                },
                "required": ["ticker", "multiplier", "timespan", "from_date", "to_date"]
            }
        ),
        Tool(
            name="get_ticker_details",
            description="Get detailed company information for a stock ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_ticker_news",
            description="Get latest news articles for a stock ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "limit": {"type": "integer", "description": "Number of articles (default: 10)"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_market_status",
            description="Get current market status (open/closed) and upcoming holidays",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_dividends",
            description="Get dividend history for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_stock_splits",
            description="Get stock split history for a ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_daily_open_close",
            description="Get open, high, low, close for a specific date",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker"},
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD)"},
                    "adjusted": {"type": "boolean", "description": "Adjusted for splits"}
                },
                "required": ["ticker", "date"]
            }
        ),
        Tool(
            name="search_tickers",
            description="Search for stock ticker symbols by company name or keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {"type": "string", "description": "Search query (company name or keyword)"},
                    "limit": {"type": "integer", "description": "Max results (default: 10)"}
                },
                "required": ["search"]
            }
        ),
        Tool(
            name="get_sma",
            description="Get Simple Moving Average (SMA) technical indicator",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker"},
                    "timestamp": {"type": "string", "description": "Date (YYYY-MM-DD)"},
                    "window": {"type": "integer", "description": "Window size (e.g., 50 for 50-day SMA)"},
                    "timespan": {"type": "string", "description": "day, week, month"}
                },
                "required": ["ticker", "timespan"]
            }
        ),
        Tool(
            name="get_ema",
            description="Get Exponential Moving Average (EMA) technical indicator",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker"},
                    "timestamp": {"type": "string", "description": "Date (YYYY-MM-DD)"},
                    "window": {"type": "integer", "description": "Window size (e.g., 12 for 12-day EMA)"},
                    "timespan": {"type": "string", "description": "day, week, month"}
                },
                "required": ["ticker", "timespan"]
            }
        ),
        Tool(
            name="get_rsi",
            description="Get Relative Strength Index (RSI) technical indicator",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker"},
                    "timestamp": {"type": "string", "description": "Date (YYYY-MM-DD)"},
                    "window": {"type": "integer", "description": "Window size (default: 14)"},
                    "timespan": {"type": "string", "description": "day, week, month"}
                },
                "required": ["ticker", "timespan"]
            }
        ),
        Tool(
            name="get_macd",
            description="Get MACD (Moving Average Convergence Divergence) indicator",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker"},
                    "timestamp": {"type": "string", "description": "Date (YYYY-MM-DD)"},
                    "timespan": {"type": "string", "description": "day, week, month"}
                },
                "required": ["ticker", "timespan"]
            }
        ),
        Tool(
            name="get_snapshot_all_tickers",
            description="Get snapshot of all tickers (current prices, volume, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "tickers": {"type": "string", "description": "Comma-separated ticker list (optional)"}
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls"""
    try:
        if name == "get_stock_price":
            data = await call_polygon_api(f"/v2/aggs/ticker/{arguments['ticker']}/prev")
            
        elif name == "get_previous_close":
            adjusted = arguments.get("adjusted", True)
            data = await call_polygon_api(
                f"/v2/aggs/ticker/{arguments['ticker']}/prev",
                {"adjusted": str(adjusted).lower()}
            )
            
        elif name == "get_aggregates":
            data = await call_polygon_api(
                f"/v2/aggs/ticker/{arguments['ticker']}/range/{arguments['multiplier']}/{arguments['timespan']}/{arguments['from_date']}/{arguments['to_date']}",
                {"adjusted": str(arguments.get("adjusted", True)).lower()}
            )
            
        elif name == "get_ticker_details":
            data = await call_polygon_api(f"/v3/reference/tickers/{arguments['ticker']}")
            
        elif name == "get_ticker_news":
            limit = arguments.get("limit", 10)
            data = await call_polygon_api(
                f"/v2/reference/news",
                {"ticker": arguments['ticker'], "limit": limit}
            )
            
        elif name == "get_market_status":
            data = await call_polygon_api("/v1/marketstatus/now")
            
        elif name == "get_dividends":
            data = await call_polygon_api(f"/v3/reference/dividends", {"ticker": arguments['ticker']})
            
        elif name == "get_stock_splits":
            data = await call_polygon_api(f"/v3/reference/splits", {"ticker": arguments['ticker']})
            
        elif name == "get_daily_open_close":
            adjusted = arguments.get("adjusted", True)
            data = await call_polygon_api(
                f"/v1/open-close/{arguments['ticker']}/{arguments['date']}",
                {"adjusted": str(adjusted).lower()}
            )
            
        elif name == "search_tickers":
            limit = arguments.get("limit", 10)
            data = await call_polygon_api(
                "/v3/reference/tickers",
                {"search": arguments['search'], "limit": limit, "market": "stocks"}
            )
            
        elif name == "get_sma":
            params = {
                "timestamp": arguments.get("timestamp"),
                "timespan": arguments["timespan"],
                "window": arguments.get("window", 50)
            }
            data = await call_polygon_api(
                f"/v1/indicators/sma/{arguments['ticker']}",
                {k: v for k, v in params.items() if v is not None}
            )
            
        elif name == "get_ema":
            params = {
                "timestamp": arguments.get("timestamp"),
                "timespan": arguments["timespan"],
                "window": arguments.get("window", 12)
            }
            data = await call_polygon_api(
                f"/v1/indicators/ema/{arguments['ticker']}",
                {k: v for k, v in params.items() if v is not None}
            )
            
        elif name == "get_rsi":
            params = {
                "timestamp": arguments.get("timestamp"),
                "timespan": arguments["timespan"],
                "window": arguments.get("window", 14)
            }
            data = await call_polygon_api(
                f"/v1/indicators/rsi/{arguments['ticker']}",
                {k: v for k, v in params.items() if v is not None}
            )
            
        elif name == "get_macd":
            params = {
                "timestamp": arguments.get("timestamp"),
                "timespan": arguments["timespan"]
            }
            data = await call_polygon_api(
                f"/v1/indicators/macd/{arguments['ticker']}",
                {k: v for k, v in params.items() if v is not None}
            )
            
        elif name == "get_snapshot_all_tickers":
            endpoint = "/v2/snapshot/locale/us/markets/stocks/tickers"
            if arguments.get("tickers"):
                endpoint = f"/v2/snapshot/locale/us/markets/stocks/tickers/{arguments['tickers']}"
            data = await call_polygon_api(endpoint)
            
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

