from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# PRODUCT DATABASE
products = [
    {"id": 1, "name": "Dell XPS 13", "brand": "Dell", "category": "laptop", "price": 1199, "stock": 10, "specs": "13-inch, Intel i7, 16GB RAM"},
    {"id": 2, "name": "Dell Inspiron 15", "brand": "Dell", "category": "laptop", "price": 699, "stock": 15, "specs": "15-inch, i5, 8GB"},
    {"id": 3, "name": "HP Spectre x360", "brand": "HP", "category": "laptop", "price": 1399, "stock": 5, "specs": "2-in-1, 4K display"},
    {"id": 4, "name": "HP Pavilion", "brand": "HP", "category": "laptop", "price": 549, "stock": 20, "specs": "AMD Ryzen 5"},
    {"id": 5, "name": "Lenovo ThinkPad X1", "brand": "Lenovo", "category": "laptop", "price": 1499, "stock": 7, "specs": "Business laptop"},
    {"id": 6, "name": "Apple MacBook Air M2", "brand": "Apple", "category": "laptop", "price": 1199, "stock": 12, "specs": "13.6-inch, 8GB unified"},
    {"id": 7, "name": "Apple MacBook Pro 14", "brand": "Apple", "category": "laptop", "price": 1999, "stock": 6, "specs": "M2 Pro chip"},
    {"id": 8, "name": "Asus ROG Zephyrus", "brand": "Asus", "category": "laptop", "price": 1599, "stock": 4, "specs": "Gaming laptop, RTX 4060"},
    {"id": 9, "name": "iPhone 15 Pro", "brand": "Apple", "category": "smartphone", "price": 999, "stock": 25, "specs": "6.1-inch, A17 Pro"},
    {"id": 10, "name": "iPhone 15", "brand": "Apple", "category": "smartphone", "price": 799, "stock": 30, "specs": "6.1-inch, dual camera"},
    {"id": 11, "name": "Samsung Galaxy S24 Ultra", "brand": "Samsung", "category": "smartphone", "price": 1299, "stock": 15, "specs": "6.8-inch, S Pen"},
    {"id": 12, "name": "Samsung Galaxy A54", "brand": "Samsung", "category": "smartphone", "price": 449, "stock": 40, "specs": "Mid-range, 5G"},
    {"id": 13, "name": "Google Pixel 8 Pro", "brand": "Google", "category": "smartphone", "price": 999, "stock": 10, "specs": "Best camera"},
    {"id": 14, "name": "Google Pixel 8", "brand": "Google", "category": "smartphone", "price": 699, "stock": 18, "specs": "Tensor G3"},
    {"id": 15, "name": "OnePlus 12", "brand": "OnePlus", "category": "smartphone", "price": 799, "stock": 12, "specs": "Snapdragon 8 Gen 3"},
    {"id": 16, "name": "Xiaomi 14 Pro", "brand": "Xiaomi", "category": "smartphone", "price": 899, "stock": 8, "specs": "Leica camera"},
    {"id": 17, "name": "Nike Air Max", "brand": "Nike", "category": "shoes", "price": 120, "stock": 20, "specs": "Men's size 7-12"},
    {"id": 18, "name": "Nike Revolution 6", "brand": "Nike", "category": "shoes", "price": 65, "stock": 35, "specs": "Running shoes"},
    {"id": 19, "name": "Adidas Ultraboost", "brand": "Adidas", "category": "shoes", "price": 180, "stock": 12, "specs": "Ultra comfort"},
    {"id": 20, "name": "Adidas Stan Smith", "brand": "Adidas", "category": "shoes", "price": 85, "stock": 22, "specs": "Classic sneakers"},
    {"id": 21, "name": "Puma Suede Classic", "brand": "Puma", "category": "shoes", "price": 70, "stock": 18, "specs": "Unisex"},
    {"id": 22, "name": "Reebok Nano X3", "brand": "Reebok", "category": "shoes", "price": 140, "stock": 9, "specs": "Training shoes"},
    {"id": 23, "name": "Bata Power", "brand": "Bata", "category": "shoes", "price": 30, "stock": 50, "specs": "Budget casuals"},
    {"id": 24, "name": "Levi's 501 Jeans", "brand": "Levi's", "category": "clothing", "price": 89, "stock": 40, "specs": "Original fit"},
    {"id": 25, "name": "Zara Slim Fit Jacket", "brand": "Zara", "category": "clothing", "price": 120, "stock": 15, "specs": "Blazer style"},
    {"id": 26, "name": "H&M Cotton T-Shirt", "brand": "H&M", "category": "clothing", "price": 15, "stock": 100, "specs": "Pack of 2"},
    {"id": 27, "name": "Rolex Submariner", "brand": "Rolex", "category": "accessories", "price": 10000, "stock": 2, "specs": "Luxury watch"},
]

# LANGUAGE DETECTION
def is_roman_urdu(text):
    urdu_hints = ["hai", "hain", "kya", "mujhe", "tumhe", "apko", "ye", "wo", "ka", "ki", "ke", "nai", "nahi", "karo", "de", "lao", "dikhao", "batao", "kahan", "yahan", "wahan", "bahut", "thoda", "kitna", "daam", "rupiye", "asslam", "salam", "adaab", "kitne", "chahiye", "chahta", "chahti"]
    text_lower = text.lower()
    for hint in urdu_hints:
        if hint in text_lower:
            return True
    return False

def detect_language(text):
    return "urdu" if is_roman_urdu(text) else "english"

def extract_brand_urdu(text):
    brands = ["dell", "hp", "lenovo", "apple", "asus", "samsung", "google", "oneplus", "xiaomi", "nike", "adidas", "puma", "reebok", "bata", "levi's", "zara", "h&m", "rolex"]
    text_lower = text.lower()
    for b in brands:
        if b in text_lower:
            return b
    return None

def extract_category_urdu(text):
    text_lower = text.lower()
    if "laptop" in text_lower or "lap" in text_lower:
        return "laptop"
    if "smartphone" in text_lower or "phone" in text_lower or "mobile" in text_lower or "fon" in text_lower:
        return "smartphone"
    if "shoe" in text_lower or "shoes" in text_lower or "joota" in text_lower or "jootay" in text_lower:
        return "shoes"
    if "clothing" in text_lower or "kapray" in text_lower or "jeans" in text_lower or "jacket" in text_lower or "tshirt" in text_lower:
        return "clothing"
    if "watch" in text_lower or "ghari" in text_lower or "rolex" in text_lower:
        return "accessories"
    return None

def get_greeting(lang):
    if lang == "urdu":
        return "Assalam u Alaikum! Main aapka Shopping Information Assistant hoon. Main products, prices, brands, aur availability ke baare mein bata sakta hoon. Type 'help' commands ke liye."
    else:
        return "Welcome! I'm your Shopping Information Assistant. I can help you find products, check prices, brands, and availability. Type 'help' for commands."

def get_help(lang):
    if lang == "urdu":
        return """Commands:
• [brand] [category] dikhao --> "Dell laptop dikhao"
• [product] ka price --> "iPhone 15 ka price"
• find/need [category] -->"help me find laptop", "I need shoes"
• [brand] k products --> "Nike shoes"
• kitne brands hain? / saare brands dikhao
• compare [brand A] aur [brand B] --> "Apple aur Samsung compare karo" """
    else:
        return """Commands:
• show [brand] [category] --> "show Dell laptops"
• price of [product] --> "price of MacBook Air"
• find/need [category] --> "help me find laptop", "I need shoes"
• list all brands / how many brands
• compare [brand A] and [brand B] --> "compare Apple and Samsung" """

def get_list_brands(lang):
    brands = sorted(set(p["brand"] for p in products))
    if lang == "urdu":
        return f"Available brands: {', '.join(brands)}"
    return f"Available Brands: {', '.join(brands)}"

def get_products_by_brand(brand, category, lang):
    filtered = [p for p in products if p["brand"].lower() == brand]
    if category:
        filtered = [p for p in filtered if p["category"] == category]
    if not filtered:
        if lang == "urdu":
            return f"{brand.title()} ka koi {category if category else 'product'} nahi mila."
        return f" No {brand} {category or 'products'} found."
    heading = f"{brand.title()} {'Products' if lang=='english' else 'ke products'}:\n"
    for p in filtered:
        heading += f"• {p['name']} – ${p['price']} ({p['specs']})\n"
    return heading

def get_price(product_name, lang):
    found = [p for p in products if product_name.lower() in p["name"].lower()]
    if not found:
        return "Product nahi mila." if lang=="urdu" else "Product not found."
    response = ""
    for p in found:
        if lang == "urdu":
            response += f"{p['name']} ka daam ${p['price']} hai. Stock: {p['stock']} units. Specs: {p['specs']}\n"
        else:
            response += f"{p['name']} costs ${p['price']}. Stock: {p['stock']} units. Specs: {p['specs']}\n"
    return response

def compare_brands(brand1, brand2, lang):
    prods1 = [p for p in products if p["brand"].lower() == brand1]
    prods2 = [p for p in products if p["brand"].lower() == brand2]
    if not prods1 or not prods2:
        if lang == "urdu":
            return "Ek ya dono brands nahi mile."
        return "One or both brands not found."
    min1 = min(p['price'] for p in prods1)
    min2 = min(p['price'] for p in prods2)
    if lang == "urdu":
        return f"{brand1.title()} vs {brand2.title()}:\n{brand1.title()} ke {len(prods1)} products hain, shuruati daam ${min1}.\n{brand2.title()} ke {len(prods2)} products hain, shuruati daam ${min2}."
    else:
        return f"Comparison {brand1.title()} vs {brand2.title()}:\n{brand1.title()} has {len(prods1)} products starting from ${min1}.\n{brand2.title()} has {len(prods2)} products starting from ${min2}."

def unknown(lang):
    return "Mujhe samajh nahi aaya. 'help' likhein." if lang=="urdu" else "I didn't understand. Type 'help'."

# MAIN BOT LOGIC
def get_bot_response(user_msg):
    lang = detect_language(user_msg)
    msg = user_msg.lower().strip()
    
    # Greetings
    greetings = ["hi", "hello", "hey", "salam", "assalam", "assalamualaikum","asslam o alaikum", "asslam-o-alaikum", "adaab", "good morning", "good evening", "good afternoon", "kem cho", "kya haal", "kaise ho"]
    if any(g in msg for g in greetings):
        return get_greeting(lang)
    
    # FIND/NEED/WANT
    find_phrases = ["need ", "want ", "chahiye", "looking for", "find me", "help me find", "find ", "i need", "i want", "mujhe", "chahta", "chahti"]
    if any(phrase in msg for phrase in find_phrases):
        category = extract_category_urdu(msg)
        brand = extract_brand_urdu(msg)
        if category:
            filtered = [p for p in products if p["category"] == category]
            if brand:
                filtered = [p for p in filtered if p["brand"].lower() == brand]
            if filtered:
                heading = f"{category.title()} options:\n" if lang=="english" else f"{category.title()} ke options*:\n"
                for p in filtered[:5]:
                    heading += f"• {p['name']} - ${p['price']}\n"
                if len(filtered) > 5:
                    heading += f"for more {len(filtered)-5} . Type 'show {brand if brand else category}' for all.\n"
                return heading
            else:
                return f"Sorry, no {category} found." if lang=="english" else f"Mazrat, {category} nahi mila."
        elif brand:
            return get_products_by_brand(brand, None, lang)
        else:
            return "Which product do you need? (e.g., shoes, laptop, smartphone)" if lang=="english" else "Aapko kis cheez ki zaroorat hai? (jaise shoes, laptop, smartphone)"
    
    # HELP
    if "help" in msg or "madad" in msg:
        return get_help(lang)
    
    # Brands count
    count_phrases = ["kitne brands", "total brands", "kull brands", "kitne brand", "total kitne brands", "brands ki tadad", "kitne hain brands", "kitne brands hain"]
    if any(phrase in msg for phrase in count_phrases) or (("brands" in msg or "brand" in msg) and ("kitne" in msg or "total" in msg or "kull" in msg)):
        brand_list = sorted(set(p["brand"] for p in products))
        count = len(brand_list)
        if lang == "urdu":
            return f"Total {count} brands hain: {', '.join(brand_list)}"
        else:
            return f"Total {count} brands: {', '.join(brand_list)}"
    
    # List all brands
    if "all brands" in msg or "saare brands" in msg or "brands dikhao" in msg:
        return get_list_brands(lang)
    
    # Brand or category (explicit)
    brand = extract_brand_urdu(msg)
    category = extract_category_urdu(msg)
    if brand or category:
        if brand:
            return get_products_by_brand(brand, category, lang)
        elif category:
            filtered = [p for p in products if p["category"] == category]
            heading = f"{category.title()} products:\n" if lang=="english" else f"{category.title()} ke products:\n"
            for p in filtered[:10]:
                heading += f"• {p['name']} - ${p['price']}\n"
            return heading
    
    # Price inquiry
    if "price" in msg or "daam" in msg:
        for p in products:
            if p["name"].lower() in msg:
                return get_price(p["name"], lang)
        return unknown(lang)
    
    # Compare two brands
    if "compare" in msg or "comparison" in msg or "muqabla" in msg:
        if "and" in msg or "aur" in msg:
            parts = re.split(r' and | aur ', msg)
            if len(parts) >= 2:
                b1 = extract_brand_urdu(parts[0])
                b2 = extract_brand_urdu(parts[1])
                if b1 and b2:
                    return compare_brands(b1, b2, lang)
        return unknown(lang)
    
    return unknown(lang)

# FLASK ROUTES 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        reply = get_bot_response(user_message)
        return jsonify({'response': reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({'response': "Kuch technical issue hai. Phir se try karein."})

if __name__ == '__main__':
    app.run(debug=True)