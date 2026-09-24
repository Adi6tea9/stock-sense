# Deploying to Render

This guide will help you deploy your AI Stock Analysis Dashboard to Render.

## Prerequisites

- A Render account (free at [render.com](https://render.com))
- Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)
- API keys for at least one AI provider

## Step 1: Prepare Your Repository

### Option A: Fork and Push to Your Own GitHub
1. Fork the repository at https://github.com/ebrown-32/Agentic-AI-Stock-Analysis-Crew
2. Clone your fork locally
3. Update the remote:
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/Agentic-AI-Stock-Analysis-Crew.git
   git push origin main
   ```

### Option B: Create a New Repository
1. Create a new repository on GitHub
2. Update the remote and push:
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## Step 2: Deploy on Render

### Using render.yaml (Recommended)

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub/GitLab account if not already connected
4. Select your repository: `Agentic-AI-Stock-Analysis-Crew`
5. Render will automatically detect the `render.yaml` file
6. Click **"Apply"**

### Manual Setup (Alternative)

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Configure:
   - **Name**: `agentic-stock-analysis`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Instance Type**: `Free`

## Step 3: Configure Environment Variables

In the Render dashboard, add these environment variables:

### Required (choose at least one AI provider):

```
OPENAI_API_KEY=your_openai_key_here
```
OR
```
ANTHROPIC_API_KEY=your_anthropic_key_here
```
OR
```
GEMINI_API_KEY=your_gemini_key_here
```

### Optional but Recommended:

```
MODEL_PROVIDER=gemini/gemini-1.5-flash
LOGGING_LEVEL=INFO
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### Additional Streamlit Configuration:

```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Step 4: Deploy

1. Click **"Create Web Service"** (or **"Apply"** for Blueprint)
2. Render will automatically build and deploy your app (takes 5-10 minutes)
3. Once deployed, you'll get a URL like: `https://agentic-stock-analysis.onrender.com`

## Step 5: Verify Deployment

1. Visit your Render URL
2. Test the app by analyzing a stock (e.g., AAPL)
3. Check the logs in Render dashboard if you encounter any issues

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect the push and redeploy your app.

## Troubleshooting

### Build Fails

- Check the build logs in Render dashboard
- Verify all dependencies in `requirements.txt` are compatible
- Ensure `runtime.txt` specifies a supported Python version (3.11.0)

### App Crashes on Start

- Check that at least one AI provider API key is set
- View the service logs in Render dashboard
- Verify the start command is correct

### API Errors

- Confirm your API keys are valid and have available credits
- Check API rate limits (free tiers have restrictions)
- Try switching to a different AI provider in the dashboard

### Performance Issues

- Free tier apps sleep after 15 minutes of inactivity
- First request after sleeping takes ~30 seconds to wake up
- Consider upgrading to a paid plan ($7/month) for always-on service

## Cost Considerations

### Render
- **Free Tier**: 750 hours/month (enough for 1 app running 24/7)
- **Paid Plan**: $7/month for always-on, faster instances
- **Automatic sleep**: Free apps sleep after 15 min inactivity

### AI API Costs (per analysis)
- **OpenAI GPT-4o-mini**: ~$0.15-0.60
- **Google Gemini Flash**: Free tier available (60 requests/minute)
- **Anthropic Claude**: Pay-as-you-go pricing

**Recommendation**: Start with Google Gemini (free tier) on Render's free plan.

## Security Best Practices

✅ Never commit `.env` file to Git (already in `.gitignore`)  
✅ Use Render's environment variables for all secrets  
✅ Rotate API keys regularly  
✅ Monitor API usage to avoid unexpected charges  
✅ Enable 2FA on your Render account  

## Getting API Keys (Free Options)

- **OpenAI**: [$5 free credits](https://platform.openai.com/signup)
- **Anthropic**: [Free tier](https://console.anthropic.com/)
- **Google Gemini**: [Free API key](https://makersuite.google.com/app/apikey)
- **Alpha Vantage**: [Free tier](https://www.alphavantage.co/support/#api-key)

## Support

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Project Issues**: Open an issue on your GitHub repository

---

**Note**: This is an educational project. Always conduct your own research and consult financial advisors before making investment decisions.
