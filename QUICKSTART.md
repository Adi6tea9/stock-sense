# Stock Sense - Quick Start Guide

## 🎉 Project Successfully Created!

Your AI Stock Analysis Dashboard is ready in the `stock-sense` folder.

---

## 📁 Project Structure

```
stock-sense/
├── dashboard.py              # Main Streamlit app
├── market_analysis_crew.py   # AI agents implementation
├── financial_tools.py        # Stock data tools
├── requirements.txt          # Python dependencies
├── .env                      # Your API keys (DO NOT share!)
├── .env.example             # Template for others
├── .streamlit/              # Streamlit configuration
│   ├── config.toml          # App settings
│   └── secrets.toml.example # Secrets template
├── DEPLOYMENT.md            # Full deployment guide
└── README.md                # Project documentation

```

---

## 🚀 Quick Start

### Run Locally
```bash
cd stock-sense
streamlit run dashboard.py
```
App will open at: http://localhost:8501

---

## ☁️ Deploy to Streamlit Cloud

### Step 1: Create GitHub Repository
```bash
cd stock-sense
git remote add origin https://github.com/YOUR_USERNAME/stock-sense.git
git push -u origin master
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `YOUR_USERNAME/stock-sense`
   - Branch: `master`
   - Main file: `dashboard.py`

### Step 3: Add Secrets
Click "Advanced settings" → "Secrets", then paste:

```toml
OPENAI_API_KEY = "sk-proj-..."
GEMINI_API_KEY = "AIzaSy..."
MODEL_PROVIDER = "gemini/gemini-1.5-pro-latest"
LOGGING_LEVEL = "INFO"
```

### Step 4: Deploy!
Click "Deploy" and wait 2-5 minutes.

---

## 🔑 Your API Keys

You currently have configured:
- ✅ OpenAI API Key
- ✅ Google Gemini API Key
- ⚠️ Model: gemini/gemini-1.5-pro-latest (free tier available)

**Never commit your `.env` file!** (Already in `.gitignore`)

---

## 🤖 Available AI Models

| Provider | Model | Cost |
|----------|-------|------|
| OpenAI | gpt-4o-mini | ~$0.15-0.60/analysis |
| Google | gemini-1.5-pro | Free tier available |
| Google | gemini-1.5-flash | Free tier available |
| Anthropic | claude-3-5-sonnet | Free tier available |

---

## 📊 Features

- **Multi-Agent Analysis**: 5 specialized AI agents
  - Market Intelligence Officer
  - Technical Analysis Specialist
  - Fundamental Analysis Expert
  - Risk Management Specialist
  - Portfolio Strategy Expert

- **Real-time Data**: Live stock prices via yfinance
- **Interactive Charts**: Candlestick, RSI, MACD, Volume
- **Risk Metrics**: VaR, Sharpe Ratio, Beta
- **Investment Terms**: Built-in glossary

---

## 🛠️ Troubleshooting

### App won't start locally
```bash
pip install -r requirements.txt
```

### Missing API key error
Check your `.env` file has at least one valid API key

### Streamlit Cloud deployment fails
- Verify secrets are in TOML format
- Check logs in Streamlit Cloud dashboard
- Ensure repository is public or you have paid Streamlit plan

---

## 📚 Resources

- Full deployment guide: `DEPLOYMENT.md`
- Project README: `README.md`
- Streamlit docs: https://docs.streamlit.io
- CrewAI docs: https://docs.crewai.com

---

## 🎯 Next Steps

1. **Test locally**: `streamlit run dashboard.py`
2. **Create GitHub repo** for your account
3. **Deploy to Streamlit Cloud**
4. **Share your app** with the world!

---

**Created:** September 24, 2026
**Location:** C:\Users\adity\OneDrive\Desktop\summer report\stock-sense
