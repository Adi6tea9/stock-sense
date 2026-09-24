# Deployment Guide for Streamlit Cloud

## Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- API keys for at least one AI provider (OpenAI, Anthropic, Google Gemini, or local Ollama)

## Step 1: Push to GitHub

1. Make sure your code is committed:
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

2. Ensure your `.env` file is NOT pushed (it's already in `.gitignore`)

## Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `Agentic-AI-Stock-Analysis-Crew`
5. Set:
   - **Branch**: `main`
   - **Main file path**: `dashboard.py`
6. Click "Advanced settings"

## Step 3: Configure Secrets

In the "Secrets" section, paste your API keys in TOML format:

```toml
# Required: At least one AI provider API key
OPENAI_API_KEY = "sk-..."
# OR
ANTHROPIC_API_KEY = "sk-ant-..."
# OR
GEMINI_API_KEY = "..."

# Optional: Stock data API
ALPHA_VANTAGE_API_KEY = "..."

# Model Configuration
MODEL_PROVIDER = "openai/gpt-4o-mini"

# Logging
LOGGING_LEVEL = "INFO"
```

**Available Model Providers:**
- OpenAI: `openai/gpt-4o`, `openai/gpt-4o-mini`, `openai/gpt-3.5-turbo`
- Anthropic: `anthropic/claude-3-5-sonnet-20241022`, `anthropic/claude-3-haiku-20240307`
- Google: `gemini/gemini-1.5-pro-latest`, `gemini/gemini-1.5-flash`

## Step 4: Deploy

Click "Deploy!" and wait for the app to build and launch (typically 2-5 minutes).

## Updating Your App

After making changes:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud will automatically redeploy your app.

## Troubleshooting

### App won't start
- Check the logs in Streamlit Cloud dashboard
- Verify all required secrets are set
- Ensure at least one AI provider API key is valid

### API errors
- Check your API key is correct and has credits
- Try a different model provider in the dashboard
- View logs for specific error messages

### Performance issues
- Consider using a lighter model (e.g., `openai/gpt-4o-mini` or `gemini/gemini-1.5-flash`)
- Note: Free Streamlit Cloud apps sleep after inactivity

## Local Testing Before Deployment

Test locally to ensure everything works:
```bash
streamlit run dashboard.py
```

## Cost Considerations

- **Streamlit Cloud**: Free tier available (1 private app, 3 public apps)
- **API Costs**: 
  - OpenAI GPT-4o-mini: ~$0.15-0.60 per analysis
  - Gemini Flash: Free tier available
  - Anthropic Claude: Free tier available

## Security Notes

- Never commit `.env` file to GitHub
- Use Streamlit Cloud secrets for all sensitive data
- Rotate API keys regularly
- Monitor API usage to avoid unexpected charges
