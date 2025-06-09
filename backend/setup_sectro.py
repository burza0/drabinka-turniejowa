#!/usr/bin/env python3

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_sectro_tables():
    """Create SECTRO tables in database"""
    try:
        DB_URL = os.getenv("DATABASE_URL")
        print("🔗 Connecting to database...")
        
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("📊 Creating SECTRO tables...")
        
        # Read and execute SQL
        with open('create_sectro_tables.sql', 'r') as f:
            sql = f.read()
        
        cur.execute(sql)
        conn.commit()
        
        # Check if tables exist
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_name LIKE 'sectro_%'
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        
        print("✅ SECTRO tables created successfully!")
        print(f"📋 Tables: {[t[0] for t in tables]}")
        
        # Check if we have test data
        cur.execute("SELECT COUNT(*) FROM sectro_sessions")
        count = cur.fetchone()[0]
        print(f"📊 Sessions count: {count}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating SECTRO tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SECTRO Database Setup")
    success = create_sectro_tables()
    if success:
        print("🎉 Setup completed successfully!")
    else:
        print("💥 Setup failed!") 