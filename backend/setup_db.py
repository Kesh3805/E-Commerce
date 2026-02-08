"""
Database Setup Script for E-Commerce Application
Run this script to create the database and tables
"""
import pymysql
import sys
from getpass import getpass


def create_database():
    print("=" * 60)
    print("E-Commerce Database Setup")
    print("=" * 60)
    
    # Get MySQL credentials
    print("\nEnter your MySQL credentials:")
    mysql_user = input("MySQL Username (default: root): ").strip() or "root"
    mysql_password = getpass("MySQL Password: ")
    mysql_host = input("MySQL Host (default: localhost): ").strip() or "localhost"
    mysql_port = input("MySQL Port (default: 3306): ").strip() or "3306"
    
    try:
        # Connect to MySQL server
        print("\nConnecting to MySQL...")
        connection = pymysql.connect(
            host=mysql_host,
            port=int(mysql_port),
            user=mysql_user,
            password=mysql_password
        )
        
        cursor = connection.cursor()
        
        # Create database
        print("Creating database 'ecommerce_db'...")
        cursor.execute("DROP DATABASE IF EXISTS ecommerce_db")
        cursor.execute("CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✓ Database created successfully!")
        
        cursor.close()
        connection.close()
        
        # Update .env file
        print("\nUpdating .env file...")
        database_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/ecommerce_db"
        
        env_content = f"""SECRET_KEY=dev-secret-key-change-in-production-2026
JWT_SECRET_KEY=jwt-dev-secret-key-change-in-production
DATABASE_URL={database_url}
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✓ .env file updated!")
        
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print("\nYou can now run: python run.py")
        print("\nDefault admin user will be created on first run.")
        print("Register a user and then manually update their role to 'ADMIN' in the database.")
        
        return True
        
    except pymysql.Error as e:
        print(f"\n✗ MySQL Error: {e}")
        print("\nPlease check your credentials and try again.")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


if __name__ == "__main__":
    success = create_database()
    sys.exit(0 if success else 1)
