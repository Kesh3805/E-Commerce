# 🚀 Complete Run Guide

This guide provides detailed instructions for running the ShopEase e-commerce application on Windows, Mac, and Linux.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Running the Application](#running-the-application)
4. [Troubleshooting](#troubleshooting)
5. [Common Issues](#common-issues)

---

## Prerequisites

### Required Software

1. **Python 3.10 or higher**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version` or `python3 --version`

2. **Node.js 18 or higher**
   - Download: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **MySQL 8.0 or higher**
   - Download: https://dev.mysql.com/downloads/
   - Verify: `mysql --version`

4. **Git** (for cloning)
   - Download: https://git-scm.com/
   - Verify: `git --version`

---

## Initial Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/Kesh3805/E-Commerce.git
cd E-Commerce
```

### Step 2: Database Setup

**Option A: Using MySQL Command Line**

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verify database created
SHOW DATABASES;

# Exit MySQL
EXIT;
```

**Option B: Using MySQL Workbench**

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Click "Create a new schema" button
4. Name: `ecommerce_db`
5. Character Set: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click "Apply"

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Verify .env file exists and has correct settings
# The file should contain:
# DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ecommerce_db
# JWT_SECRET_KEY=your-secret-key-here
# Replace YOUR_PASSWORD with your MySQL root password
```

### Step 4: Seed Database with Sample Data

```bash
# Make sure you're in the backend directory with venv activated
python seed_data.py
```

**Expected Output:**
```
Database seeded successfully!
 62 products across 6 categories
 3 users (admin@shopease.com / john@example.com / jane@example.com)
 3 addresses
 Reviews added to all products
 4 coupons: WELCOME10, SAVE20, FLAT50, SUMMER25
 Passwords: admin123 (admin) / user123 (users)
```

### Step 5: Frontend Setup

```bash
# Open a new terminal window/tab
cd frontend

# Install Node.js dependencies
npm install
```

**This will take a few minutes to download all packages.**

---

## Running the Application

You need to run both the backend and frontend servers simultaneously in separate terminal windows.

### Method 1: Manual Start (Recommended for Development)

#### Terminal 1 - Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Start Flask server
python run.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in production.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

✅ **Backend is now running at:** `http://localhost:5000`

#### Terminal 2 - Frontend Server

```bash
# Navigate to frontend directory
cd frontend

# Start Vite dev server
npm run dev
```

**Expected Output:**
```
VITE v6.4.1  ready in 605 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
➜  press h + enter to show help
```

✅ **Frontend is now running at:** `http://localhost:3000`

### Method 2: Using Startup Scripts (Windows)

**Create `start_backend.bat` in the backend folder:**

```batch
@echo off
echo Starting Backend Server...
cd /d "%~dp0"
call venv\Scripts\activate
python run.py
pause
```

**Create `start_frontend.bat` in the frontend folder:**

```batch
@echo off
echo Starting Frontend Server...
cd /d "%~dp0"
npm run dev
pause
```

**Usage:**
1. Double-click `start_backend.bat` to start backend
2. Double-click `start_frontend.bat` to start frontend

### Method 3: Using Startup Scripts (Mac/Linux)

**Create `start_backend.sh` in the backend folder:**

```bash
#!/bin/bash
echo "Starting Backend Server..."
cd "$(dirname "$0")"
source venv/bin/activate
python run.py
```

**Create `start_frontend.sh` in the frontend folder:**

```bash
#!/bin/bash
echo "Starting Frontend Server..."
cd "$(dirname "$0")"
npm run dev
```

**Make scripts executable:**
```bash
chmod +x backend/start_backend.sh
chmod +x frontend/start_frontend.sh
```

**Usage:**
```bash
# Terminal 1
./backend/start_backend.sh

# Terminal 2
./frontend/start_frontend.sh
```

---

## Accessing the Application

Once both servers are running:

1. **Open your web browser**
2. **Navigate to:** `http://localhost:3000`
3. **Login with test accounts:**

| Role | Email | Password | Access |
|------|-------|----------|--------|
| **Admin** | admin@shopease.com | admin123 | Full access to admin panel |
| **User** | john@example.com | user123 | Customer features |
| **User** | jane@example.com | user123 | Customer features |

---

## Stopping the Application

### To Stop Servers:

**In each terminal window:**
- Press `Ctrl + C` (Windows/Linux)
- Press `Cmd + C` (Mac)

### To Deactivate Virtual Environment:

```bash
deactivate
```

---

## Troubleshooting

### Issue 1: "python: command not found"

**Solution:**
Try using `python3` instead:
```bash
python3 --version
python3 -m venv venv
python3 run.py
```

### Issue 2: "Access denied for user 'root'@'localhost'"

**Solution:**
Check your MySQL password in the `.env` file:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_ACTUAL_PASSWORD@localhost:3306/ecommerce_db
```

### Issue 3: "Port 5000 already in use"

**Solution:**

**Windows:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process (replace PID with actual process ID)
kill -9 <PID>
```

### Issue 4: "Port 3000 already in use"

**Solution:**
Vite will automatically suggest the next available port (3001, 3002, etc.)

Or manually kill the process:

**Windows:**
```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :3000
kill -9 <PID>
```

### Issue 5: "ModuleNotFoundError" in Python

**Solution:**
Ensure virtual environment is activated and dependencies installed:
```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 6: "npm ERR!" or Node package errors

**Solution:**
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install
```

### Issue 7: Database connection errors

**Solution:**
1. Verify MySQL is running:
   ```bash
   # Windows (Services)
   services.msc  # Look for MySQL80

   # Mac
   brew services list

   # Linux
   sudo systemctl status mysql
   ```

2. Test MySQL connection:
   ```bash
   mysql -u root -p
   ```

3. Verify database exists:
   ```sql
   SHOW DATABASES;
   ```

### Issue 8: "Cannot find module" in React

**Solution:**
```bash
cd frontend
npm install
```

### Issue 9: CORS errors in browser console

**Solution:**
This should not happen with the current configuration, but if it does:

1. Verify backend `.env` has correct CORS settings
2. Restart backend server
3. Clear browser cache or use incognito mode

---

## Common Issues

### Virtual Environment Not Activating

**Windows PowerShell:**
```powershell
# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
venv\Scripts\Activate.ps1
```

### MySQL Not Starting

**Windows:**
```bash
# Start MySQL service
net start MySQL80
```

**Mac:**
```bash
# Start MySQL service
brew services start mysql

# Or
sudo /usr/local/mysql/support-files/mysql.server start
```

**Linux:**
```bash
# Start MySQL service
sudo systemctl start mysql

# Enable auto-start on boot
sudo systemctl enable mysql
```

### Backend Running but No Response

**Check logs for errors:**
1. Look at the terminal where backend is running
2. Check for error messages
3. Verify `.env` configuration
4. Test database connection: `python seed_data.py`

### Frontend Shows Blank Page

**Solution:**
1. Open browser DevTools (F12)
2. Check Console tab for JavaScript errors
3. Check Network tab for failed API requests
4. Verify backend is running and accessible
5. Clear browser cache (Ctrl + Shift + Delete)
6. Try incognito mode

---

## Development Tips

### Hot Reload

Both servers support hot reload:
- **Backend:** Flask auto-reloads on code changes
- **Frontend:** Vite hot-reloads on save

### Viewing Database Data

**Using MySQL Command Line:**
```sql
mysql -u root -p
USE ecommerce_db;

-- View users
SELECT id, name, email, is_admin FROM users;

-- View products
SELECT id, name, price, stock, category_id FROM products LIMIT 10;

-- View orders
SELECT id, user_id, total_price, status, created_at FROM orders;
```

**Using MySQL Workbench:**
1. Open MySQL Workbench
2. Connect to your server
3. Select `ecommerce_db` from schemas
4. Right-click on tables → "Select Rows"

### Resetting Database

To start fresh with new sample data:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# The seed script automatically drops and recreates tables
python seed_data.py
```

---

## Production Deployment

For production deployment, see [README.md](README.md) deployment section.

**Key changes needed:**
1. Use production database (not localhost)
2. Set `DEBUG=False` in Flask
3. Use Gunicorn or uWSGI instead of `python run.py`
4. Build frontend: `npm run build`
5. Serve frontend build with Nginx or Apache
6. Set strong `JWT_SECRET_KEY`
7. Enable HTTPS
8. Configure CORS for production domain

---

## Additional Resources

- **Main README:** [README.md](README.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Business Logic:** [BUSINESS_LOGIC.md](BUSINESS_LOGIC.md)
- **GitHub Repository:** https://github.com/Kesh3805/E-Commerce

---

## Support

If you encounter issues not covered in this guide:

1. Check all terminal outputs for error messages
2. Review the [Troubleshooting](#troubleshooting) section
3. Open an issue on GitHub with:
   - Operating system and versions
   - Error messages (full output)
   - Steps to reproduce
   - Screenshots if applicable

---

<div align="center">

**Happy Coding! 🚀**

</div>
