// Generate unique user ID for per-user history
function getUserId() {
    let userId = localStorage.getItem('stoxiee_user_id');
    if (!userId) {
        userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('stoxiee_user_id', userId);
    }
    return userId;
}

// Client-side history management with user-specific storage
const USER_ID = getUserId();
const HISTORY_KEY = `stoxiee_history_${USER_ID}`;
const MAX_HISTORY = 5;

function getHistory() {
    try {
        const stored = localStorage.getItem(HISTORY_KEY);
        return stored ? JSON.parse(stored) : [];
    } catch (e) {
        console.error('Error reading history:', e);
        return [];
    }
}

function saveHistory(history) {
    try {
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    } catch (e) {
        console.error('Error saving history:', e);
    }
}

function addToHistory(stockInfo) {
    let history = getHistory();
    
    // Remove if already exists to avoid duplicates
    history = history.filter(item => item.symbol !== stockInfo.symbol);
    
    // Add to beginning
    history.unshift(stockInfo);
    
    // Keep only max items
    if (history.length > MAX_HISTORY) {
        history = history.slice(0, MAX_HISTORY);
    }
    
    saveHistory(history);
    updateHistoryDisplay();
}

function updateHistoryDisplay() {
    const history = getHistory();
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';
    
    if (history.length === 0) {
        historyList.innerHTML = '<div class="no-history">No searches yet</div>';
        return;
    }
    
    history.forEach(stock => {
        const item = document.createElement('div');
        item.className = 'history-item';
        
        const changeText = stock.change >= 0 ? `+₹${stock.change}` : `-₹${Math.abs(stock.change)}`;
        
        item.innerHTML = `
            <span class="stock-symbol">${stock.symbol}</span>
            <span class="stock-price">₹${stock.price}</span>
            <span class="stock-change ${stock.direction}">${changeText}</span>
        `;
        
        // Add click functionality to search again
        item.style.cursor = 'pointer';
        item.addEventListener('click', () => {
            document.getElementById('stockInput').value = stock.symbol;
            searchStock();
        });
        
        historyList.appendChild(item);
    });
}

function searchStock() {
    const symbol = document.getElementById('stockInput').value.trim().toUpperCase();
    const result = document.getElementById('result');
    
    if (!symbol) {
        showResult('Please enter a stock symbol', 'error');
        return;
    }
    
    showResult('<div class="loading-spinner"></div>Searching...', 'loading');
    
    fetch(`/api/stock?symbol=${symbol}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showResult(data.error, 'error');
            } else {
                const changeText = data.change >= 0 ? `+₹${data.change}` : `-₹${Math.abs(data.change)}`;
                const arrow = data.direction === 'up' ? '📈' : '📉';
                showResult(`${data.symbol}: ₹${data.price} ${arrow} ${changeText}`, 'success');
                
                // Add to history
                addToHistory(data);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            showResult('Failed to fetch stock data. Please check your connection and try again.', 'error');
        });
}

function showResult(message, type) {
    const result = document.getElementById('result');
    result.innerHTML = message;
    result.className = type;
}

// Clear history function (optional - you can add a button for this)
function clearHistory() {
    localStorage.removeItem(HISTORY_KEY);
    updateHistoryDisplay();
}

// Allow Enter key to search
document.getElementById('stockInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchStock();
    }
});

// Load history on page load
document.addEventListener('DOMContentLoaded', () => {
    updateHistoryDisplay();
});
