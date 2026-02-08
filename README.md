# 🛒 ShopEase - Modern E-Commerce Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green?style=for-the-badge&logo=flask)
![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?style=for-the-badge&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A production-ready, feature-rich e-commerce platform with modern UI/UX**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-api-documentation)

</div>

---

## ✨ Features

### 🛍️ Customer Features
- **Product Browsing** - Browse 60+ products across 6 categories
- **Advanced Filters** - Filter by category, price range, brand, availability
- **Smart Search** - Real-time product search with instant results
- **Wishlist** - Save favorite products for later
- **Shopping Cart** - Add/remove items with real-time price calculations
- **Coupon System** - Apply discount coupons (WELCOME10, SAVE20, FLAT50, SUMMER25)
- **Multiple Addresses** - Manage shipping addresses
- **Order Tracking** - View order history with tracking details
- **Product Reviews** - Read and write product reviews with ratings
- **User Profile** - Manage account information

### 👨‍💼 Admin Features
- **Product Management** - Create, update, delete products
- **Category Management** - Organize products into categories
- **Order Management** - View and manage customer orders
- **User Management** - View registered users
- **Inventory Control** - Track stock levels and availability

### 🔐 Security
- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt encryption for user passwords
- **Protected Routes** - Role-based access control (Admin/User)
- **Refresh Tokens** - Seamless session management
- **SQL Injection Protection** - Parameterized queries via SQLAlchemy

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/)

### Installation

#### 1️⃣ Clone Repository
```bash
git clone https://github.com/Kesh3805/E-Commerce.git
cd E-Commerce
```

#### 2️⃣ Database Setup
```sql
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### 3️⃣ Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment (.env file should already exist)
# Update DATABASE_URL with your MySQL password

# Initialize database with sample data
python seed_data.py
```

#### 4️⃣ Frontend Setup
```bash
cd frontend

# Install dependencies
npm install
```

### 🎯 Running the Application

#### Windows - Simple Start
```bash
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 🎉 Access the Application

Visit **http://localhost:3000** in your browser

#### Test Accounts

| Role  | Email | Password  | Access Level |
|-------|-------|-----------|--------------|
| **Admin** | admin@shopease.com | admin123 | Full admin panel access |
| **User** | john@example.com | user123 | Customer features |
| **User** | jane@example.com | user123 | Customer features |

---

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │ ───> │   Flask     │ ───> │   MySQL     │
│   Client    │ <─── │  REST API   │ <─── │  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
     │                      │                     │
     │                      │                     │
   Vite              JWT + Bcrypt          SQLAlchemy
```

### Tech Stack

#### Frontend
- **React 18.3.1** - UI library with hooks
- **React Router 7.1.3** - Client-side routing
- **Axios** - HTTP client with interceptors
- **React Toastify** - Toast notifications
- **Vite 6.0.7** - Build tool and dev server

#### Backend
- **Flask 3.1.0** - Web framework
- **Flask-SQLAlchemy** - ORM for database
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin support
- **PyMySQL** - MySQL driver

#### Database
- **MySQL 8.0.44** - Relational database
- **9 Tables** - User, Product, Category, Cart, Order, OrderItem, Review, Wishlist, Address, Coupon

---

## 📁 Project Structure

```
E-Commerce/
├── backend/                   # Flask backend
│   ├── app/
│   │   ├── models/           # Database models (9 tables)
│   │   ├── routes/           # API endpoints (9 blueprints)
│   │   ├── services/         # Business logic layer
│   │   └── utils/            # Helper functions
│   ├── run.py                # Application entry point
│   ├── seed_data.py          # Database seeding (62 products)
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── api/              # Axios configuration
│   │   ├── context/          # React context (Auth)
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components (10 pages)
│   │   └── App.jsx           # Root component
│   └── package.json          # NPM dependencies
│
├── README.md                 # This file
├── QUICKSTART.md            # Quick start guide
└── BUSINESS_LOGIC.md        # Business logic documentation
```

---

## 🔌 API Documentation

### Base URL: `http://localhost:5000/api`

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | User login | ❌ |
| POST | `/auth/refresh` | Refresh access token | ✅ (Refresh Token) |
| GET | `/auth/me` | Get current user | ✅ |

### Product Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/products` | Get all products (with filters) | ❌ |
| GET | `/products/:id` | Get single product | ❌ |
| GET | `/products/featured` | Get featured products | ❌ |
| GET | `/products/deals` | Get deal products | ❌ |
| POST | `/products` | Create product | ✅ (Admin) |
| PUT | `/products/:id` | Update product | ✅ (Admin) |
| DELETE | `/products/:id` | Delete product | ✅ (Admin) |

### Cart, Orders, Reviews, Wishlist & More

Full API documentation available in [API_DOCS.md](API_DOCS.md)

---

## 📊 Database Schema

### Core Tables

- **users** - User accounts with authentication
- **products** - Product catalog (62 products)
- **categories** - 6 product categories
- **cart** - Shopping cart items
- **orders** - Order records with tracking
- **order_items** - Order line items
- **reviews** - Product reviews and ratings
- **wishlist** - Saved products
- **addresses** - Shipping addresses
- **coupons** - Discount coupons

---

## 🧪 Sample Data

The seed script creates:

- **62 Products** across 6 categories
  - 📱 Electronics (12)
  - 👕 Fashion (11)
  - 🏠 Home & Kitchen (10)
  - ⚽ Sports & Outdoors (10)
  - 📚 Books (9)
  - 💄 Beauty & Health (10)

- **3 Users** (admin, john, jane)
- **4 Coupons** (WELCOME10, SAVE20, FLAT50, SUMMER25)
- **Reviews** on all products

---

## 🛠️ Development

### Run Backend in Development Mode
```bash
cd backend
python run.py
```

### Run Frontend with Hot Reload
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
cd frontend
npm run build
```

---

## 📦 Deployment

### Deployment Checklist
- [ ] Update `.env` with production database URL
- [ ] Set strong `JWT_SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Build frontend: `npm run build`
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure database backups

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📞 Support

For issues or questions:
1. Check [QUICKSTART.md](QUICKSTART.md)
2. Open an issue on GitHub
3. Contact the maintainer

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

</div>
