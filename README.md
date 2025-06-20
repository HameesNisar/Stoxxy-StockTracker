<h1 align="center">📈 Stoxxy - Indian Stock Tracker</h1>

<p align="center">
  <em>A sleek, minimal stock price viewer for the Indian stock market — built with Flask, HTML, CSS, and JavaScript using the Alpha Vantage API.</em>
</p>

<hr>

<h2>🚀 About the Project</h2>
<p><strong>Stoxxy</strong> is a beginner-friendly web app that shows live stock prices of Indian stocks (e.g., <code>TCS.BSE</code>) with a recent history of searches. Built using <strong>Flask</strong> and <strong>Alpha Vantage API</strong>.</p>

<h2>🛠️ Features</h2>
<ul>
  <li>🔍 Real-time stock price lookup</li>
  <li>📊 Displays last searched stocks</li>
  <li>⚡ Minimalist UI with live updates</li>
  <li>🔐 API key stored securely via <code>.env</code></li>
</ul>

<h2>📂 Project Structure</h2>
<pre><code>Stoxxy-Stock-Tracker/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   ├── background.js
│   └── script.js
├── requirements.txt
└── .gitignore
</code></pre>

<h2>🔐 API Key Setup</h2>
<ol>
  <li>Get your API key from <a href="https://www.alphavantage.co/support/#api-key" target="_blank">Alpha Vantage</a></li>
  <li>Create a file named <code>.env</code> and add:<br><code>API_KEY=your_actual_key_here</code></li>
</ol>

<h2>💻 Run Locally</h2>
<pre><code>pip install -r requirements.txt
python app.py
</code></pre>

<h2>📜 License</h2>
<p>Free to use. Built for educational/demo purposes.</p>

<h2>🙌 Credits</h2>

Created with 💻 by **Hamees Nisar**.  
Built as part of a project — showcasing practical use of real-time APIs, secure coding practices, and clean UI design with Flask.


