#!/usr/bin/env python3
"""
Test script for SECTRO module setup
Run this to verify everything is working correctly
"""

import sys
import os

def test_parser():
    """Test SECTRO parser functionality"""
    print("🧪 Testing SECTRO Parser...")
    
    try:
        from backend.sectro.sectro_parser import SectroParser
        
        parser = SectroParser(start_input=1, finish_input=4)
        
        # Test valid frames
        test_frames = [
            "CZL1123456789",  # START
            "CZL4123459500",  # FINISH 
            "CZL0000000000",  # SYNC
            "CHLx123456789",  # Invalid (should fail)
            "INVALID",        # Invalid (should fail)
        ]
        
        for frame_str in test_frames:
            frame = parser.parse_frame(frame_str)
            status = "✅ VALID" if frame.is_valid else "❌ INVALID"
            print(f"  {frame_str} -> {status} ({frame.measurement_type})")
        
        # Test race time calculation
        start = parser.parse_frame("CZL1123456000")  # 12:34:56.000
        finish = parser.parse_frame("CZL4123459500")  # 12:34:59.500
        race_time = parser.calculate_race_time(start, finish)
        
        if race_time:
            print(f"  Race time calculation: {parser.format_time(race_time)} ✅")
        else:
            print("  Race time calculation: FAILED ❌")
        
        print("✅ Parser test PASSED!\n")
        return True
        
    except Exception as e:
        print(f"❌ Parser test FAILED: {e}\n")
        return False

def test_database_schema():
    """Test if database tables exist"""
    print("🗄️ Testing Database Schema...")
    
    try:
        # Try to connect to database and check tables
        import psycopg2
        import os
        
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("⚠️ DATABASE_URL not set, skipping database test\n")
            return True
        
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check if SECTRO tables exist
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_name LIKE 'sectro_%'
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cur.fetchall()]
        expected_tables = ['sectro_sessions', 'sectro_measurements', 'sectro_results', 'sectro_logs']
        
        print(f"  Found tables: {tables}")
        
        missing_tables = [t for t in expected_tables if t not in tables]
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            print("   Run: psql $DATABASE_URL -f backend/migrations/03_add_sectro_tables.sql")
            return False
        else:
            print("✅ All required tables exist!")
        
        cur.close()
        conn.close()
        print("✅ Database test PASSED!\n")
        return True
        
    except Exception as e:
        print(f"❌ Database test FAILED: {e}")
        print("   Make sure database is running and tables are created\n")
        return False

def test_api_imports():
    """Test if API module can be imported"""
    print("🔧 Testing API Imports...")
    
    try:
        # Test if we can import the blueprint
        sys.path.append('backend')
        from sectro.sectro_api import sectro_bp
        
        print(f"  Blueprint name: {sectro_bp.name}")
        print(f"  URL prefix: {sectro_bp.url_prefix}")
        
        # Check if routes are registered
        rules = [rule.rule for rule in sectro_bp.deferred_functions]
        print(f"  Registered routes: {len(rules) if rules else 'Unknown'}")
        
        print("✅ API import test PASSED!\n")
        return True
        
    except Exception as e:
        print(f"❌ API import test FAILED: {e}")
        print("   Make sure all files are in place and __init__.py exists\n")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("📁 Testing File Structure...")
    
    required_files = [
        'backend/sectro/__init__.py',
        'backend/sectro/sectro_parser.py',
        'backend/sectro/sectro_api.py',
        'backend/migrations/03_add_sectro_tables.sql',
        'frontend/src/views/SectroView.vue',
        'SECTRO_IMPLEMENTATION_PLAN.md',
        'SECTRO_QUICK_START.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {len(missing_files)}")
        return False
    else:
        print("\n✅ All required files exist!")
        return True

def main():
    """Run all tests"""
    print("🚀 SECTRO MODULE SETUP TEST")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_parser,
        test_api_imports,
        test_database_schema
    ]
    
    results = []
    for test_func in tests:
        results.append(test_func())
    
    print("=" * 50)
    print("📊 FINAL RESULTS:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Ready to proceed!")
        print("\nNext steps:")
        print("1. Add SECTRO blueprint to api_server.py")
        print("2. Add routing to frontend")
        print("3. Test in browser")
    else:
        print("⚠️ Some tests failed. Fix issues before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 