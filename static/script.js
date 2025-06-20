function searchStock() {
    const symbol = document.getElementById('stockInput').value.trim().toUpperCase();
    const result = document.getElementById('result');
    
    if (!symbol) {
        showResult('Please enter a stock symbol', 'error');
        return;
    }
    
    showResult('Loading...', 'loading');
    
    fetch(`/api/stock?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showResult(data.error, 'error');
            } else {
                const changeText = data.change >= 0 ? `+₹${data.change}` : `-₹${Math.abs(data.change)}`;
                const arrow = data.direction === 'up' ? '↗️' : '↘️';
                showResult(`${data.symbol}: ₹${data.price} ${arrow} ${changeText}`, 'success');
                updateHistory();
            }
        })
        .catch(error => {
            showResult('Failed to fetch stock data', 'error');
        });
}

function showResult(message, type) {
    const result = document.getElementById('result');
    result.textContent = message;
    result.className = type;
}

function updateHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(history => {
            const historyList = document.getElementById('historyList');
            historyList.innerHTML = '';
            
            if (history.length === 0) {
                historyList.innerHTML = '<p style="text-align: center; color: #6c757d;">No searches yet</p>';
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
                
                historyList.appendChild(item);
            });
        });
}

// Allow Enter key to search
document.getElementById('stockInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchStock();
    }
});

// Load history on page load
document.addEventListener('DOMContentLoaded', updateHistory);
