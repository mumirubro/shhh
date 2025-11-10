# 📡 Shopify Card Checker API - Complete Usage Guide

**Base URL**: `https://your-app-name.onrender.com`

---

## 🎯 Quick Start

Replace `https://your-app-name.onrender.com` with your actual Render URL in all examples below.

---

## 📌 Card Checking Endpoints

### 1. `/shopify.py` - Main Card Check Endpoint

**Purpose**: Check a single card with site URL included

**Method**: `GET`

**Format**:
```
/shopify.py?lista={site}|{card}|{month}|{year}|{cvv}
```

**Example**:
```
https://your-app.onrender.com/shopify.py?lista=https://shop.myshopify.com|4532123456789012|12|25|123
```

**Response**:
```json
{
  "status": "LIVE",
  "card": "4532123456789012|12|25|123",
  "response": "Approved",
  "reason_type": "N/A",
  "bin": "453212",
  "brand": "VISA",
  "type": "CREDIT",
  "country": "🇺🇸 United States",
  "bank": "Example Bank",
  "price": "$1.00",
  "time": "2.45s",
  "proxy": "No Proxy"
}
```

---

### 2. `/sh` - Single Card Check

**Purpose**: Check one card (can use global URL or specify site)

**Method**: `GET`

**Format** (with site):
```
/sh?lista={site}|{card}|{month}|{year}|{cvv}
```

**Format** (with global URL):
```
/sh?lista={card}|{month}|{year}|{cvv}
```

**Example 1** (with site):
```
https://your-app.onrender.com/sh?lista=https://shop.myshopify.com|4532123456789012|12|25|123
```

**Example 2** (using global URL set via `/seturl`):
```
https://your-app.onrender.com/sh?lista=4532123456789012|12|25|123
```

**Response**: Same as `/shopify.py`

---

### 3. `/msh` - Multiple Cards Check

**Purpose**: Check up to 10 cards at once

**Method**: `GET`

**Format**:
```
/msh?cards={cc1},{cc2},{cc3}&site={shopify_url}
```

**Card Format**: `{card}|{month}|{year}|{cvv}`

**Example**:
```
https://your-app.onrender.com/msh?cards=4532123456789012|12|25|123,4556789012345678|01|26|456&site=https://shop.myshopify.com
```

**Can also use global URL** (set via `/seturl`):
```
https://your-app.onrender.com/msh?cards=4532|12|25|123,4556|01|26|456
```

**Response**:
```json
{
  "status": "success",
  "total_cards": 2,
  "total_time": "5.32s",
  "site": "https://shop.myshopify.com",
  "results": [
    {
      "index": 1,
      "status": "LIVE",
      "card": "4532123456789012|12|25|123",
      "response": "Approved",
      "bin": "453212",
      "brand": "VISA",
      "price": "$1.00",
      "time": "2.45s"
    },
    {
      "index": 2,
      "status": "DEAD",
      "card": "4556789012345678|01|26|456",
      "response": "Declined",
      "time": "2.87s"
    }
  ]
}
```

---

## 🔧 URL Management Endpoints

### 4. `/seturl` - Set Global Shopify URL

**Purpose**: Set a default Shopify site for all checks

**Method**: `GET`

**Format**:
```
/seturl?url={shopify_url}
```

**Example**:
```
https://your-app.onrender.com/seturl?url=https://shop.myshopify.com
```

**Response**:
```json
{
  "status": "success",
  "message": "Global Shopify URL set successfully",
  "url": "https://shop.myshopify.com"
}
```

**Note**: After setting global URL, you can use `/sh` and `/msh` without specifying site parameter!

---

### 5. `/myurl` - Show Current Global URL

**Purpose**: Check what global URL is currently set

**Method**: `GET`

**Format**:
```
/myurl
```

**Example**:
```
https://your-app.onrender.com/myurl
```

**Response** (when URL is set):
```json
{
  "status": "success",
  "url": "https://shop.myshopify.com"
}
```

**Response** (when no URL is set):
```json
{
  "status": "info",
  "message": "No global URL set",
  "hint": "Use /seturl?url={shopify_url} to set one"
}
```

---

### 6. `/rmurl` - Remove Global URL

**Purpose**: Clear the global URL setting

**Method**: `GET`

**Format**:
```
/rmurl
```

**Example**:
```
https://your-app.onrender.com/rmurl
```

**Response**:
```json
{
  "status": "success",
  "message": "Global URL removed",
  "previous_url": "https://shop.myshopify.com"
}
```

---

## 🔌 Proxy Management Endpoints

### 7. `/addp` - Add Proxy

**Purpose**: Add a proxy to rotation pool

**Method**: `GET`

**Format**:
```
/addp?proxy={proxy_url}
```

**Example**:
```
https://your-app.onrender.com/addp?proxy=http://user:pass@proxy.com:8080
```

**Response**:
```json
{
  "status": "success",
  "message": "Proxy added successfully",
  "proxy": "http://user:pass@proxy.com:8080",
  "total_proxies": 3
}
```

---

### 8. `/rp` - Remove Proxy

**Purpose**: Remove a proxy or all proxies

**Method**: `GET`

**Format** (remove specific proxy):
```
/rp?index={number}
```

**Format** (remove all proxies):
```
/rp
```

**Example 1** (remove proxy #2):
```
https://your-app.onrender.com/rp?index=2
```

**Example 2** (remove all):
```
https://your-app.onrender.com/rp
```

**Response** (specific):
```json
{
  "status": "success",
  "message": "Proxy removed",
  "removed_proxy": "http://user:pass@proxy.com:8080",
  "remaining_proxies": 2
}
```

**Response** (all):
```json
{
  "status": "success",
  "message": "All proxies removed",
  "removed_count": 3
}
```

---

### 9. `/lp` - List Proxies

**Purpose**: View all configured proxies

**Method**: `GET`

**Format**:
```
/lp
```

**Example**:
```
https://your-app.onrender.com/lp
```

**Response**:
```json
{
  "status": "success",
  "total_proxies": 3,
  "next_proxy_index": 2,
  "proxies": [
    {
      "index": 1,
      "proxy": "http://user:pass@proxy1.com:8080"
    },
    {
      "index": 2,
      "proxy": "http://user:pass@proxy2.com:8080"
    },
    {
      "index": 3,
      "proxy": "http://user:pass@proxy3.com:8080"
    }
  ]
}
```

---

### 10. `/cp` - Check Proxy Status

**Purpose**: Test if the next proxy in rotation is working

**Method**: `GET`

**Format**:
```
/cp
```

**Example**:
```
https://your-app.onrender.com/cp
```

**Response** (proxy alive):
```json
{
  "status": "alive",
  "proxy": "http://user:pass@proxy.com:8080",
  "ip": "185.123.45.67",
  "response_time": "1.23s",
  "index": 2,
  "total_proxies": 3
}
```

**Response** (proxy dead):
```json
{
  "status": "dead",
  "proxy": "http://user:pass@proxy.com:8080",
  "error": "Connection timeout",
  "index": 2
}
```

---

## 🧪 Site Testing Endpoints

### 11. `/chkurl` - Test Single Shopify Site

**Purpose**: Check if a Shopify site is working and accessible

**Method**: `GET`

**Format**:
```
/chkurl?url={shopify_site}
```

**Example**:
```
https://your-app.onrender.com/chkurl?url=https://shop.myshopify.com
```

**Response** (working site):
```json
{
  "status": "working",
  "url": "https://shop.myshopify.com",
  "products_found": 45,
  "message": "Site is working! Found 45 products"
}
```

**Response** (error):
```json
{
  "status": "error",
  "url": "https://shop.myshopify.com",
  "message": "Connection timeout"
}
```

---

### 12. `/mchku` - Mass Check Multiple Sites

**Purpose**: Test multiple Shopify sites at once (up to 20)

**Method**: `GET`

**Format**:
```
/mchku?urls={url1},{url2},{url3}
```

**Example**:
```
https://your-app.onrender.com/mchku?urls=https://shop1.com,https://shop2.com,https://shop3.com
```

**Response**:
```json
{
  "status": "success",
  "total_sites": 3,
  "working_sites": 2,
  "results": [
    {
      "index": 1,
      "status": "working",
      "url": "https://shop1.com",
      "products_found": 23,
      "message": "Site is working! Found 23 products"
    },
    {
      "index": 2,
      "status": "error",
      "url": "https://shop2.com",
      "message": "Connection refused"
    },
    {
      "index": 3,
      "status": "working",
      "url": "https://shop3.com",
      "products_found": 15,
      "message": "Site is working! Found 15 products"
    }
  ]
}
```

---

## 📊 Health & Info Endpoints

### `/` - API Information

**Purpose**: Get API status and all available endpoints

**Method**: `GET`

**Example**:
```
https://your-app.onrender.com/
```

---

### `/health` - Health Check

**Purpose**: Check if API is running

**Method**: `GET`

**Example**:
```
https://your-app.onrender.com/health
```

**Response**:
```json
{
  "status": "healthy",
  "proxies_loaded": 3,
  "global_url_set": true
}
```

---

## 🔄 Complete Workflow Examples

### Example 1: Basic Card Check (No Setup Required)

```bash
# Just check a card with site URL
https://your-app.onrender.com/shopify.py?lista=https://shop.com|4532123456789012|12|25|123
```

---

### Example 2: Set Up Global URL Then Check Cards

```bash
# Step 1: Set global URL
https://your-app.onrender.com/seturl?url=https://shop.myshopify.com

# Step 2: Check single card (no need to specify site)
https://your-app.onrender.com/sh?lista=4532123456789012|12|25|123

# Step 3: Check multiple cards
https://your-app.onrender.com/msh?cards=4532|12|25|123,4556|01|26|456
```

---

### Example 3: Add Proxies and Use Them

```bash
# Step 1: Add proxies
https://your-app.onrender.com/addp?proxy=http://user:pass@proxy1.com:8080
https://your-app.onrender.com/addp?proxy=http://user:pass@proxy2.com:8080

# Step 2: List proxies to confirm
https://your-app.onrender.com/lp

# Step 3: Check proxy status
https://your-app.onrender.com/cp

# Step 4: Now all card checks will automatically use proxies
https://your-app.onrender.com/shopify.py?lista=https://shop.com|4532|12|25|123
```

---

### Example 4: Find Working Shopify Sites

```bash
# Test multiple sites to find working ones
https://your-app.onrender.com/mchku?urls=https://shop1.com,https://shop2.com,https://shop3.com

# Test a specific site
https://your-app.onrender.com/chkurl?url=https://shop.myshopify.com
```

---

## ⚠️ Important Notes

1. **Global Settings Reset**: Settings (URL, proxies) reset when the app restarts on Render free plan
2. **Permanent Proxies**: Use environment variable `PROXIES` in Render for permanent proxy configuration
3. **Permanent URL**: Use environment variable `DEFAULT_SHOPIFY_URL` in Render
4. **Rate Limits**: Use proxies to avoid being blocked by Shopify
5. **Max Cards**: Maximum 10 cards per `/msh` request
6. **Max Sites**: Maximum 20 sites per `/mchku` request

---

## 🌐 Using From Browser

All endpoints work directly in your browser! Just paste the URL.

**Example**:
```
https://your-app.onrender.com/shopify.py?lista=https://shop.com|4532123456789012|12|25|123
```

Paste this in your browser and hit Enter - you'll see the JSON response!

---

## 📱 Using From Code

### JavaScript/Fetch
```javascript
fetch('https://your-app.onrender.com/shopify.py?lista=https://shop.com|4532|12|25|123')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python
```python
import requests
response = requests.get('https://your-app.onrender.com/shopify.py?lista=https://shop.com|4532|12|25|123')
print(response.json())
```

### cURL
```bash
curl "https://your-app.onrender.com/shopify.py?lista=https://shop.com|4532|12|25|123"
```

---

## ✅ Status Responses

- **LIVE** - Card approved/valid
- **DEAD** - Card declined/invalid  
- **ERROR** - System error occurred

---

**Need Help?** Check the main README.md for deployment instructions!
