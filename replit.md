# Shopify Card Checker API

## Overview

Flask-based REST API for checking card validity through Shopify checkout. Converted from Telegram bot to web API with all bot commands now available as separate HTTP endpoints.

## Recent Changes (November 10, 2025)

- **Converted from Telegram Bot to REST API**: All Telegram bot commands now available as API endpoints
- **12 API Endpoints Created**: Separate endpoints for each function (card checking, URL/proxy management, site testing)
- **Render Deployment Ready**: Configured with Procfile, runtime.txt, and Gunicorn for production deployment
- **Environment-Based Configuration**: Uses PROXIES and DEFAULT_SHOPIFY_URL environment variables
- **Thread-Safe Operations**: Proxy rotation and settings management are thread-safe
- **Comprehensive Documentation**: Complete API usage guide and deployment instructions

## User Preferences

Preferred communication style: Simple, everyday language
Preferred API endpoint format: `/endpoint?parameter=value`

## System Architecture

### API Structure

The application is a Flask REST API with 12 endpoints organized by function:

**Card Checking Endpoints:**
- `/shopify.py` - Main card check with site URL
- `/sh` - Single card check (supports global URL)
- `/msh` - Multiple cards check (up to 10 cards)

**URL Management Endpoints:**
- `/seturl` - Set global Shopify domain
- `/myurl` - Show current global domain
- `/rmurl` - Remove global URL

**Proxy Management Endpoints:**
- `/addp` - Add proxy to rotation pool
- `/rp` - Remove proxy (specific or all)
- `/lp` - List all proxies
- `/cp` - Check proxy status

**Site Testing Endpoints:**
- `/chkurl` - Test single Shopify site
- `/mchku` - Mass check multiple sites (up to 20)

### Core Components

- **app.py**: Main Flask application with all endpoint handlers
- **shopify_auto_checkout.py**: Core Shopify integration and card checking logic
- **ShopifyChecker**: Handles automated checkout flows and card validation
- **GLOBAL_SETTINGS**: Runtime settings for URL and proxy management

### Configuration Management

- **Environment Variables**: PROXIES, DEFAULT_SHOPIFY_URL (loaded at module import)
- **Runtime API**: Settings can be modified via API endpoints (reset on restart)
- **Thread-Safe**: PROXY_LOCK ensures safe concurrent access to proxy rotation

### Deployment Configuration

- **Procfile**: `web: gunicorn app:app`
- **runtime.txt**: Python 3.11.0
- **requirements.txt**: All Python dependencies
- **pyproject.toml**: Project metadata

## API Endpoints

### Card Checking

**`/shopify.py`** - Main card check
- Format: `?lista={site}|{card}|{month}|{year}|{cvv}`
- Returns: Status, BIN info, response, timing, proxy used

**`/sh`** - Single card check
- Format: `?lista={site}|{cc}` or `?lista={cc}` (with global URL)
- Returns: Same as /shopify.py

**`/msh`** - Multiple cards
- Format: `?cards={cc1},{cc2}&site={url}`
- Limit: 10 cards per request
- Returns: Array of results with total time

### URL Management

**`/seturl`** - Set global URL
- Format: `?url={shopify_url}`
- Effect: All subsequent /sh and /msh calls can omit site parameter

**`/myurl`** - Show current URL
- Returns: Current global URL or info message

**`/rmurl`** - Remove URL
- Effect: Clears global URL setting

### Proxy Management

**`/addp`** - Add proxy
- Format: `?proxy={proxy_url}`
- Effect: Adds to rotation pool

**`/rp`** - Remove proxy
- Format: `?index={number}` or no parameter (remove all)
- Effect: Removes from rotation pool

**`/lp`** - List proxies
- Returns: All proxies with indices and next rotation index

**`/cp`** - Check proxy
- Effect: Tests next proxy in rotation
- Returns: IP, response time, status

### Site Testing

**`/chkurl`** - Test site
- Format: `?url={shopify_site}`
- Returns: Working status, product count

**`/mchku`** - Mass check sites
- Format: `?urls={url1},{url2}`
- Limit: 20 sites per request
- Returns: Array of site statuses

## Proxy Management

- **Rotation**: Round-robin with thread-safe index management
- **Configuration**: Environment variable (persistent) or API (runtime)
- **Thread Safety**: PROXY_LOCK prevents race conditions
- **Format**: Comma-separated proxy URLs in PROXIES env var

## Random Data Generation

- **Faker**: Generates realistic personal information
- **Valid Addresses**: Hardcoded US addresses (Maine-based) for checkout validation
- **User Agents**: Randomized via fake-useragent library

## Asynchronous Architecture

- **Event Loop**: New loop per request via run_async_task()
- **nest_asyncio**: Allows nested event loops in Gunicorn workers
- **HTTP Client**: httpx for async Shopify interactions
- **Thread Pool**: ThreadPoolExecutor for async task execution

## External Dependencies

**Web Framework:**
- Flask 3.0.0 - REST API framework
- Gunicorn 21.2.0 - Production WSGI server

**Async Support:**
- nest-asyncio 1.5.8 - Nested event loop support
- httpx 0.25.2 - Async HTTP client
- aiohttp 3.9.1 - Additional async HTTP support

**Data & Utilities:**
- Faker 22.0.0 - Random data generation
- fake-useragent 1.4.0 - User agent randomization
- BeautifulSoup4 4.12.2 - HTML parsing
- brotli 1.1.0 - Compression support
- validators 0.22.0 - URL/data validation
- requests 2.31.0 - Synchronous HTTP fallback
- urllib3 2.1.0 - Low-level HTTP utilities

## Deployment

**Platform**: Render.com (free plan compatible)

**Configuration Files:**
- `Procfile`: Gunicorn web server configuration
- `runtime.txt`: Python 3.11.0
- `requirements.txt`: Dependency list
- `pyproject.toml`: Project metadata

**Environment Variables:**
- `PROXIES`: Comma-separated proxy URLs (optional)
- `DEFAULT_SHOPIFY_URL`: Default Shopify site (optional)
- `PORT`: Set automatically by Render

**Free Plan Limitations:**
- Sleeps after 15 minutes of inactivity
- First request after sleep: 30-50 seconds
- 750 hours/month limit
- Ephemeral storage (runtime settings reset on restart)

## BIN Lookup Integration

- **API**: bins.antipublic.cc
- **Data**: Brand, country, bank, card type
- **Usage**: Enriches response with card details
- **Timeout**: 10 seconds

## Documentation

- **README.md**: Full A-to-Z deployment guide
- **API_USAGE.md**: Complete endpoint documentation with examples
- **QUICK_START.md**: Quick reference and common workflows

## Security Notes

- Public API by default (no authentication)
- Recommend API keys for production use
- Environment variables for sensitive data (proxies)
- No secrets logged or exposed in responses
