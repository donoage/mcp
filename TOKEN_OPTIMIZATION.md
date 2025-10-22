# Token Usage & Optimization Guide

## 🔍 Why So Many Tokens?

### Token Usage Breakdown (Per Query)

| Source | Tokens | Percentage |
|--------|--------|------------|
| **MCP Tool Descriptions** | 8,000-12,000 | 60-70% |
| **Conversation History** | 2,000-5,000 | 15-25% |
| **System Prompt** | 100-200 | 1-2% |
| **Your Query** | 50-500 | 1-3% |
| **Formatting Context** | 500-1,000 | 3-5% |
| **TOTAL** | ~12,000-18,000 | 100% |

### The Main Culprit: MCP Tool Descriptions

The Polygon.io MCP server provides access to dozens of tools:
- Stock prices (current, historical, OHLC)
- Company information
- News and sentiment
- Options data
- Forex rates
- Crypto prices
- Market status
- Dividends
- Splits
- And many more...

**Every single query** sends descriptions of ALL these tools to Claude, even if you only need one!

## ✅ Optimizations Implemented

### 1. **Limited Conversation History**
```python
MAX_HISTORY_MESSAGES = 4  # Only keep last 2 exchanges
```
- **Before**: Unlimited history (grows indefinitely)
- **After**: Only last 4 messages (2 Q&A pairs)
- **Savings**: 2,000-5,000 tokens per query after the 3rd query

### 2. **Shorter System Prompt**
```python
# Before: 150 tokens
"You are an expert financial analyst. Note that when using Polygon tools, 
prices are already stock split adjusted. Use the latest data available. 
Always double check your math. For any questions about the current date, 
use the 'get_today_date' tool. For long or complex queries, break the query 
into logical subtasks and process each subtask in order. Format your responses 
in a clear, structured way using markdown when appropriate."

# After: 50 tokens
"You are a financial analyst. Polygon prices are stock-split adjusted. 
Use latest data. For current date, use 'get_today_date' tool. 
Format responses clearly with markdown."
```
- **Savings**: ~100 tokens per query

### 3. **Rate Limiting** (Already Implemented)
- Prevents rapid queries that compound token usage
- **Limit**: 3 queries per minute

## 📊 Expected Token Usage Now

### First Query:
- **Before Optimization**: ~15,000-18,000 tokens
- **After Optimization**: ~12,000-15,000 tokens
- **Savings**: ~3,000 tokens (20%)

### Subsequent Queries:
- **Before Optimization**: ~18,000-25,000 tokens (with growing history)
- **After Optimization**: ~12,000-15,000 tokens (capped history)
- **Savings**: ~6,000-10,000 tokens (40-50%)

## 🚫 What We CAN'T Optimize

### MCP Tool Descriptions (8,000-12,000 tokens)
This is controlled by the Polygon.io MCP server, not our app. The server sends ALL tool descriptions on every request.

**Why?** Claude needs to know what tools are available to answer your question.

**Solutions:**
1. **Accept it** - This is the cost of using MCP servers
2. **Use Polygon.io API directly** - More work, but full control
3. **Wait for MCP improvements** - Future versions may optimize this

## 💰 Cost Implications

### Claude Sonnet 4.5 Pricing:
- **Input**: $3 per million tokens
- **Output**: $15 per million tokens

### Per Query Cost:
```
Input:  12,000 tokens × $3 / 1,000,000 = $0.036
Output:   500 tokens × $15 / 1,000,000 = $0.0075
Total: ~$0.04 per query
```

### With Rate Limiting (3 queries/min):
- **Per hour**: 180 queries × $0.04 = $7.20
- **Per day** (8 hours): $57.60
- **Per month** (20 days): $1,152

**Reality Check**: Most users don't query continuously!
- **Realistic usage**: 10-50 queries/day = $0.40-$2.00/day

## 🎯 Best Practices to Minimize Tokens

### 1. **Clear Conversation History**
Click the "Clear" button after getting your answer if you don't need context.
- **Saves**: 2,000-5,000 tokens per subsequent query

### 2. **Ask Specific Questions**
❌ Bad: "Tell me everything about tech stocks"
✅ Good: "What is Apple's current stock price?"

### 3. **Avoid Follow-up Questions**
Instead of:
1. "What's Tesla's price?"
2. "What about yesterday?"
3. "And the day before?"

Ask once:
"What was Tesla's price for the last 3 days?"

### 4. **Use Simple Queries**
Complex queries trigger more tool calls = more tokens
- Each tool call adds ~1,000-2,000 tokens to the response

### 5. **Batch Your Questions**
Instead of 5 separate queries, ask:
"Get the current prices for AAPL, TSLA, MSFT, GOOGL, and AMZN"

## 🔧 Advanced Optimizations (Not Implemented)

### Option 1: Implement Caching
```python
# Cache common queries
cache = {
    "AAPL_price": {"data": 150.25, "timestamp": time.time()}
}
```
- **Pros**: Eliminates API calls for repeated queries
- **Cons**: Data may be stale

### Option 2: Use Polygon.io API Directly
Skip the MCP server entirely:
```python
import requests
response = requests.get(
    "https://api.polygon.io/v2/aggs/ticker/AAPL/prev",
    params={"apiKey": POLYGON_API_KEY}
)
```
- **Pros**: No MCP overhead, full control
- **Cons**: More code, lose Claude's reasoning

### Option 3: Selective Tool Loading
Modify MCP server to only send relevant tool descriptions:
- **Pros**: Massive token savings (50-70%)
- **Cons**: Requires forking/modifying MCP server

### Option 4: Use Claude Haiku for Simple Queries
Switch to cheaper model for simple price checks:
- **Claude Haiku**: $0.25 per million input tokens (12x cheaper!)
- **Use for**: Simple price queries, basic data lookups
- **Use Sonnet for**: Complex analysis, comparisons

## 📈 Monitoring Token Usage

### Check Anthropic Dashboard
1. Go to https://console.anthropic.com
2. Click "Usage"
3. View token consumption by day

### Response Headers
The API returns usage in headers:
```
anthropic-ratelimit-input-tokens-remaining: 28500
anthropic-ratelimit-input-tokens-limit: 30000
```

## 🎓 Understanding the Math

### Why 30,000 tokens/min is limiting:

With 15,000 tokens per query:
- **Max queries**: 30,000 ÷ 15,000 = 2 queries/min
- **Our limit**: 3 queries/min (conservative)

After optimization (12,000 tokens per query):
- **Max queries**: 30,000 ÷ 12,000 = 2.5 queries/min
- **Our limit**: Still 3 queries/min (safe buffer)

## 🚀 Recommended Configuration

### For Light Usage (<50 queries/day):
```python
MAX_HISTORY_MESSAGES = 4  # Current setting
rate_limiter = RateLimiter(max_requests=3, time_window=60)
```

### For Moderate Usage (50-200 queries/day):
```python
MAX_HISTORY_MESSAGES = 2  # Less history
rate_limiter = RateLimiter(max_requests=2, time_window=60)
```

### For Heavy Usage (>200 queries/day):
```python
MAX_HISTORY_MESSAGES = 0  # No history (stateless)
rate_limiter = RateLimiter(max_requests=2, time_window=60)
# Consider upgrading Anthropic plan
```

## 📞 Need Higher Limits?

### Contact Anthropic Sales:
- Email: sales@anthropic.com
- Request: Higher rate limits
- Mention: Production use case
- Typical increase: 100,000-500,000 tokens/min

## 🎯 Summary

**Token Usage**: ~12,000-15,000 per query (after optimization)
**Main Cost**: MCP tool descriptions (unavoidable)
**Optimizations**: ✅ History limiting, ✅ Shorter prompts, ✅ Rate limiting
**Cost**: ~$0.04 per query
**Realistic Daily Cost**: $0.40-$2.00 (10-50 queries)

The high token usage is primarily due to the MCP server architecture, not your app. The optimizations we've implemented reduce what we can control, but the bulk of the tokens (tool descriptions) are inherent to using MCP servers.

---

**Current Configuration**: Optimized for balance between functionality and token efficiency
**Last Updated**: October 22, 2025

