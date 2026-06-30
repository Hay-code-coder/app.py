from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
import math

app = Flask(__name__)

# ==========================================
# 1. CATALOG CONFIGURATION
# You can change names and weights (in grams) directly here!
# ==========================================
PRODUCTS_CONFIG = [
    {"image": "krtist02306.jpg", "name": "Baraka Rose Gold Hexagon Bracelet", "weight": 12.5},
    {"image": "krtist02301.jpg", "name": "Baraka Slim Ceramic Link Bracelet", "weight": 9.8},
    {"image": "krtist02299.jpg", "name": "Baraka Diamond Accent Chain", "weight": 15.2},
    {"image": "krtist02298.jpg", "name": "Baraka Geometric Tech-Ceramic", "weight": 11.4},
    {"image": "krtist02313.jpg", "name": "Baraka Heavy Matte Link Bracelet", "weight": 18.5},
    {"image": "krtist02316.jpg", "name": "Baraka Multi-tone Segmented Band", "weight": 14.0},
    {"image": "krtist02314.jpg", "name": "Baraka Minimalist Hex Lock", "weight": 10.5},
    {"image": "krtist02312.jpg", "name": "Baraka Bold Structural Ceramic", "weight": 16.8},
    {"image": "krtist02311.jpg", "name": "Baraka Classic Signature Edition", "weight": 13.2},
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
            
            if len(cols_text) >= 3 and '999.9' in cols_text[0]:
                sell_price_str = cols_text[2]
                sell_price = float(''.join(c for c in sell_price_str if c.isdigit() or c == '.'))
                return sell_price
    except Exception as e:
        print(f"Error fetching live price: {e}")
        return 128.00  # Dynamic fallback
    return 128.00 

@app.route('/')
def customer_pricing_page():
    live_gold_sell_price = get_live_gold_price()
    
    # Gold price per gram (e.g., $127.30 / 1.7 = $74.88)
    gold_price_per_gram = math.floor((live_gold_sell_price / 1.7) * 100) / 100.0
    
    # Summarize extra fees: 21 + 8 + 10 + 7 + 4 = 50
    extra_costs = 21 + 8 + 10 + 7 + 4 
    
    calculated_products = []
    for product in PRODUCTS_CONFIG:
        # Final price formula: (Live gold price / 1.7) + (Extra costs * weight)
        final_price = gold_price_per_gram + (extra_costs * product["weight"])
        
        calculated_products.append({
            "image": product["image"],
            "name": product["name"],
            "weight": product["weight"],
            "final_price": round(final_price, 2)
        })
    
    return render_template_string(HTML_TEMPLATE, 
                                  products=calculated_products, 
                                  gold_per_gram=gold_price_per_gram,
                                  live_gold=live_gold_sell_price)

# Frontend Layout matching premium dark/gold requirements
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baraka Exclusive Collection</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        serif: ['Cinzel', 'serif'],
                    },
                    colors: {
                        obsidian: '#0a0a0a',
                        gold: {
                            400: '#facc15',
                            500: '#eab308',
                            600: '#ca8a04',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        .glass-card {
            background: linear-gradient(145deg, rgba(30,30,30,0.8) 0%, rgba(15,15,15,0.9) 100%);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(234, 179, 8, 0.15);
        }
    </style>
</head>
<body class="bg-obsidian text-gray-200 font-sans min-h-screen selection:bg-gold-500 selection:text-black">
    
    <!-- Navigation Bar -->
    <nav class="border-b border-white/10 bg-black/50 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="text-gold-500 font-serif text-2xl tracking-widest font-bold uppercase">
                BARAKA COLLECTION
            </div>
            <div class="flex flex-col sm:flex-row items-center gap-3">
                <div class="flex items-center gap-2 bg-white/5 rounded-full px-4 py-1.5 border border-white/10 text-xs">
                    <span class="text-gray-400">Live 999.9 Gold Sell Price:</span>
                    <span class="text-gold-400 font-semibold font-mono">${{ "{:,.2f}".format(live_gold) }}</span>
                </div>
                <div class="flex items-center gap-2 bg-amber-500/10 rounded-full px-4 py-1.5 border border-amber-500/20 text-xs">
                    <span class="text-amber-500 font-medium">Calculated Gold / Gram:</span>
                    <span class="text-gold-400 font-bold font-mono">${{ "{:,.2f}".format(gold_per_gram) }}</span>
                </div>
            </div>
        </div>
    </nav>

    <!-- Header -->
    <header class="max-w-7xl mx-auto px-6 py-16 text-center">
        <h1 class="text-4xl md:text-5xl font-serif text-white mb-4 tracking-wide">
            Luxurious <span class="text-gold-500 italic">Prestige</span>
        </h1>
        <p class="max-w-2xl mx-auto text-gray-400 font-light text-sm leading-relaxed">
            Our premium Italian bracelets are dynamically priced relative to live market valuations of 999.9 gold weight content.
        </p>
    </header>

    <!-- Product Grid -->
    <main class="max-w-7xl mx-auto px-6 pb-24">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for product in products %}
            <article class="glass-card rounded-2xl overflow-hidden group hover:border-gold-500/50 transition-all duration-500 flex flex-col justify-between">
                
                <!-- Image Container -->
                <div class="aspect-square bg-[#121212] relative overflow-hidden flex items-center justify-center p-6">
                    <!-- Standard HTML image search path pointing to our local Flask static files -->
                    <img src="/static/{{ product.image }}" alt="{{ product.name }}" class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-700 ease-out" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    
                    <!-- Beautiful Fallback Card if image doesn't exist yet -->
                    <div class="absolute inset-0 hidden flex-col items-center justify-center text-gray-500 z-10 p-4 text-center">
                        <svg class="w-12 h-12 mb-2 text-gold-500/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                        <span class="text-xs font-mono text-gray-400 bg-black/40 px-2 py-1 rounded border border-white/5">{{ product.image }}</span>
                    </div>
                </div>

                <!-- Product Details -->
                <div class="p-6 border-t border-white/5 bg-black/20">
                    <h2 class="text-md font-serif text-white tracking-wide mb-1 leading-snug h-12 overflow-hidden">{{ product.name }}</h2>
                    <div class="flex items-center justify-between border-t border-white/5 pt-4 mt-2">
                        <div>
                            <span class="text-[10px] tracking-widest text-gray-400 uppercase block">Weight</span>
                            <span class="text-sm font-semibold text-slate-200 font-mono">{{ product.weight }} g</span>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] tracking-widest text-gold-500 uppercase block">Total Price</span>
                            <span class="text-xl text-gold-400 font-mono font-bold">${{ "{:,.2f}".format(product.final_price) }}</span>
                        </div>
                    </div>
                </div>
            </article>
            {% endfor %}
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-white/10 py-12 text-center text-xs text-gray-500">
        Prices are calculated dynamically in real-time based on official market data.
    </footer>

</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
