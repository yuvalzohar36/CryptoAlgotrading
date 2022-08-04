import requests

resp = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=BTC&vs_currencies=USDT&include_market_cap=true"
                    "&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true")

print(resp.json())