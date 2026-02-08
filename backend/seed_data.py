"""Seed the database with categories, products, users, reviews, and coupons."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.review import Review
from app.models.coupon import Coupon
from app.models.address import Address
from datetime import datetime, timezone, timedelta
import json, random

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ── CATEGORIES ──
    categories_data = [
        {"name": "Electronics", "slug": "electronics", "description": "Smartphones, laptops, gadgets and more",
         "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400"},
        {"name": "Fashion", "slug": "fashion", "description": "Clothing, shoes, and accessories",
         "image_url": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=400"},
        {"name": "Home & Kitchen", "slug": "home-kitchen", "description": "Furniture, decor, and kitchen essentials",
         "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400"},
        {"name": "Sports & Outdoors", "slug": "sports-outdoors", "description": "Fitness gear and outdoor equipment",
         "image_url": "https://images.unsplash.com/photo-1461896836934-bd45ba8fcf9b?w=400"},
        {"name": "Books", "slug": "books", "description": "Best-selling books across all genres",
         "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400"},
        {"name": "Beauty & Health", "slug": "beauty-health", "description": "Skincare, makeup, and wellness products",
         "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400"},
    ]

    categories = {}
    for c in categories_data:
        cat = Category(**c)
        db.session.add(cat)
        db.session.flush()
        categories[c["slug"]] = cat

    # ── PRODUCTS ──
    products_data = [
        # Electronics (12 products)
        {"name": "iPhone 15 Pro Max", "description": "Apple's flagship smartphone with A17 Pro chip, 48MP camera system, titanium design, and all-day battery life. Features USB-C and Action Button.", "price": 1199.99, "compare_price": 1299.99, "stock": 45, "brand": "Apple", "sku": "APL-IP15PM-256", "is_featured": True, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400"},
        {"name": "Samsung Galaxy S24 Ultra", "description": "Samsung's most powerful Galaxy with Snapdragon 8 Gen 3, 200MP camera, S Pen, titanium frame, and Galaxy AI features.", "price": 1099.99, "compare_price": 1199.99, "stock": 38, "brand": "Samsung", "sku": "SAM-S24U-256", "is_featured": True, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400"},
        {"name": "MacBook Pro 16\" M3 Max", "description": "The most powerful MacBook ever with M3 Max chip, 36GB unified memory, stunning Liquid Retina XDR display, and up to 22 hours battery life.", "price": 2499.99, "compare_price": 2799.99, "stock": 20, "brand": "Apple", "sku": "APL-MBP16-M3M", "is_featured": True, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400"},
        {"name": "Sony WH-1000XM5 Headphones", "description": "Industry-leading noise cancellation with exceptional sound quality, 30-hour battery, and ultra-comfortable design.", "price": 349.99, "compare_price": 399.99, "stock": 85, "brand": "Sony", "sku": "SNY-WH1000XM5", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"},
        {"name": "iPad Air M2", "description": "Supercharged by the M2 chip with a stunning 11-inch Liquid Retina display, all-day battery, and Apple Pencil support.", "price": 599.99, "compare_price": None, "stock": 55, "brand": "Apple", "sku": "APL-IPADAIR-M2", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400"},
        {"name": "Dell UltraSharp 27\" 4K Monitor", "description": "Professional-grade 27-inch 4K IPS monitor with USB-C hub, 99% sRGB, HDR400, and factory-calibrated colors.", "price": 449.99, "compare_price": 549.99, "stock": 30, "brand": "Dell", "sku": "DELL-U2723QE", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400"},
        {"name": "Google Pixel 8 Pro", "description": "Google's AI-powered flagship with Tensor G3, Magic Eraser, Best Take, and 7 years of updates.", "price": 999.00, "compare_price": 1099.00, "stock": 42, "brand": "Google", "sku": "GOOG-PIX8PRO", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400"},
        {"name": "AirPods Pro 2nd Gen", "description": "Active noise cancellation, Adaptive Audio, personalized spatial audio with dynamic head tracking.", "price": 249.00, "compare_price": 279.00, "stock": 95, "brand": "Apple", "sku": "APL-APRO2", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=400"},
        {"name": "LG 55\" OLED C3 TV", "description": "4K OLED TV with α9 AI Processor, Dolby Vision IQ, perfect blacks, and 120Hz gaming features.", "price": 1599.99, "compare_price": 1899.99, "stock": 18, "brand": "LG", "sku": "LG-OLEDC3-55", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400"},
        {"name": "Lenovo ThinkPad X1 Carbon", "description": "Premium business ultrabook with Intel Core Ultra, 14\" 2.8K OLED touchscreen, 32GB RAM, military-grade durability.", "price": 1849.00, "compare_price": 2099.00, "stock": 25, "brand": "Lenovo", "sku": "LEN-X1C-G11", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400"},
        {"name": "Canon EOS R5 Camera", "description": "Professional mirrorless camera with 45MP sensor, 8K video, Dual Pixel CMOS AF II, in-body stabilization.", "price": 3899.00, "compare_price": 4299.00, "stock": 12, "brand": "Canon", "sku": "CAN-EOSR5", "is_featured": True, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400"},
        {"name": "Logitech MX Master 3S", "description": "Premium wireless mouse with 8K DPI sensor, MagSpeed scroll, USB-C charging, works on any surface including glass.", "price": 99.99, "compare_price": 119.99, "stock": 120, "brand": "Logitech", "sku": "LOG-MXMASTER3S", "is_featured": False, "category": "electronics",
         "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400"},

        # Fashion (11 products)
        {"name": "Nike Air Max 270", "description": "Iconic lifestyle sneaker featuring the tallest Air unit yet for unmatched comfort. Mesh upper for breathability with bold colorway.", "price": 149.99, "compare_price": 179.99, "stock": 120, "brand": "Nike", "sku": "NKE-AM270-BLK", "is_featured": True, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"},
        {"name": "Levi's 501 Original Fit Jeans", "description": "The original blue jean since 1873. Button fly, straight leg, sits at waist. 100% cotton denim that gets better with every wear.", "price": 69.50, "compare_price": 89.99, "stock": 200, "brand": "Levi's", "sku": "LEV-501-32-32", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"},
        {"name": "Ray-Ban Aviator Classic", "description": "Timeless aviator sunglasses with gold metal frame and crystal green G-15 lenses. 100% UV protection.", "price": 161.00, "compare_price": None, "stock": 75, "brand": "Ray-Ban", "sku": "RB-AV-3025", "is_featured": True, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"},
        {"name": "North Face Thermoball Jacket", "description": "Lightweight, packable insulated jacket with ThermoBall Eco insulation. Warm even when wet, perfect for any adventure.", "price": 199.00, "compare_price": 249.00, "stock": 60, "brand": "North Face", "sku": "NF-THRMBL-L", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"},
        {"name": "Adidas Ultraboost 23", "description": "Revolutionary running shoe with BOOST midsole, Primeknit+ upper, and Continental rubber outsole. Perfect for any distance.", "price": 179.99, "compare_price": 199.99, "stock": 85, "brand": "Adidas", "sku": "ADS-UB23-BLK", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400"},
        {"name": "Patagonia Down Sweater Hoody", "description": "Lightweight, windproof, and water-resistant insulated jacket. 800-fill-power recycled down. Fair Trade Certified sewn.", "price": 329.00, "compare_price": None, "stock": 45, "brand": "Patagonia", "sku": "PAT-DWNSW-M", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1544923246-77d639e45b26?w=400"},
        {"name": "Ralph Lauren Polo Shirt", "description": "Classic fit polo in soft cotton mesh. Iconic embroidered pony. Ribbed collar and armbands. Timeless American style.", "price": 89.50, "compare_price": 110.00, "stock": 150, "brand": "Ralph Lauren", "sku": "RL-POLO-BLU-L", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1588117305388-c2631a279f82?w=400"},
        {"name": "Canada Goose Expedition Parka", "description": "Extreme cold weather parka rated to -30°C. 625-fill duck down, Cordura fabric, coyote fur trim. Made in Canada.", "price": 1495.00, "compare_price": None, "stock": 15, "brand": "Canada Goose", "sku": "CG-EXPPARK-L", "is_featured": True, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=400"},
        {"name": "Timberland 6-Inch Premium Boots", "description": "Iconic waterproof leather boots with padded collar, anti-fatigue technology, and recycled materials. Built to last.", "price": 198.00, "compare_price": 220.00, "stock": 70, "brand": "Timberland", "sku": "TMB-6INCH-WHT", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1605812860427-4024433a70fd?w=400"},
        {"name": "Lululemon Align Leggings", "description": "High-rise yoga pants in buttery-soft Nulu fabric. Weightless feel, four-way stretch, no pilling guarantee.", "price": 98.00, "compare_price": None, "stock": 110, "brand": "Lululemon", "sku": "LLL-ALIGN-BLK-6", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400"},
        {"name": "Carhartt Work Jacket", "description": "Heavy-duty duck canvas jacket with thick blanket lining. Multiple tool pockets, triple-stitched seams. Built for tough work.", "price": 129.99, "compare_price": 149.99, "stock": 95, "brand": "Carhartt", "sku": "CAR-WORK-BRN-XL", "is_featured": False, "category": "fashion",
         "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"},

        # Home & Kitchen (10 products)
        {"name": "Dyson V15 Detect Vacuum", "description": "Most powerful intelligent cordless vacuum with laser dust detection, LCD screen showing real-time particle counts.", "price": 749.99, "compare_price": 849.99, "stock": 35, "brand": "Dyson", "sku": "DYS-V15-DET", "is_featured": True, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400"},
        {"name": "KitchenAid Stand Mixer", "description": "Iconic tilt-head stand mixer with 5-quart stainless steel bowl, 10 speeds, and versatile hub for attachments.", "price": 379.99, "compare_price": 449.99, "stock": 40, "brand": "KitchenAid", "sku": "KA-ARTISAN-5Q", "is_featured": True, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1594385208974-2e75f8d7bb48?w=400"},
        {"name": "Instant Pot Duo 7-in-1", "description": "Multi-use pressure cooker, slow cooker, rice cooker, steamer, saute pan, yogurt maker, and warmer. 6-quart capacity.", "price": 89.95, "compare_price": 119.99, "stock": 90, "brand": "Instant Pot", "sku": "IP-DUO-6QT", "is_featured": False, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400"},
        {"name": "Philips Sonicare DiamondClean", "description": "Premium electric toothbrush with 5 modes, smart sensor technology, and beautiful glass charging cup.", "price": 219.99, "compare_price": 249.99, "stock": 50, "brand": "Philips", "sku": "PHL-SONICARE-DC", "is_featured": False, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1559591937-21a428f0d510?w=400"},
        {"name": "Nespresso Vertuo Next", "description": "Premium coffee and espresso maker using Centrifusion technology. Brews 5 sizes with one-touch simplicity.", "price": 179.95, "compare_price": 199.95, "stock": 60, "brand": "Nespresso", "sku": "NES-VERTNXT-GRY", "is_featured": False, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400"},
        {"name": "Le Creuset Dutch Oven 5.5qt", "description": "Enameled cast iron Dutch oven perfect for braising, stewing, and baking. Lifetime guarantee. Made in France.", "price": 399.95, "compare_price": None, "stock": 35, "brand": "Le Creuset", "sku": "LC-DUTCH-RED-5Q", "is_featured": False, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1585755351566-206e332fef3a?w=400"},
        {"name": "iRobot Roomba j7+", "description": "Self-emptying robot vacuum with PrecisionVision Navigation, avoids pet waste, creates smart maps, voice control.", "price": 799.99, "compare_price": 899.99, "stock": 28, "brand": "iRobot", "sku": "IRB-J7PLUS", "is_featured": True, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400"},
        {"name": "Cuisinart Food Processor 14-Cup", "description": "Powerful 720W motor with extra-large feed tube, stainless steel disc and blades. Makes meal prep effortless.", "price": 199.95, "compare_price": 249.95, "stock": 45, "brand": "Cuisinart", "sku": "CUI-FP14-BLK", "is_featured": False, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=400"},
        {"name": "Ninja Foodi Air Fryer Oven", "description": "10-in-1 countertop oven with air fry, bake, roast, broil, toast, bagel, and more. Digital controls, spacious interior.", "price": 229.99, "compare_price": 269.99, "stock": 55, "brand": "Ninja", "sku": "NJA-FOODI-AFO", "is_featured": False, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400"},
        {"name": "Weber Genesis II Gas Grill", "description": "Premium 3-burner gas grill with LED-lit control knobs, GS4 grilling system, porcelain-enameled cast iron grates.", "price": 949.00, "compare_price": None, "stock": 20, "brand": "Weber", "sku": "WBR-GEN2-335", "is_featured": False, "category": "home-kitchen",
         "image_url": "https://images.unsplash.com/photo-1603039346248-6fa60d8a4a3c?w=400"},

        # Sports & Outdoors (10 products)
        {"name": "Peloton Bike+", "description": "Premium indoor cycling bike with auto-follow resistance, rotating 23.8-inch HD touchscreen, and Apple GymKit integration.", "price": 2495.00, "compare_price": None, "stock": 15, "brand": "Peloton", "sku": "PLT-BIKEPLUS", "is_featured": True, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1517963879433-6ad2b056d712?w=400"},
        {"name": "Yeti Tundra 45 Cooler", "description": "Virtually indestructible cooler with 2+ inches of PermFrost insulation. Bear-resistant certified. Holds up to 26 cans.", "price": 325.00, "compare_price": 349.99, "stock": 25, "brand": "Yeti", "sku": "YETI-T45-WHT", "is_featured": False, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1576037728058-cfb240e15e5a?w=400"},
        {"name": "Garmin Fenix 7X Pro", "description": "Ultimate multisport GPS watch with solar charging, built-in flashlight, advanced training metrics, and topo maps.", "price": 899.99, "compare_price": 999.99, "stock": 20, "brand": "Garmin", "sku": "GAR-FNX7XPRO", "is_featured": True, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"},
        {"name": "Hydro Flask 32oz Bottle", "description": "Double-wall vacuum insulated stainless steel water bottle. Keeps drinks cold 24hrs or hot 12hrs.", "price": 44.95, "compare_price": None, "stock": 150, "brand": "Hydro Flask", "sku": "HF-32OZ-BLK", "is_featured": False, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400"},
        {"name": "TRX Pro4 Suspension Trainer", "description": "Professional-grade bodyweight training system. Build strength, balance, flexibility, and core stability anywhere.", "price": 199.95, "compare_price": None, "stock": 65, "brand": "TRX", "sku": "TRX-PRO4-SYS", "is_featured": False, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400"},
        {"name": "Coleman Sundome 6-Person Tent", "description": "Family camping tent with WeatherTec system, large windows, ground vent, easy setup. Fits 2 queen airbeds.", "price": 119.99, "compare_price": 149.99, "stock": 40, "brand": "Coleman", "sku": "CLM-SUND6P", "is_featured": False, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400"},
        {"name": "Bowflex SelectTech 552 Dumbbells", "description": "Adjustable dumbbells replace 15 sets of weights, 5-52.5 lbs per hand. Dial system changes weight in seconds.", "price": 549.00, "compare_price": 649.00, "stock": 30, "brand": "Bowflex", "sku": "BFX-ST552-PAIR", "is_featured": True, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400"},
        {"name": "Osprey Atmos AG 65 Backpack", "description": "Premium backpacking pack with Anti-Gravity suspension, adjustable harness, integrated rain cover. 65L capacity.", "price": 299.95, "compare_price": None, "stock": 35, "brand": "Osprey", "sku": "OSP-ATMOS65-M", "is_featured": False, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1511994477824-af37e70b7c58?w=400"},
        {"name": "Schwinn IC4 Indoor Cycling Bike", "description": "Connected fitness bike with magnetic resistance, dual-sided pedals, media rack, works with Zwift and Peloton app.", "price": 899.00, "compare_price": 999.00, "stock": 25, "brand": "Schwinn", "sku": "SCH-IC4-BLK", "is_featured": False, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1559895197-a75f6d3e7093?w=400"},
        {"name": "REI Quarter Dome SL 2 Tent", "description": "Ultralight 2-person backpacking tent with rainfly, easy-pitch clips, stuff sack. Weighs only 2 lbs 14 oz.", "price": 449.00, "compare_price": 499.00, "stock": 22, "brand": "REI", "sku": "REI-QDSL2-GRY", "is_featured": False, "category": "sports-outdoors",
         "image_url": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400"},

        # Books (9 products)
        {"name": "Atomic Habits by James Clear", "description": "An easy and proven way to build good habits and break bad ones. Over 15 million copies sold worldwide.", "price": 16.99, "compare_price": 27.00, "stock": 300, "brand": "Avery", "sku": "BK-ATOMICHABITS", "is_featured": True, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"},
        {"name": "The Psychology of Money", "description": "Timeless lessons on wealth, greed, and happiness by Morgan Housel. 19 short stories exploring the strange ways people think about money.", "price": 14.99, "compare_price": 20.00, "stock": 250, "brand": "Harriman", "sku": "BK-PSYMONEY", "is_featured": False, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"},
        {"name": "Clean Code by Robert C. Martin", "description": "A handbook of agile software craftsmanship. Essential reading for every developer who wants to write better code.", "price": 39.99, "compare_price": 49.99, "stock": 80, "brand": "Prentice Hall", "sku": "BK-CLEANCODE", "is_featured": False, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400"},
        {"name": "Thinking, Fast and Slow", "description": "Daniel Kahneman's groundbreaking exploration of the two systems that drive the way we think and make choices.", "price": 18.99, "compare_price": 28.00, "stock": 180, "brand": "Farrar Straus Giroux", "sku": "BK-THINKING", "is_featured": False, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"},
        {"name": "Sapiens by Yuval Noah Harari", "description": "A brief history of humankind from the Stone Age to the modern age. International bestseller translated into 60+ languages.", "price": 24.99, "compare_price": 35.00, "stock": 220, "brand": "Harper", "sku": "BK-SAPIENS", "is_featured": True, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400"},
        {"name": "The Lean Startup", "description": "Eric Ries' revolutionary approach to creating and managing successful startups in an age of uncertainty.", "price": 17.99, "compare_price": 26.00, "stock": 150, "brand": "Currency", "sku": "BK-LEANSTARTUP", "is_featured": False, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"},
        {"name": "Can't Hurt Me by David Goggins", "description": "Master your mind and defy the odds. Former Navy SEAL's memoir about self-discipline and mental toughness.", "price": 19.99, "compare_price": 28.00, "stock": 190, "brand": "Lioncrest", "sku": "BK-CANTHURTME", "is_featured": False, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"},
        {"name": "Deep Work by Cal Newport", "description": "Rules for focused success in a distracted world. Learn to develop a deep work ethic for massive productivity.", "price": 16.99, "compare_price": 27.00, "stock": 170, "brand": "Grand Central", "sku": "BK-DEEPWORK", "is_featured": False, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=400"},
        {"name": "The Almanack of Naval Ravikant", "description": "A guide to wealth and happiness. Curated collection of Naval's wisdom on wealth creation and finding happiness.", "price": 24.99, "compare_price": None, "stock": 200, "brand": "Magrathea", "sku": "BK-NAVAL", "is_featured": False, "category": "books",
         "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400"},

        # Beauty & Health (10 products)
        {"name": "CeraVe Moisturizing Cream", "description": "Dermatologist-recommended moisturizer with 3 essential ceramides and hyaluronic acid. Fragrance-free, non-comedogenic.", "price": 18.99, "compare_price": None, "stock": 200, "brand": "CeraVe", "sku": "CV-MOIST-16OZ", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400"},
        {"name": "Dyson Airwrap Multi-Styler", "description": "Complete hair styling tool using the Coanda effect. Curl, wave, smooth, and dry with no extreme heat damage.", "price": 599.99, "compare_price": 649.99, "stock": 30, "brand": "Dyson", "sku": "DYS-AIRWRAP-CM", "is_featured": True, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1522338242992-e1a54571a9f7?w=400"},
        {"name": "Ordinary Niacinamide 10% + Zinc 1%", "description": "High-strength vitamin and mineral blemish formula targeting pore congestion, oiliness, and skin texture.", "price": 6.50, "compare_price": 9.99, "stock": 500, "brand": "The Ordinary", "sku": "TO-NIAC10-30ML", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400"},
        {"name": "Olaplex Hair Perfector No.3", "description": "Professional bond-building treatment repairs damaged hair, reduces breakage, strengthens and protects all hair types.", "price": 30.00, "compare_price": None, "stock": 180, "brand": "Olaplex", "sku": "OLP-NO3-100ML", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400"},
        {"name": "La Roche-Posay Sunscreen SPF 50", "description": "Dermatologist-recommended anthelios melt-in milk sunscreen. Broad spectrum UVA/UVB protection, non-greasy.", "price": 35.99, "compare_price": 42.99, "stock": 220, "brand": "La Roche-Posay", "sku": "LRP-ANTH-SPF50", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400"},
        {"name": "Theragun Pro 5th Gen", "description": "Professional-grade percussive therapy device. 5 speeds, 16mm amplitude, OLED screen, Bluetooth connectivity.", "price": 599.00, "compare_price": 699.00, "stock": 35, "brand": "Theragun", "sku": "THR-PRO5-BLK", "is_featured": True, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=400"},
        {"name": "Drunk Elephant Vitamin C Serum", "description": "C-Firma Fresh Day Serum with 15% Vitamin C, pumpkin ferment, and pomegranate extract. Firms, brightens, and evens tone.", "price": 78.00, "compare_price": None, "stock": 140, "brand": "Drunk Elephant", "sku": "DE-CFIRMA-30ML", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400"},
        {"name": "Bioré Charcoal Pore Strips", "description": "Deep cleansing pore strips remove dirt, oil, and blackheads. Dermatologist tested, oil-free. 14 nose strips.", "price": 12.99, "compare_price": None, "stock": 350, "brand": "Bioré", "sku": "BIO-CHAR-14CT", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400"},
        {"name": "Whoop 4.0 Fitness Tracker", "description": "24/7 health and fitness monitor with strain, recovery, sleep tracking. No screen, subscription-based analytics.", "price": 239.00, "compare_price": None, "stock": 55, "brand": "Whoop", "sku": "WHP-40-BLK", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1576243345690-4e4b79b63288?w=400"},
        {"name": "Neutrogena Hydro Boost Gel", "description": "Oil-free, fragrance-free hydrating gel-cream with hyaluronic acid. Instantly quenches dry skin and keeps it hydrated.", "price": 19.99, "compare_price": 24.99, "stock": 280, "brand": "Neutrogena", "sku": "NEU-HYDRO-17OZ", "is_featured": False, "category": "beauty-health",
         "image_url": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400"},
    ]

    products = []
    for p in products_data:
        cat_slug = p.pop("category")
        product = Product(
            **p,
            category_id=categories[cat_slug].id,
            images=json.dumps([p["image_url"]]),
        )
        db.session.add(product)
        products.append(product)

    db.session.flush()

    # ── USERS ──
    admin_user = User(
        name="Admin User", email="admin@shopease.com",
        password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="ADMIN", phone="+1-555-0100",
    )
    regular_user = User(
        name="John Doe", email="john@example.com",
        password_hash=bcrypt.generate_password_hash("user123").decode("utf-8"),
        role="USER", phone="+1-555-0101",
    )
    jane_user = User(
        name="Jane Smith", email="jane@example.com",
        password_hash=bcrypt.generate_password_hash("user123").decode("utf-8"),
        role="USER", phone="+1-555-0102",
    )
    db.session.add_all([admin_user, regular_user, jane_user])
    db.session.flush()

    # ── ADDRESSES ──
    db.session.add_all([
        Address(user_id=regular_user.id, label="Home", full_name="John Doe",
                phone="+1-555-0101", address_line1="123 Main Street", address_line2="Apt 4B",
                city="New York", state="NY", zip_code="10001", country="US", is_default=True),
        Address(user_id=regular_user.id, label="Office", full_name="John Doe",
                phone="+1-555-0101", address_line1="456 Business Ave", address_line2="Suite 200",
                city="San Francisco", state="CA", zip_code="94105", country="US", is_default=False),
        Address(user_id=jane_user.id, label="Home", full_name="Jane Smith",
                phone="+1-555-0102", address_line1="789 Oak Street",
                city="Chicago", state="IL", zip_code="60601", country="US", is_default=True),
    ])

    # ── REVIEWS ──
    review_comments = [
        ("Amazing product!", "Exceeded all my expectations. The quality is outstanding and delivery was fast."),
        ("Great value", "Really happy with this purchase. Works exactly as described."),
        ("Solid choice", "Does what it's supposed to do. Good quality for the price."),
        ("Excellent quality", "Premium feel and build quality. Would buy again without hesitation."),
        ("Highly recommend", "Everyone should get one of these. Life-changing product."),
        ("Love it!", "My new favorite thing. Use it every single day."),
    ]

    users_for_reviews = [regular_user, jane_user]
    for product in products:
        num_reviews = random.randint(1, 2)
        for i in range(num_reviews):
            user = users_for_reviews[i % len(users_for_reviews)]
            title, comment = random.choice(review_comments)
            rating = random.choices([3, 4, 5], weights=[15, 35, 50])[0]
            review = Review(
                user_id=user.id,
                product_id=product.id,
                rating=rating,
                title=title,
                comment=comment,
            )
            db.session.add(review)

    # ── COUPONS ──
    coupons = [
        Coupon(code="WELCOME10", discount_type="percent", discount_value=10,
               min_order_amount=50, max_discount=100, usage_limit=1000,
               expires_at=datetime.now(timezone.utc) + timedelta(days=90)),
        Coupon(code="SAVE20", discount_type="percent", discount_value=20,
               min_order_amount=100, max_discount=200, usage_limit=500,
               expires_at=datetime.now(timezone.utc) + timedelta(days=60)),
        Coupon(code="FLAT50", discount_type="flat", discount_value=50,
               min_order_amount=200, usage_limit=200,
               expires_at=datetime.now(timezone.utc) + timedelta(days=30)),
        Coupon(code="SUMMER25", discount_type="percent", discount_value=25,
               min_order_amount=75, max_discount=150, usage_limit=300,
               expires_at=datetime.now(timezone.utc) + timedelta(days=45)),
    ]
    db.session.add_all(coupons)

    db.session.commit()

    print("\n  Database seeded successfully!")
    print(f"   {len(products)} products across {len(categories)} categories")
    print(f"   3 users (admin@shopease.com / john@example.com / jane@example.com)")
    print(f"   3 addresses")
    print(f"   Reviews added to all products")
    print(f"   {len(coupons)} coupons: WELCOME10, SAVE20, FLAT50, SUMMER25")
    print(f"   Passwords: admin123 (admin) / user123 (users)")
    print()
