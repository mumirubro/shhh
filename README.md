# 🛒 Shopify Card Checker API

Complete REST API for checking card validity through Shopify checkout with proxy rotation support.

**Ready for Render Free Plan Deployment!**

---

## 🚀 Full A-to-Z Render Deployment Guide

Follow these steps **exactly** to deploy your API:

### Step 1: Download All Files

1. Download ALL files from this project to your computer
2. Make sure you have these files:
   - `app.py`
   - `shopify_auto_checkout.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `pyproject.toml`
   - `.gitignore`
   - `README.md`
   - `API_USAGE.md`

---

### Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the **"+"** button (top right) → **"New repository"**
3. Repository settings:
   - **Name**: `shopify-checker-api` (or any name you want)
   - **Visibility**: Choose **Private** (recommended) or Public
   - **DO NOT** check "Initialize with README"
4. Click **"Create repository"**

---

### Step 3: Upload Files to GitHub

**Option A: Using GitHub Website (Easier)**

1. On your new repository page, click **"uploading an existing file"**
2. Drag and drop ALL the files you downloaded
3. Scroll down and click **"Commit changes"**

**Option B: Using Git Commands**

```bash
cd your-project-folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shopify-checker-api.git
git push -u origin main
```

---

### Step 4: Sign Up for Render

1. Go to [Render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up using:
   - **GitHub** (Recommended - easiest)
   - Or Email
4. Complete the sign-up process

---

### Step 5: Connect GitHub to Render

1. In Render dashboard, you'll be asked to connect GitHub
2. Click **"Connect GitHub"**
3. Authorize Render to access your GitHub
4. Select **"All repositories"** or **"Only select repositories"**
5. If selecting specific repos, choose your `shopify-checker-api` repository

---

### Step 6: Create New Web Service

1. In Render dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories
4. Find your `shopify-checker-api` repository
5. Click **"Connect"** next to it

---

### Step 7: Configure Your Web Service

Fill in these settings **EXACTLY**:

**Basic Settings:**
- **Name**: `shopify-checker` (or any name - this will be part of your URL)
- **Region**: Choose closest to you:
  - `Oregon (US West)`
  - `Ohio (US East)`
  - `Frankfurt (Europe)`
  - `Singapore (Asia)`
- **Branch**: `main` (or whatever your default branch is)
- **Root Directory**: Leave **EMPTY**
- **Runtime**: `Python 3`

**Build Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Plan:**
- Select **"Free"** plan (Scroll down to find it!)
  - Free plan gives you 750 hours/month
  - App sleeps after 15 min of inactivity
  - Perfect for testing and personal use

---

### Step 8: Advanced Settings (Optional but Recommended)

Click **"Advanced"** to expand advanced settings:

**Environment Variables** (Optional - add proxies or default URL):

Click **"Add Environment Variable"** and add:

1. **For Proxies** (if you have proxies):
   - **Key**: `PROXIES`
   - **Value**: `http://user:pass@proxy1.com:8080,http://user:pass@proxy2.com:8080`
   - *(Separate multiple proxies with commas)*

2. **For Default Shopify URL** (if you want a default site):
   - **Key**: `DEFAULT_SHOPIFY_URL`
   - **Value**: `https://your-shop.myshopify.com`

**Auto-Deploy**: Leave as **Yes** (recommended)

---

### Step 9: Deploy!

1. Click **"Create Web Service"** button at the bottom
2. Render will now:
   - Clone your GitHub repository
   - Install Python dependencies
   - Start your application
3. **Wait 2-5 minutes** for first deployment
4. Watch the logs to see progress

---

### Step 10: Get Your API URL

1. Once deployment is complete, you'll see **"Live ✓"** with a green checkmark
2. Your API URL will be shown at the top:
   ```
   https://shopify-checker.onrender.com
   ```
   (Your actual URL will be different based on the name you chose)

3. **Copy this URL** - this is your API base URL!

---

### Step 11: Test Your API

Open your browser and paste:

```
https://your-app-name.onrender.com/
```

You should see:

```json
{
  "status": "online",
  "message": "🛒 Shopify Card Checker API",
  "version": "2.0",
  "endpoints": { ... }
}
```

**If you see this - SUCCESS! Your API is live! 🎉**

---

## 📡 How to Use Your API

Now that your API is deployed, here's how to use it:

### Quick Start - Card Check

Replace `your-app-name.onrender.com` with your actual URL:

```
https://your-app-name.onrender.com/shopify.py?lista=https://shop.myshopify.com|4532123456789012|12|25|123
```

Just paste this in your browser and hit Enter!

---

## 📚 All Available Endpoints

### 🎯 Card Checking

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `/shopify.py` | Main card check | `/shopify.py?lista={site}\|{cc}` |
| `/sh` | Single card | `/sh?lista={site}\|{cc}` |
| `/msh` | Multiple cards | `/msh?cards={cc1},{cc2}&site={url}` |

### 🔧 URL Management

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `/seturl` | Set global URL | `/seturl?url=https://shop.com` |
| `/myurl` | Show current URL | `/myurl` |
| `/rmurl` | Remove URL | `/rmurl` |

### 🔌 Proxy Management

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `/addp` | Add proxy | `/addp?proxy=http://user:pass@ip:port` |
| `/rp` | Remove proxy | `/rp?index=1` or `/rp` (remove all) |
| `/lp` | List proxies | `/lp` |
| `/cp` | Check proxy | `/cp` |

### 🧪 Site Testing

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `/chkurl` | Test one site | `/chkurl?url=https://shop.com` |
| `/mchku` | Test multiple sites | `/mchku?urls=shop1.com,shop2.com` |

### 📊 Info

| Endpoint | Purpose |
|----------|---------|
| `/` | API info & all endpoints |
| `/health` | Health check |

---

## 💡 Complete Usage Examples

### Example 1: Basic Card Check (No Setup)

```
https://your-app.onrender.com/shopify.py?lista=https://goddess-creations-8093.myshopify.com|4532123456789012|12|25|123
```

**Response**:
```json
{
  "status": "LIVE",
  "card": "4532123456789012|12|25|123",
  "response": "Approved",
  "bin": "453212",
  "brand": "VISA",
  "type": "CREDIT",
  "country": "🇺🇸 United States",
  "bank": "Chase Bank",
  "price": "$1.00",
  "time": "2.45s",
  "proxy": "No Proxy"
}
```

---

### Example 2: Set Global URL, Then Check Cards

**Step 1**: Set global URL
```
https://your-app.onrender.com/seturl?url=https://goddess-creations-8093.myshopify.com
```

**Step 2**: Now check cards without specifying site
```
https://your-app.onrender.com/sh?lista=4532123456789012|12|25|123
```

**Step 3**: Check multiple cards
```
https://your-app.onrender.com/msh?cards=4532123456789012|12|25|123,4556789012345678|01|26|456
```

---

### Example 3: Add and Use Proxies

**Step 1**: Add proxy
```
https://your-app.onrender.com/addp?proxy=http://user:pass@proxy.com:8080
```

**Step 2**: List proxies to confirm
```
https://your-app.onrender.com/lp
```

**Step 3**: Check proxy status
```
https://your-app.onrender.com/cp
```

**Step 4**: All card checks now use proxies automatically!

---

### Example 4: Find Working Shopify Sites

**Test multiple sites**:
```
https://your-app.onrender.com/mchku?urls=https://shop1.com,https://shop2.com,https://shop3.com
```

**Test single site**:
```
https://your-app.onrender.com/chkurl?url=https://goddess-creations-8093.myshopify.com
```

---

## 🔧 Advanced Configuration

### Adding Permanent Proxies in Render

1. Go to your service in Render dashboard
2. Click **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `PROXIES`
   - **Value**: `http://user:pass@proxy1.com:8080,http://user:pass@proxy2.com:8080,http://user:pass@proxy3.com:8080`
   *(Separate multiple proxies with commas, no spaces)*
5. Click **"Save Changes"**
6. App will auto-redeploy with proxies

### Adding Default Shopify URL

1. Same steps as above, but add:
   - **Key**: `DEFAULT_SHOPIFY_URL`
   - **Value**: `https://your-shop.myshopify.com`

---

## 📖 Detailed API Documentation

For complete API documentation with all parameters and responses, see:

**[API_USAGE.md](API_USAGE.md)** - Full documentation with examples for every endpoint

---

## ⚠️ Important Notes

### Render Free Plan Limitations

- **Sleep After Inactivity**: App sleeps after 15 minutes of no requests
- **Wake-Up Time**: First request after sleep takes 30-50 seconds
- **After Wake-Up**: Subsequent requests are fast
- **Monthly Limit**: 750 hours/month (plenty for personal use)
- **Storage**: Ephemeral (runtime settings reset on restart)

### Settings Persistence

**Runtime Settings** (via API endpoints like `/seturl`, `/addp`):
- ❌ **NOT persistent** - reset when app restarts
- ✅ Good for testing and temporary use

**Environment Variables** (set in Render dashboard):
- ✅ **Persistent** - stay after restart
- ✅ Recommended for proxies and default URL

---

## 🔄 Updating Your API

### Method 1: Push to GitHub (Automatic)

1. Update your code files locally
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update API"
   git push
   ```
3. Render auto-deploys the changes (if auto-deploy is enabled)

### Method 2: Manual Deploy in Render

1. Go to your service in Render
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🐛 Troubleshooting

### Problem: API shows "Application Failed"

**Solution**:
1. Check Render logs (click "Logs" tab)
2. Make sure all files are uploaded to GitHub
3. Verify `requirements.txt` and `Procfile` exist
4. Try manual redeploy

### Problem: First request is very slow

**Solution**: This is normal on free plan! The app sleeps after 15 min of inactivity. First request wakes it up (30-50 seconds), then it's fast.

### Problem: Settings (URL/proxies) disappeared

**Solution**: Runtime settings reset when app restarts. Use environment variables in Render dashboard for permanent settings.

### Problem: Getting rate limited by Shopify

**Solution**: Add proxies using `/addp` endpoint or `PROXIES` environment variable

---

## 📊 API Response Statuses

- **LIVE** ✅ - Card approved/valid
- **DEAD** ❌ - Card declined/invalid
- **ERROR** ⚠️ - System error occurred

---

## 🔐 Security Notes

- ⚠️ API is **public by default** (no authentication)
- 🔒 Don't share your deployment URL publicly if you don't want others to use it
- 🔑 Consider adding API keys for production use (requires code modification)
- 🔐 Keep your proxy credentials safe

---

## 💰 Cost

**Free Plan**: $0/month
- 750 hours/month
- Sleeps after 15 min inactivity
- Perfect for personal use and testing

**Paid Plan** (if you need always-on service): $7/month
- Never sleeps
- Always fast
- More resources

---

## 📝 Files Included

- `app.py` - Main Flask application
- `shopify_auto_checkout.py` - Card checking logic
- `requirements.txt` - Python dependencies
- `Procfile` - Render deployment config
- `runtime.txt` - Python version (3.11.0)
- `pyproject.toml` - Project metadata
- `.gitignore` - Git ignore rules
- `README.md` - This file
- `API_USAGE.md` - Complete API documentation

---

## 🎯 Quick Reference Card

**Your API URL Format**:
```
https://YOUR-APP-NAME.onrender.com/ENDPOINT?PARAMETERS
```

**Most Used Endpoints**:
```
/shopify.py?lista={site}|{card}|{month}|{year}|{cvv}
/sh?lista={card}|{month}|{year}|{cvv}  (needs global URL)
/msh?cards={cc1},{cc2}&site={url}
/seturl?url={shopify_url}
/addp?proxy={proxy_url}
```

---

## ✅ Deployment Checklist

- [ ] All files downloaded
- [ ] GitHub repository created
- [ ] Files uploaded to GitHub
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Web service created
- [ ] Settings configured correctly
- [ ] App deployed successfully
- [ ] API tested and working
- [ ] Environment variables added (if using proxies)

---

## 🆘 Need Help?

1. **Check Logs**: In Render dashboard → "Logs" tab
2. **Review API_USAGE.md**: Complete documentation for all endpoints
3. **Test Health**: Visit `https://your-app.onrender.com/health`
4. **Verify Files**: Make sure all files are in GitHub repo

---

## 🎉 You're Ready!

Your Shopify Card Checker API is now live and ready to use!

**Next Steps**:
1. Copy your API URL from Render
2. Test the endpoints using examples above
3. Check API_USAGE.md for detailed documentation
4. Add proxies if needed
5. Start checking cards!

---

**Built for Render Free Plan | Production Ready | Easy to Deploy**
