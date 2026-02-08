# 🚀 Quick Start Guide

## Prerequisites Check
- ✅ Python 3.10+
- ✅ Node.js 18+
- ✅ MySQL 8.0+

## 1-Minute Setup

### Step 1: Create Database
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 2: Configure Backend
```bash
cd backend

# Update .env with your MySQL password
# DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ecommerce_db

# Install dependencies (already done)
# Virtual environment and packages are ready

# Seed database with sample data
python seed_data.py
```

### Step 3: Start Backend
```bash
python run.py
```
Backend runs at: http://localhost:5000

### Step 4: Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```
Frontend runs at: http://localhost:3000

## Ready to Use! 🎉

### Test Accounts

**Admin Account** (Full access to admin panel)
- Email: `admin@shopease.com`
- Password: `admin123`

**Regular User Account**
- Email: `john@example.com`
- Password: `user123`

Or create your own account by clicking "Register"

## What's Included

### 24 Sample Products
- iPhone 15 Pro Max ($1,199.99)
- MacBook Pro 16" ($2,499.99)
- Sony WH-1000XM5 ($399.99)
- PlayStation 5, Xbox Series X, Nintendo Switch
- Smart home devices, fashion items, fitness gear
- And many more!

### Features to Try

#### As a User:
1. **Browse Products** - View 24 products across multiple categories
2. **Search & Filter** - Find products by name or price range
3. **Add to Cart** - Smart validation prevents over-ordering
4. **Place Orders** - Checkout with real-time stock validation
5. **Order History** - Track your orders and their status

#### As an Admin:
1. **Product Management** - Create, update, delete products
2. **Stock Control** - Manage inventory levels
3. **Order Management** - Update order status (PLACED → SHIPPED → DELIVERED)
4. **View All Orders** - See orders from all users

## API Endpoints

All endpoints are documented in the main README.md

Quick reference:
- Products: `GET /api/products`
- Cart: `GET /api/cart`
- Orders: `POST /api/orders/place`
- Auth: `POST /api/auth/login`

## Troubleshooting

### Can't connect to MySQL?
- Check MySQL is running
- Verify credentials in `backend/.env`
- Ensure `ecommerce_db` database exists

### Port already in use?
- Backend: Change port in `backend/run.py`
- Frontend: Change port in `frontend/vite.config.js`

### Missing dependencies?
```bash
# Backend
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Next Steps

1. **Customize Products** - Edit sample products or add your own
2. **Add Categories** - Extend the product model with categories
3. **Payment Integration** - Add Stripe or PayPal
4. **Email Notifications** - Send order confirmations
5. **Advanced Search** - Add category filters and faceted search

## Need Help?

Check the main [README.md](README.md) for detailed documentation.
