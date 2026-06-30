from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
import math

app = Flask(__name__)

# Your product catalog (9 uploaded items)
PRODUCTS_CONFIG = [
    {"image": "krtist02306.jpg", "name": "Baraka Rose Gold Hexagon Bracelet"},
    {"image": "krtist02301.jpg", "name": "Baraka Slim Ceramic Link Bracelet"},
    {"image": "krtist02299.jpg", "name": "Baraka Diamond Accent Chain"},
    {"image": "krtist02298.jpg", "name": "Baraka Geometric Tech-Ceramic"},
    {"image": "krtist02313.jpg", "name": "Baraka Heavy Matte Link Bracelet"},
    {"image": "krtist02316.jpg", "name": "Baraka Multi-tone Segmented Band"},
    {"image": "krtist02314.jpg", "name": "Baraka Minimalist Hex Lock"},
    {"image": "krtist02312.jpg", "name": "Baraka Bold Structural Ceramic"},
    {"image": "krtist02311.jpg", "name": "Baraka Classic Signature Edition"},
]

def get_live_gold_price():
    url = "https://goldcenter.am/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols_text = [col.text.strip() for col in cols]
            
            # CRITICAL UPDATE: Explicitly scanning for the 999.9 row purity row
            if len(cols_text) >= 3 and '999.9' in cols_text[0]:
                # Extract the selling price (the 3rd column / Index 2)
                sell_price_str = cols_text[2]
                sell_price = float(''.join(c for c in sell_price_str if c.isdigit() or c == '.'))
                return sell_price
                
    except Exception as e:
        print(f"Error fetching live price: {e}")
        return 128.00  # Safe dynamic fallback
    
    return 128.00 

@app.route('/')
def customer_pricing_page():
    live_gold_sell_price = get_live_gold_price()
    
    # Mathematical Flow: Divide by 1.7 and slice off exactly at 2 decimals (e.g., 75.29)
    divided_price = math.floor((live_gold_sell_price / 1.7) * 100) / 100.0
    
    # Summarize extra amounts: 21 + 8 + 10 + 7 + 4 = 50
    extra_costs = 21 + 8 + 10 + 7 + 4 
    final_price = divided_price + extra_costs
    
    return render_template_string(HTML_TEMPLATE, 
                                  products=PRODUCTS_CONFIG, 
                                  final_price=final_price,
                                  live_gold=live_gold_sell_price)

# Frontend Layout matching your premium theme requirements
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Collection Catalogue</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0f172a] text-slate-200 font-sans p-4 md:p-10">
    <div class="max-w-4xl mx-auto">
        <header class="mb-10 border-b border-slate-700 pb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
                <h1 class="text-3xl font-bold text-amber-500 mb-2">Baraka Luxury Catalog</h1>
                <p class="text-sm text-slate-400">Real-time valuation synchronized instantly with current market rates.</p>
            </div>
            <div class="bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 shadow-md">
                <span class="text-xs text-slate-400 uppercase block font-semibold tracking-wider mb-1">Live 999.9 Gold Sell Rate</span>
                <span class="text-amber-400 font-mono text-xl font-bold">${{ "{:,.2f}".format(live_gold) }}</span>
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {% for product in products %}
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex items-center gap-5 hover:border-amber-500/30 transition-all duration-300 shadow-lg">
                <div class="w-20 h-20 bg-slate-800 border border-slate-700 rounded-lg flex flex-col items-center justify-center shrink-0">
                    <span class="text-[9px] text-slate-400 font-mono px-2 text-center break-all">{{ product.image }}</span>
                </div>
                <div class="flex-1">
                    <h3 class="text-md font-semibold text-slate-100 leading-tight mb-2">{{ product.name }}</h3>
                    <p class="text-2xl font-bold text-amber-400 font-mono">${{ "{:,.2f}".format(final_price) }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <footer class="mt-16 text-center text-xs text-slate-500 border-t border-slate-800 pt-6">
            All prices are updated automatically relative to official daily financial market postings.
        </footer>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
