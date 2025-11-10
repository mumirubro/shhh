from flask import Flask, request, jsonify
import asyncio
import time
import httpx
from shopify_auto_checkout import ShopifyChecker
import json
import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import nest_asyncio
from fake_useragent import UserAgent

nest_asyncio.apply()

app = Flask(__name__)

GLOBAL_SETTINGS = {
    'url': None,
    'proxies': [],
    'proxy_index': 0
}

PROXY_LOCK = Lock()
executor = ThreadPoolExecutor(max_workers=10)

def load_settings():
    global GLOBAL_SETTINGS
    try:
        default_url = os.environ.get('DEFAULT_SHOPIFY_URL', '')
        if default_url:
            GLOBAL_SETTINGS['url'] = default_url
            print(f"Loaded default URL: {default_url}")
        
        proxies_env = os.environ.get('PROXIES', '')
        if proxies_env:
            proxy_list = [p.strip() for p in proxies_env.split(',') if p.strip()]
            GLOBAL_SETTINGS['proxies'] = proxy_list
            print(f"Loaded {len(proxy_list)} proxies from environment")
    except Exception as e:
        print(f"Error loading settings: {e}")

def get_next_proxy():
    with PROXY_LOCK:
        if not GLOBAL_SETTINGS['proxies']:
            return None
        
        proxy = GLOBAL_SETTINGS['proxies'][GLOBAL_SETTINGS['proxy_index']]
        GLOBAL_SETTINGS['proxy_index'] = (GLOBAL_SETTINGS['proxy_index'] + 1) % len(GLOBAL_SETTINGS['proxies'])
        return proxy

async def get_bin_info(bin_number):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"https://bins.antipublic.cc/bins/{bin_number}")
            if response.status_code == 200:
                return response.json()
    except:
        pass
    return None

async def check_card_async(site_url, card_num, month, year, cvv):
    start_time = time.time()
    
    try:
        proxy = get_next_proxy()
        bin_info = await get_bin_info(card_num[:6])
        
        checker = ShopifyChecker(proxy=proxy)
        result_data = await checker.check_card(
            site_url=site_url,
            card_num=card_num,
            month=month,
            year=year,
            cvv=cvv
        )
        
        elapsed = time.time() - start_time
        
        result = result_data if isinstance(result_data, str) else result_data.get('message', 'Unknown result')
        price_info = None
        
        if isinstance(result_data, dict):
            price_info = result_data.get('price')
        
        status = "LIVE" if "approved" in result.lower() or "live" in result.lower() else "DEAD"
        
        response_msg = result.split('\n')[0] if '\n' in result else result
        response_msg = response_msg.replace('❌ ', '').replace('✅ ', '').strip()
        
        reason_type = ""
        if '\nReason:' in result and '\nType:' in result:
            reason = result.split('\nReason:')[1].split('\n')[0].strip() if '\nReason:' in result else ""
            type_val = result.split('\nType:')[1].split('\n')[0].strip() if '\nType:' in result else ""
            reason_type = f"{reason}:{type_val}"
        else:
            reason_type = "N/A"
        
        card_display = f"{card_num}|{month}|{year}|{cvv}"
        
        brand = ""
        card_type = ""
        country_display = ""
        bank = ""
        bin_num = ""
        
        if bin_info:
            brand = bin_info.get('brand', 'N/A')
            card_type = bin_info.get('type', 'N/A')
            country_flag = bin_info.get('country_flag', '')
            country_name = bin_info.get('country_name', 'N/A')
            bank = bin_info.get('bank', 'N/A')
            bin_num = bin_info.get('bin', card_num[:6])
            country_display = f"{country_flag} {country_name}"
        
        price_display = "N/A"
        if price_info:
            try:
                price_dollars = float(price_info) / 100
                price_display = f"${price_dollars:.2f}"
            except:
                price_display = "N/A"
        
        return {
            'status': status,
            'card': card_display,
            'response': response_msg,
            'reason_type': reason_type,
            'bin': bin_num,
            'brand': brand,
            'type': card_type,
            'country': country_display,
            'bank': bank,
            'price': price_display,
            'time': f"{elapsed:.2f}s",
            'proxy': proxy[:40] if proxy else "No Proxy"
        }
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'card': f"{card_num}|{month}|{year}|{cvv}",
            'response': str(e),
            'reason_type': 'N/A',
            'bin': '',
            'brand': '',
            'type': '',
            'country': '',
            'bank': '',
            'price': 'N/A',
            'time': f"{time.time() - start_time:.2f}s",
            'proxy': 'N/A'
        }

async def test_shopify_site(url):
    try:
        ua = UserAgent()
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{url}/products.json",
                headers={'User-Agent': ua.random}
            )
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                return {
                    'status': 'working',
                    'url': url,
                    'products_found': len(products),
                    'message': f'Site is working! Found {len(products)} products'
                }
            else:
                return {
                    'status': 'warning',
                    'url': url,
                    'http_status': response.status_code,
                    'message': f'Site responded with status {response.status_code}'
                }
    except Exception as e:
        return {
            'status': 'error',
            'url': url,
            'message': str(e)
        }

def run_async_task(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'message': '🛒 Shopify Card Checker API',
        'version': '2.0',
        'endpoints': {
            'card_checking': {
                '/shopify.py': 'Main card check - ?lista={site}|{cc}',
                '/sh': 'Single card check - ?lista={site}|{cc}',
                '/msh': 'Multiple cards check - ?cards={cc1},{cc2}&site={url}'
            },
            'url_management': {
                '/seturl': 'Set global URL - ?url={shopify_url}',
                '/myurl': 'Show current global URL',
                '/rmurl': 'Remove global URL'
            },
            'proxy_management': {
                '/addp': 'Add proxy - ?proxy={proxy_url}',
                '/rp': 'Remove proxy - ?index={number} or remove all',
                '/lp': 'List all proxies',
                '/cp': 'Check proxy status'
            },
            'site_testing': {
                '/chkurl': 'Test Shopify site - ?url={site}',
                '/mchku': 'Mass check sites - ?urls={url1},{url2}'
            }
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'proxies_loaded': len(GLOBAL_SETTINGS['proxies']),
        'global_url_set': GLOBAL_SETTINGS['url'] is not None
    })

@app.route('/shopify.py')
def shopify_check():
    lista = request.args.get('lista', '')
    
    if not lista:
        return jsonify({
            'status': 'error',
            'message': 'Missing lista parameter',
            'usage': 'GET /shopify.py?lista={site}|{cc}',
            'example': '/shopify.py?lista=https://shop.com|4532123456789012|12|25|123'
        }), 400
    
    try:
        parts = lista.split('|')
        if len(parts) < 5:
            return jsonify({
                'status': 'error',
                'message': 'Invalid format. Use: site|card|mm|yy|cvv',
                'example': '/shopify.py?lista=https://shop.com|4532123456789012|12|25|123'
            }), 400
        
        site_url = parts[0]
        card_num = parts[1]
        month = parts[2]
        year = parts[3]
        cvv = parts[4]
        
        if not site_url.startswith('http'):
            site_url = f'https://{site_url}'
        
        result = run_async_task(check_card_async(site_url, card_num, month, year, cvv))
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/sh')
def single_check():
    lista = request.args.get('lista', '')
    
    if not lista:
        return jsonify({
            'status': 'error',
            'message': 'Missing lista parameter',
            'usage': 'GET /sh?lista={site}|{cc} OR use global URL with /sh?lista={cc}',
            'example': '/sh?lista=https://shop.com|4532123456789012|12|25|123'
        }), 400
    
    try:
        parts = lista.split('|')
        
        if len(parts) == 4:
            if not GLOBAL_SETTINGS['url']:
                return jsonify({
                    'status': 'error',
                    'message': 'No global URL set. Use /seturl first or provide full URL',
                    'usage': '/sh?lista={site}|{cc} OR set global URL with /seturl'
                }), 400
            
            site_url = GLOBAL_SETTINGS['url']
            card_num, month, year, cvv = parts
        elif len(parts) == 5:
            site_url = parts[0]
            card_num, month, year, cvv = parts[1], parts[2], parts[3], parts[4]
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid format',
                'usage': 'card|mm|yy|cvv (with global URL) OR site|card|mm|yy|cvv'
            }), 400
        
        if not site_url.startswith('http'):
            site_url = f'https://{site_url}'
        
        result = run_async_task(check_card_async(site_url, card_num, month, year, cvv))
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/msh')
def multi_check():
    cards_param = request.args.get('cards', '')
    site = request.args.get('site', '')
    
    if not cards_param:
        return jsonify({
            'status': 'error',
            'message': 'Missing cards parameter',
            'usage': 'GET /msh?cards={cc1},{cc2}&site={url}',
            'example': '/msh?cards=4532|12|25|123,4556|01|26|456&site=https://shop.com'
        }), 400
    
    if not site and not GLOBAL_SETTINGS['url']:
        return jsonify({
            'status': 'error',
            'message': 'No site URL provided and no global URL set',
            'usage': 'Provide site parameter or set global URL with /seturl'
        }), 400
    
    site_url = site if site else GLOBAL_SETTINGS['url']
    
    if not site_url.startswith('http'):
        site_url = f'https://{site_url}'
    
    try:
        cards_list = cards_param.split(',')
        cards_list = cards_list[:10]
        
        results = []
        total_start = time.time()
        
        for i, card_str in enumerate(cards_list, 1):
            parts = card_str.split('|')
            if len(parts) != 4:
                results.append({
                    'index': i,
                    'status': 'error',
                    'card': card_str,
                    'message': 'Invalid card format'
                })
                continue
            
            card_num, month, year, cvv = parts
            result = run_async_task(check_card_async(site_url, card_num, month, year, cvv))
            result['index'] = i
            results.append(result)
        
        total_time = time.time() - total_start
        
        return jsonify({
            'status': 'success',
            'total_cards': len(cards_list),
            'total_time': f'{total_time:.2f}s',
            'site': site_url,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/seturl')
def set_url():
    url = request.args.get('url', '')
    
    if not url:
        return jsonify({
            'status': 'error',
            'message': 'Missing url parameter',
            'usage': 'GET /seturl?url={shopify_url}',
            'example': '/seturl?url=https://shop.myshopify.com'
        }), 400
    
    if not url.startswith('http'):
        url = f'https://{url}'
    
    GLOBAL_SETTINGS['url'] = url
    
    return jsonify({
        'status': 'success',
        'message': 'Global Shopify URL set successfully',
        'url': url
    })

@app.route('/myurl')
def my_url():
    if GLOBAL_SETTINGS['url']:
        return jsonify({
            'status': 'success',
            'url': GLOBAL_SETTINGS['url']
        })
    else:
        return jsonify({
            'status': 'info',
            'message': 'No global URL set',
            'hint': 'Use /seturl?url={shopify_url} to set one'
        })

@app.route('/rmurl')
def remove_url():
    old_url = GLOBAL_SETTINGS['url']
    GLOBAL_SETTINGS['url'] = None
    
    return jsonify({
        'status': 'success',
        'message': 'Global URL removed',
        'previous_url': old_url
    })

@app.route('/addp')
def add_proxy():
    proxy = request.args.get('proxy', '')
    
    if not proxy:
        return jsonify({
            'status': 'error',
            'message': 'Missing proxy parameter',
            'usage': 'GET /addp?proxy={proxy_url}',
            'example': '/addp?proxy=http://user:pass@ip:port'
        }), 400
    
    with PROXY_LOCK:
        if proxy not in GLOBAL_SETTINGS['proxies']:
            GLOBAL_SETTINGS['proxies'].append(proxy)
            return jsonify({
                'status': 'success',
                'message': 'Proxy added successfully',
                'proxy': proxy[:50] + '...' if len(proxy) > 50 else proxy,
                'total_proxies': len(GLOBAL_SETTINGS['proxies'])
            })
        else:
            return jsonify({
                'status': 'warning',
                'message': 'Proxy already exists',
                'total_proxies': len(GLOBAL_SETTINGS['proxies'])
            })

@app.route('/rp')
def remove_proxy():
    index_param = request.args.get('index', '')
    
    with PROXY_LOCK:
        if not index_param:
            count = len(GLOBAL_SETTINGS['proxies'])
            GLOBAL_SETTINGS['proxies'] = []
            GLOBAL_SETTINGS['proxy_index'] = 0
            return jsonify({
                'status': 'success',
                'message': 'All proxies removed',
                'removed_count': count
            })
        
        try:
            index = int(index_param) - 1
            if 0 <= index < len(GLOBAL_SETTINGS['proxies']):
                removed = GLOBAL_SETTINGS['proxies'].pop(index)
                if GLOBAL_SETTINGS['proxy_index'] >= len(GLOBAL_SETTINGS['proxies']) and GLOBAL_SETTINGS['proxies']:
                    GLOBAL_SETTINGS['proxy_index'] = 0
                
                return jsonify({
                    'status': 'success',
                    'message': 'Proxy removed',
                    'removed_proxy': removed[:50] + '...' if len(removed) > 50 else removed,
                    'remaining_proxies': len(GLOBAL_SETTINGS['proxies'])
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'Invalid index. Use 1-{len(GLOBAL_SETTINGS["proxies"])}'
                }), 400
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Index must be a number',
                'usage': '/rp?index={number} or /rp (to remove all)'
            }), 400

@app.route('/lp')
def list_proxies():
    if not GLOBAL_SETTINGS['proxies']:
        return jsonify({
            'status': 'info',
            'message': 'No proxies configured',
            'hint': 'Use /addp?proxy={url} to add proxies'
        })
    
    proxy_list = []
    for i, p in enumerate(GLOBAL_SETTINGS['proxies'], 1):
        proxy_list.append({
            'index': i,
            'proxy': p[:50] + '...' if len(p) > 50 else p
        })
    
    next_index = (GLOBAL_SETTINGS['proxy_index'] % len(GLOBAL_SETTINGS['proxies'])) + 1
    
    return jsonify({
        'status': 'success',
        'total_proxies': len(GLOBAL_SETTINGS['proxies']),
        'next_proxy_index': next_index,
        'proxies': proxy_list
    })

@app.route('/cp')
def check_proxy():
    with PROXY_LOCK:
        if not GLOBAL_SETTINGS['proxies']:
            return jsonify({
                'status': 'error',
                'message': 'No proxies configured',
                'hint': 'Use /addp?proxy={url} to add proxies'
            }), 400
        
        next_proxy = GLOBAL_SETTINGS['proxies'][GLOBAL_SETTINGS['proxy_index']]
        next_idx = GLOBAL_SETTINGS['proxy_index'] + 1
    
    async def test_proxy():
        try:
            start_time = time.time()
            async with httpx.AsyncClient(proxy=next_proxy, timeout=15.0) as client:
                response = await client.get('https://api.ipify.org?format=json')
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    ip_data = response.json()
                    proxy_ip = ip_data.get('ip', 'Unknown')
                    
                    return {
                        'status': 'alive',
                        'proxy': next_proxy[:50] + '...' if len(next_proxy) > 50 else next_proxy,
                        'ip': proxy_ip,
                        'response_time': f'{elapsed:.2f}s',
                        'index': next_idx,
                        'total_proxies': len(GLOBAL_SETTINGS['proxies'])
                    }
                else:
                    return {
                        'status': 'warning',
                        'proxy': next_proxy[:50] + '...' if len(next_proxy) > 50 else next_proxy,
                        'http_status': response.status_code,
                        'index': next_idx
                    }
        except Exception as e:
            return {
                'status': 'dead',
                'proxy': next_proxy[:50] + '...' if len(next_proxy) > 50 else next_proxy,
                'error': str(e)[:100],
                'index': next_idx
            }
    
    result = run_async_task(test_proxy())
    return jsonify(result)

@app.route('/chkurl')
def check_url():
    url = request.args.get('url', '')
    
    if not url:
        return jsonify({
            'status': 'error',
            'message': 'Missing url parameter',
            'usage': 'GET /chkurl?url={shopify_site}',
            'example': '/chkurl?url=https://shop.myshopify.com'
        }), 400
    
    if not url.startswith('http'):
        url = f'https://{url}'
    
    result = run_async_task(test_shopify_site(url))
    return jsonify(result)

@app.route('/mchku')
def mass_check_urls():
    urls_param = request.args.get('urls', '')
    
    if not urls_param:
        return jsonify({
            'status': 'error',
            'message': 'Missing urls parameter',
            'usage': 'GET /mchku?urls={url1},{url2},{url3}',
            'example': '/mchku?urls=https://shop1.com,https://shop2.com'
        }), 400
    
    try:
        urls = [u.strip() for u in urls_param.split(',') if u.strip()]
        urls = urls[:20]
        
        results = []
        for i, url in enumerate(urls, 1):
            if not url.startswith('http'):
                url = f'https://{url}'
            
            result = run_async_task(test_shopify_site(url))
            result['index'] = i
            results.append(result)
        
        working = sum(1 for r in results if r['status'] == 'working')
        
        return jsonify({
            'status': 'success',
            'total_sites': len(urls),
            'working_sites': working,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

load_settings()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
