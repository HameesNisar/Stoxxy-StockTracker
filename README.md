# 📈 Stoxxy - Indian Stock Tracker

<p align="center">
  <em>A sleek, minimal stock price viewer for the Indian stock market — built with Flask, HTML, CSS, and JavaScript using NSE and Yahoo Finance APIs.</em><br>
  <a href="https://stoxxy-stocktracker.onrender.com/">🌐 Live Demo</a>
</p>

---

## 🚀 About the Project

**Stoxxy** is a beginner-friendly web app that shows live stock prices of Indian companies (e.g., `TCS`, `RELIANCE`, `INFY`).  
Built using **Flask**, it first tries to fetch data from the **official NSE API**, and falls back to **Yahoo Finance** if needed.

### ✨ Key Highlights

- 🎯 **No API Key Required** – Uses free public APIs  
- 🔄 **Smart Fallback System** – NSE → Yahoo Finance → BSE  
- 📱 **Mobile Responsive** – Works on all devices  
- ⚡ **Fast & Lightweight** – Minimal dependencies  

---

## 🛠️ Features

- 🔍 Real-time stock price lookup using NSE India API  
- 📉 Yahoo Finance fallback for reliability  
- 📊 Recent search history (client-side storage via `localStorage`)  
- 🎨 Animated background with interactive squares  
- ⚡ Minimalist, mobile-responsive UI  
- 🔐 Secure environment variable support via `.env`  

---

## 📂 Project Structure

```
Stoxxy-Stock-Tracker/
├── app.py                 # Flask backend with API endpoints
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── style.css          # Glassmorphism UI styles
│   ├── background.js      # Animated squares background
│   └── script.js          # Frontend logic & API calls
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (optional)
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Stoxxy-Stock-Tracker.git
cd Stoxxy-Stock-Tracker

# Install dependencies
pip install -r requirements.txt
```

---

## 🔧 API Configuration

The app uses:

- 🟢 **NSE India API** – Primary source  
- 🟡 **Yahoo Finance API** – Backup (`.NS` suffix)  
- 🔵 **Yahoo Finance BSE** – Backup fallback (`.BO` suffix)  

---

## 📈 Supported Stock Symbols

Try these popular Indian stocks:

- `TCS` – Tata Consultancy Services  
- `RELIANCE` – Reliance Industries  
- `INFY` – Infosys  
- `HDFCBANK` – HDFC Bank  
- `ICICIBANK` – ICICI Bank  
- `BHARTIARTL` – Bharti Airtel  
- `SBIN` – State Bank of India  

---

## 🎨 UI Features

- 🧊 Glassmorphism Design – Modern frosted glass effect  
- 🧠 Animated Background – Interactive moving squares  
- 📱 Responsive Layout – Works on desktop and mobile  
- 📈 Real-time Updates – Live stock price changes  
- 🕓 Search History – Recent searches saved locally  

---

## 🔧 Technical Details

- **Backend:** Flask (Python)  
- **Frontend:** Vanilla JavaScript, HTML5, CSS3  
- **APIs:** NSE India, Yahoo Finance  
- **Styling:** Custom CSS with glassmorphism effects  
- **Animation:** Canvas-based background animation  
- **Storage:** `localStorage` for search history  

---

## 📝 License

This project is open source and available under the **MIT License**.

---

## 🙌 Credits

Created with 💻 by **Hamees Nisar**

This project showcases:

- Practical use of live public APIs  
- Fallback strategies for API reliability  
- Secure coding practices  
- Clean UI design using Flask  
- Modern web development techniques  

---

<p align="center">
  <strong>⭐ Star this repo if you found it helpful!</strong>
</p>
