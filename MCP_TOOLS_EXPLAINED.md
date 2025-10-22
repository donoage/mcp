# MCP Tool Descriptions Explained

## 🤔 What Are MCP Tool Descriptions?

When you make a query, the Polygon.io MCP server sends Claude a list of ALL available tools (API endpoints) it can use. Each tool includes:

1. **Tool Name** - e.g., `get_stock_price`
2. **Description** - What the tool does
3. **Parameters** - What inputs it needs
4. **Parameter Types** - String, number, date, etc.
5. **Required vs Optional** - Which parameters are mandatory
6. **Examples** - How to use the tool

## 📊 Example: What Gets Sent

Here's what ONE tool description looks like:

```json
{
  "name": "get_previous_close",
  "description": "Get the previous day's open, high, low, and close (OHLC) for the specified stock ticker.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string",
        "description": "The ticker symbol of the stock/equity. Examples: AAPL, TSLA, MSFT"
      },
      "adjusted": {
        "type": "boolean",
        "description": "Whether or not the results are adjusted for splits. Default: true"
      }
    },
    "required": ["ticker"]
  }
}
```

**This ONE tool = ~150 tokens**

## 🎯 All Available Tools (Sent Every Query!)

The Polygon.io MCP server provides approximately **40-50 tools**:

### Stock Market Tools (~15 tools)
1. `get_stock_price` - Current stock price
2. `get_previous_close` - Previous day's OHLC
3. `get_aggregates` - Historical price bars
4. `get_grouped_daily` - All tickers for a date
5. `get_daily_open_close` - Specific day OHLC
6. `get_ticker_details` - Company information
7. `get_ticker_news` - Latest news articles
8. `get_market_status` - Is market open?
9. `get_market_holidays` - Market holiday schedule
10. `get_dividends` - Dividend history
11. `get_stock_splits` - Stock split history
12. `get_financials` - Financial statements
13. `get_related_companies` - Similar companies
14. `get_sma` - Simple Moving Average
15. `get_ema` - Exponential Moving Average

### Options Tools (~8 tools)
16. `get_options_contract` - Option contract details
17. `get_options_chain` - All options for a stock
18. `get_option_snapshot` - Current option data
19. `get_option_aggregates` - Historical option prices
20. `get_option_trades` - Recent option trades
21. `get_option_quotes` - Option bid/ask quotes
22. `get_option_open_interest` - Open interest data
23. `get_option_implied_volatility` - IV data

### Forex Tools (~5 tools)
24. `get_forex_quote` - Current forex rate
25. `get_forex_aggregates` - Historical forex data
26. `get_forex_previous_close` - Previous forex close
27. `get_forex_snapshot` - All forex pairs
28. `get_currency_conversion` - Convert currencies

### Crypto Tools (~5 tools)
29. `get_crypto_price` - Current crypto price
30. `get_crypto_aggregates` - Historical crypto data
31. `get_crypto_previous_close` - Previous crypto close
32. `get_crypto_snapshot` - All crypto pairs
33. `get_crypto_trades` - Recent crypto trades

### Market Data Tools (~8 tools)
34. `get_exchanges` - List of exchanges
35. `get_conditions` - Trade conditions
36. `get_tickers` - Search tickers
37. `get_ticker_types` - Types of securities
38. `get_market_movers` - Gainers/losers
39. `get_snapshot_all_tickers` - All ticker snapshots
40. `get_universal_snapshot` - Multi-asset snapshot
41. `get_technical_indicators` - Various indicators

### Additional Tools (~5 tools)
42. `get_macd` - MACD indicator
43. `get_rsi` - RSI indicator
44. `get_bollinger_bands` - Bollinger Bands
45. `get_vwap` - Volume Weighted Average Price
46. `search_tickers` - Find ticker symbols

## 💰 Token Cost Breakdown

```
Number of Tools: ~45
Tokens per Tool: ~150-200
Total Tool Descriptions: 45 × 175 = 7,875 tokens

Add JSON structure overhead: ~1,000 tokens
Add MCP protocol metadata: ~500 tokens

TOTAL PER QUERY: ~9,000-10,000 tokens
```

## 🤷 Do We Need All These Tools?

### The Problem:
- You ask: "What's Apple's stock price?" (10 tokens)
- MCP sends: Descriptions of 45 tools (9,000 tokens)
- Claude uses: 1 tool (`get_stock_price`)
- **Waste**: 44 unused tool descriptions = 8,800 tokens!

### Why It Works This Way:
1. **Claude needs to know what tools exist** to choose the right one
2. **MCP protocol sends all tools** by design
3. **No way to filter** which tools to send (yet)

### Do We NEED It?
**Yes and No:**

✅ **Yes, we need SOME tool descriptions:**
- Claude must know what tools are available
- Needs to understand parameters and formats
- Required for intelligent tool selection

❌ **No, we don't need ALL of them:**
- Most queries use 1-3 tools
- 90% of tools go unused
- Massive token waste

## 🔧 Alternatives to MCP

### Option 1: Direct API Calls (No MCP)
```python
# Instead of MCP, call Polygon.io directly
import requests

def get_stock_price(ticker):
    response = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev",
        params={"apiKey": POLYGON_API_KEY}
    )
    return response.json()

# Then let Claude analyze the result
result = get_stock_price("AAPL")
response = await agent.run(f"Analyze this data: {result}")
```

**Pros:**
- No MCP overhead (save 9,000 tokens!)
- Full control over API calls
- Faster responses

**Cons:**
- Lose Claude's intelligent tool selection
- More code to maintain
- Manual error handling
- No automatic parameter validation

### Option 2: Selective Tool Loading (Custom MCP)
Fork the Polygon.io MCP server and only expose relevant tools:

```python
# Custom MCP server with only 5 tools
tools = [
    "get_stock_price",
    "get_previous_close", 
    "get_ticker_news",
    "get_ticker_details",
    "get_aggregates"
]
```

**Pros:**
- Keep MCP benefits
- Reduce tokens by 80% (9,000 → 1,800)
- Still intelligent tool selection

**Cons:**
- Need to maintain custom MCP server
- Lose access to other tools
- More complex setup

### Option 3: Hybrid Approach
Use MCP for complex queries, direct API for simple ones:

```python
if is_simple_price_query(query):
    # Direct API call (no MCP overhead)
    result = get_stock_price(ticker)
else:
    # Use MCP for complex analysis
    result = await agent.run(query)
```

**Pros:**
- Best of both worlds
- Optimize common cases
- Keep flexibility for complex queries

**Cons:**
- More complex logic
- Need query classification
- Maintenance overhead

## 📈 Token Savings Comparison

| Approach | Tokens per Query | Savings | Complexity |
|----------|------------------|---------|------------|
| **Current (Full MCP)** | 12,000-15,000 | 0% | Low |
| **Direct API** | 3,000-5,000 | 70% | Medium |
| **Selective MCP** | 5,000-8,000 | 50% | High |
| **Hybrid** | 4,000-10,000 | 40% | Very High |

## 🎯 Recommendations

### For Your Use Case:

**Current Setup (Keep MCP)** ✅ RECOMMENDED
- **Why**: You want the full power of Claude's reasoning
- **Trade-off**: Higher token cost for better intelligence
- **Best for**: Complex financial analysis, comparisons, multi-step queries

**When to Consider Alternatives:**

1. **Direct API** if:
   - 90% of queries are simple price checks
   - Budget is very tight
   - You don't need Claude's reasoning

2. **Selective MCP** if:
   - You know exactly which tools you need
   - Willing to maintain custom server
   - Need both intelligence and efficiency

3. **Hybrid** if:
   - Mix of simple and complex queries
   - Want to optimize costs
   - Have development resources

## 💡 Current Optimizations (Already Implemented)

We've already optimized what we CAN control:

✅ **Limited conversation history** (4 messages max)
- Saves: 2,000-5,000 tokens per query

✅ **Concise system prompt** (150 tokens)
- Saves: 100 tokens per query

✅ **Rate limiting** (3 queries/min)
- Prevents: Token usage spikes

✅ **Timeout protection** (60 seconds)
- Prevents: Runaway queries

**What we CAN'T optimize:**
❌ MCP tool descriptions (9,000 tokens) - Controlled by MCP server

## 🔮 Future Improvements

### MCP Protocol Enhancements (Coming?)
The MCP protocol may eventually support:
- **Tool filtering** - Only send relevant tools
- **Tool caching** - Send tools once, reference later
- **Dynamic tool loading** - Load tools on demand
- **Tool categories** - Group related tools

### For Now:
The token cost is the price of using MCP's powerful abstraction. It's like paying for a full buffet when you only want one dish - but you get access to everything if you need it!

## 📊 Real-World Impact

### Your Current Usage:
- **Queries per day**: ~10-50
- **Tokens per query**: ~12,000
- **Daily tokens**: 120,000-600,000
- **Monthly cost**: $10-$50

### With Direct API (No MCP):
- **Tokens per query**: ~3,000
- **Daily tokens**: 30,000-150,000
- **Monthly cost**: $3-$15
- **Savings**: 70% ($7-$35/month)

### Is It Worth Switching?
**Probably not** because:
- MCP provides intelligent tool selection
- Claude can handle complex multi-step queries
- Better user experience
- Less code to maintain
- $7-$35/month is reasonable for the convenience

## 🎓 Summary

**MCP Tool Descriptions:**
- ~9,000 tokens per query
- Descriptions of 45+ Polygon.io API endpoints
- Necessary for Claude to know what tools exist
- Biggest source of token usage (60-70%)

**Do We Need It?**
- **Technically**: No, could use direct API calls
- **Practically**: Yes, for intelligent financial analysis
- **Trade-off**: Higher tokens for better AI reasoning

**Current Setup**: Optimized for intelligence over cost
**Alternative**: Direct API would save 70% tokens but lose AI benefits

---

**Recommendation**: Keep MCP unless token costs become prohibitive. The intelligence and convenience are worth the extra tokens for most use cases.

**Reference**: [Polygon.io MCP Server](https://github.com/polygon-io/mcp_polygon)

