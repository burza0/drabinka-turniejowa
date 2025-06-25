#!/usr/bin/env python3
"""
Run SECTRO database migration using Python
Alternative to psql command
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    """Execute SECTRO database migration"""
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    try:
        # Read migration file
        with open('backend/migrations/03_add_sectro_tables.sql', 'r') as f:
            migration_sql = f.read()
        
        # Connect to database
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(db_url)
        conn.autocommit = True  # Auto-commit for DDL statements
        cur = conn.cursor()
        
        # Execute migration
        print("📊 Executing SECTRO migration...")
        cur.execute(migration_sql)
        
        # Verify tables were created
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_name LIKE 'sectro_%'
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cur.fetchall()]
        print(f"✅ Created tables: {tables}")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("🎉 Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    if success:
        print("\nNext step: Run 'python3 test_sectro_setup.py' to verify setup")
    exit(0 if success else 1) 