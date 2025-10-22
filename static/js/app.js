// WebSocket connection
let ws = null;
let isConnected = false;

// DOM Elements
const queryInput = document.getElementById('queryInput');
const submitBtn = document.getElementById('submitBtn');
const clearBtn = document.getElementById('clearBtn');
const retryBtn = document.getElementById('retryBtn');
const responseSection = document.getElementById('responseSection');
const responseContent = document.getElementById('responseContent');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const toolsUsed = document.getElementById('toolsUsed');
const toolsList = document.getElementById('toolsList');
const statusDot = document.querySelector('.status-dot');
const statusText = document.querySelector('.status-text');
const exampleBtns = document.querySelectorAll('.example-btn');

// Initialize WebSocket connection
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        isConnected = true;
        updateStatus('connected', 'Connected');
        console.log('WebSocket connected');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateStatus('error', 'Connection Error');
    };
    
    ws.onclose = () => {
        isConnected = false;
        updateStatus('disconnected', 'Disconnected');
        console.log('WebSocket disconnected');
        
        // Attempt to reconnect after 3 seconds
        setTimeout(() => {
            if (!isConnected) {
                connectWebSocket();
            }
        }, 3000);
    };
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'connected':
            console.log('Server:', data.message);
            break;
            
        case 'processing':
            showLoading();
            break;
            
        case 'response':
            showResponse(data.data);
            break;
            
        case 'error':
            showError(data.message);
            break;
            
        default:
            console.log('Unknown message type:', data);
    }
}

// Update connection status
function updateStatus(status, text) {
    statusText.textContent = text;
    statusDot.className = 'status-dot';
    
    if (status === 'connected') {
        statusDot.style.background = 'var(--success)';
    } else if (status === 'error' || status === 'disconnected') {
        statusDot.style.background = 'var(--error)';
    } else {
        statusDot.style.background = 'var(--warning)';
    }
}

// Show loading state
function showLoading() {
    responseSection.style.display = 'none';
    errorState.style.display = 'none';
    loadingState.style.display = 'flex';
    submitBtn.disabled = true;
}

// Show response
function showResponse(data) {
    loadingState.style.display = 'none';
    errorState.style.display = 'none';
    responseSection.style.display = 'block';
    submitBtn.disabled = false;
    
    // Display response content
    responseContent.innerHTML = data.output;
    
    // Display tools used
    if (data.tools_used && data.tools_used.length > 0) {
        toolsUsed.style.display = 'block';
        toolsList.innerHTML = data.tools_used
            .map(tool => `<span class="tool-tag">${tool}</span>`)
            .join('');
    } else {
        toolsUsed.style.display = 'none';
    }
    
    // Scroll to response
    responseSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error
function showError(message) {
    loadingState.style.display = 'none';
    responseSection.style.display = 'none';
    errorState.style.display = 'flex';
    submitBtn.disabled = false;
    
    errorMessage.textContent = message;
}

// Submit query
function submitQuery() {
    const query = queryInput.value.trim();
    
    if (!query) {
        return;
    }
    
    if (!isConnected) {
        showError('Not connected to server. Please wait...');
        return;
    }
    
    try {
        ws.send(JSON.stringify({ query }));
    } catch (error) {
        showError('Failed to send query. Please try again.');
        console.error('Send error:', error);
    }
}

// Clear response and reset conversation
function clearResponse() {
    responseSection.style.display = 'none';
    errorState.style.display = 'none';
    queryInput.value = '';
    queryInput.focus();
    
    // Reconnect WebSocket to clear server-side history
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
        setTimeout(() => {
            connectWebSocket();
        }, 100);
    }
}

// Event Listeners
submitBtn.addEventListener('click', submitQuery);

queryInput.addEventListener('keydown', (e) => {
    // Submit on Enter (without Shift for new line)
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitQuery();
    }
});

clearBtn.addEventListener('click', clearResponse);

retryBtn.addEventListener('click', () => {
    errorState.style.display = 'none';
    submitQuery();
});

// Example query buttons
exampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        queryInput.value = query;
        queryInput.focus();
        
        // Auto-submit after a short delay
        setTimeout(() => {
            submitQuery();
        }, 300);
    });
});

// Initialize connection on page load
window.addEventListener('load', () => {
    connectWebSocket();
    queryInput.focus();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && !isConnected) {
        connectWebSocket();
    }
});

