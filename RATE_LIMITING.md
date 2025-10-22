# Rate Limiting Guide

## 🚦 Why Rate Limiting?

The Anthropic API has rate limits to prevent abuse and ensure fair usage:
- **Your current limit**: 30,000 input tokens per minute
- **Typical query**: Uses 5,000-15,000 tokens (including context)
- **Problem**: Multiple rapid queries can exceed this limit

## ✅ Solution Implemented

### Application-Level Rate Limiting
The app now limits you to **3 queries per minute** to prevent hitting the API rate limit.

### Features Added:

1. **Rate Limit Check**: Before each query, the app checks if you're within limits
2. **User-Friendly Messages**: Clear error messages if you hit the limit
3. **Visual Warning**: Yellow notice bar showing the rate limit
4. **Timeout Protection**: 60-second timeout for long-running queries
5. **Better Error Handling**: Specific messages for different error types

## 📊 Current Settings

```python
# In app.py
rate_limiter = RateLimiter(
    max_requests=3,      # Maximum 3 queries
    time_window=60       # Per 60 seconds (1 minute)
)
```

## 🔧 Adjusting Rate Limits

### To Increase Queries Per Minute

Edit `app.py` line 40:

```python
# For 5 queries per minute
rate_limiter = RateLimiter(max_requests=5, time_window=60)

# For 10 queries per 2 minutes
rate_limiter = RateLimiter(max_requests=10, time_window=120)
```

### To Disable Rate Limiting (Not Recommended)

Comment out the rate limit check in `app.py` (lines 119-126):

```python
# # Check rate limit
# can_proceed, wait_time = await rate_limiter.acquire()
# if not can_proceed:
#     await websocket.send_json({
#         "type": "error",
#         "message": f"Rate limit exceeded..."
#     })
#     continue
```

**Warning**: Disabling may cause API errors!

## 💡 Best Practices

### 1. Keep Queries Simple
❌ Bad: "Compare all tech stocks, analyze their financials, get news sentiment, and predict future performance"
✅ Good: "What is the latest price of Apple?"

### 2. Wait Between Queries
- After 3 queries, wait 60 seconds
- The app will tell you how long to wait

### 3. Use Specific Queries
❌ Bad: "Tell me everything about the market"
✅ Good: "What is Tesla's current stock price?"

### 4. Avoid Rapid-Fire Testing
- Don't spam the submit button
- Wait for responses before sending new queries

## 🔍 Understanding Token Usage

### What Counts as Tokens?
- Your query text
- Conversation history (previous messages)
- System prompts
- Tool descriptions (from MCP server)
- API responses

### Example Token Counts:
- Simple query: ~5,000 tokens
- Complex query with history: ~15,000 tokens
- Multiple tool calls: ~20,000+ tokens

### Why You Hit the Limit:
If you make 3 complex queries quickly:
- Query 1: 15,000 tokens
- Query 2: 15,000 tokens (includes history)
- Query 3: 20,000 tokens (more history)
- **Total**: 50,000 tokens → **Exceeds 30,000/min limit!**

## 🚀 Solutions for Heavy Usage

### Option 1: Upgrade Your Anthropic Plan
Contact Anthropic sales to increase your rate limit:
- https://www.anthropic.com/contact-sales
- Request higher tokens per minute
- Usually approved for legitimate use cases

### Option 2: Clear Conversation History
The app keeps conversation history for context. To reduce token usage:
- Click "Clear" button after each query
- This removes history but loses context

### Option 3: Use Simpler Queries
- Break complex questions into smaller parts
- Ask one thing at a time
- Avoid asking for multiple comparisons

### Option 4: Implement Caching
For advanced users, implement response caching:
- Cache common queries
- Reuse results for similar questions
- Reduces API calls

## 📈 Monitoring Usage

### Check Your Anthropic Dashboard
1. Go to https://console.anthropic.com
2. View "Usage" section
3. See your rate limit status

### Watch for These Signs:
- Queries taking longer than usual
- "Rate limit" error messages
- 429 status codes in logs

## 🔄 What Happens When You Hit the Limit?

### Application Response:
1. Shows error message: "Rate limit exceeded"
2. Tells you how long to wait
3. Prevents the query from being sent

### API Response (if it gets through):
```
status_code: 429
error: rate_limit_error
message: "This request would exceed the rate limit..."
```

## ⚙️ Technical Details

### Rate Limiter Implementation
```python
class RateLimiter:
    def __init__(self, max_requests=5, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    async def acquire(self):
        now = time.time()
        # Remove old requests outside time window
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        # Check if under limit
        if len(self.requests) >= self.max_requests:
            wait_time = self.requests[0] + self.time_window - now
            if wait_time > 0:
                return False, wait_time
        
        self.requests.append(now)
        return True, 0
```

### Error Handling
```python
except Exception as e:
    error_msg = str(e)
    if "rate_limit_error" in error_msg or "429" in error_msg:
        # Show user-friendly rate limit message
        await websocket.send_json({
            "type": "error",
            "message": "API rate limit exceeded. Please wait..."
        })
```

## 🎯 Recommendations

### For Development/Testing:
- Keep rate limit at 3 queries/minute
- Clear history between tests
- Use simple test queries

### For Production:
- Monitor actual usage patterns
- Adjust rate limit based on user needs
- Consider implementing user-specific limits
- Add authentication to prevent abuse

### For High-Volume Use:
1. Upgrade Anthropic plan
2. Implement caching
3. Use queue system for queries
4. Consider batch processing

## 📞 Getting Help

### Rate Limit Increase:
- Email: sales@anthropic.com
- Explain your use case
- Mention expected query volume

### Technical Issues:
- Check Railway logs: `railway logs`
- Review browser console (F12)
- Check Anthropic status page

## 📝 Summary

✅ **What's Fixed**:
- Application-level rate limiting (3/min)
- Better error messages
- Visual warning indicator
- Timeout protection

⚠️ **What to Remember**:
- Wait between queries
- Keep queries simple
- Clear history when needed
- Monitor your usage

🚀 **For More Queries**:
- Upgrade your Anthropic plan
- Adjust rate limiter settings
- Implement caching

---

**Current Status**: Rate limiting active at 3 queries/minute
**Last Updated**: October 22, 2025

