"""
AttendEase Database Initialization Script
==========================================
Connects to MySQL, executes schema.sql and seed.sql, verifies tables,
and outputs initial administrator and demo credentials.

Usage:
    python init_db.py [--host HOST] [--user USER] [--password PWD] [--port PORT] [--seed]
"""

import os
import sys
import argparse
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load existing environment
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def parse_sql_file(file_path):
    """
    Reads an SQL file and splits it into executable statements,
    handling multi-line queries, comments, and delimiters.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SQL file not found at: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    statements = []
    current_statement = []
    in_multiline_comment = False
    
    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed:
            continue
        if trimmed.startswith('/*') and not trimmed.endswith('*/'):
            in_multiline_comment = True
            continue
        if in_multiline_comment:
            if '*/' in trimmed:
                in_multiline_comment = False
            continue
        if trimmed.startswith('--') or trimmed.startswith('#'):
            continue
            
        # If line contains ';', strip any trailing comment following ';'
        if ';' in line:
            line = line.split(';')[0] + ';'

        current_statement.append(line.strip())
        if line.strip().endswith(';'):
            stmt = '\n'.join(current_statement).strip()
            if stmt:
                statements.append(stmt)
            current_statement = []
            
    if current_statement:
        stmt = '\n'.join(current_statement).strip()
        if stmt:
            statements.append(stmt)
            
    return statements

def run_init(host, port, user, password, db_name, run_seed=True):
    print("=" * 60)
    print(" AttendEase: Database Initialization & Verification ")
    print("=" * 60)
    print(f" Connecting to MySQL server at {host}:{port} as '{user}'...")

    # Step 1: Connect to MySQL server without selecting DB first
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset="utf8mb4",
            autocommit=True
        )
        cursor = conn.cursor(buffered=True)
        print(" Connected to MySQL server successfully.")
    except Error as e:
        print(f"\n[ERROR] Failed to connect to MySQL: {e}")
        print("\nPlease check:")
        print("  1. Is MySQL Server running? (e.g. Service 'MySQL80')")
        print("  2. Did you enter the correct password in .env (DB_PASSWORD)?")
        print("  3. Run: python init_db.py --password your_password")
        return False

    # Step 2: Create database if not exists
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE `{db_name}`;")
        print(f" Database `{db_name}` is ready.")
    except Error as e:
        print(f"[ERROR] Failed to create or use database `{db_name}`: {e}")
        conn.close()
        return False

    # Step 3: Run schema.sql
    schema_path = os.path.join(basedir, 'schema.sql')
    print(f"\n Executing schema definition: {schema_path}...")
    schema_stmts = parse_sql_file(schema_path)
    
    success_count = 0
    for stmt in schema_stmts:
        try:
            cursor.execute(stmt)
            while conn.unread_result:
                conn.get_rows()
            success_count += 1
        except Error as e:
            # Ignore harmless warnings like dropping non-existent views
            if "Unknown table" in str(e) or "doesn't exist" in str(e):
                continue
            print(f"  [WARN/ERROR in statement]: {e}")
            print(f"  Statement snippet: {stmt[:100]}...\n")

    print(f" Schema created ({success_count} statements processed).")

    # Step 4: Run seed.sql if requested
    if run_seed:
        seed_path = os.path.join(basedir, 'seed.sql')
        print(f"\n Seeding realistic sample data: {seed_path}...")
        seed_stmts = parse_sql_file(seed_path)
        seed_success = 0
        for stmt in seed_stmts:
            try:
                cursor.execute(stmt)
                while conn.unread_result:
                    conn.get_rows()
                seed_success += 1
            except Error as e:
                print(f"  [WARN/ERROR in seed]: {e}")
        print(f" Seed data inserted ({seed_success} statements processed).")

    # Step 5: Verification & Summary
    cursor.execute("SHOW TABLES;")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"\n Verified Database Tables ({len(tables)} tables/views present):")
    for t in sorted(tables):
        cursor.execute(f"SELECT COUNT(*) FROM `{t}`")
        count = cursor.fetchone()[0]
        print(f"   • {t.ljust(30)} : {count} records")

    cursor.close()
    conn.close()

    # Update .env file with credentials if provided
    env_file = os.path.join(basedir, '.env')
    if os.path.exists(env_file) and password:
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                if line.startswith('DB_PASSWORD='):
                    new_lines.append(f"DB_PASSWORD={password}\n")
                elif line.startswith('DB_USER='):
                    new_lines.append(f"DB_USER={user}\n")
                elif line.startswith('DB_HOST='):
                    new_lines.append(f"DB_HOST={host}\n")
                elif line.startswith('DB_PORT='):
                    new_lines.append(f"DB_PORT={port}\n")
                else:
                    new_lines.append(line)
            with open(env_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(" Automatically synchronized credentials with .env file.")
        except Exception as e:
            print(f" Note: Could not update .env file: {e}")

    print("\n" + "=" * 60)
    print(" INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("Demo Logins Available (Password for all: Password@123):")
    print("  • Administrator : admin        (or email: admin@college.edu)")
    print("  • Faculty (CSE) : prof_alan    (or email: alan.turing@college.edu)")
    print("  • Faculty (CSE) : prof_grace   (or email: grace.hopper@college.edu)")
    print("  • Student       : alex_rivera  (or email: alex.r@college.edu)")
    print("  • Student       : priya_patel  (or email: priya.p@college.edu)")
    print("  • Student       : marcus_vance (or email: marcus.v@college.edu - <75% shortage alert)")
    print("=" * 60)
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Initialize AttendEase MySQL Database")
    parser.add_argument('--host', default=os.getenv('DB_HOST', 'localhost'), help="MySQL Host")
    parser.add_argument('--port', type=int, default=int(os.getenv('DB_PORT', 3306)), help="MySQL Port")
    parser.add_argument('--user', default=os.getenv('DB_USER', 'root'), help="MySQL User")
    parser.add_argument('--password', default=os.getenv('DB_PASSWORD', ''), help="MySQL Password")
    parser.add_argument('--database', default=os.getenv('DB_NAME', 'attendease_db'), help="Database Name")
    parser.add_argument('--no-seed', action='store_true', help="Do not insert sample seed data")
    
    args = parser.parse_args()
    
    success = run_init(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        db_name=args.database,
        run_seed=not args.no_seed
    )
    
    sys.exit(0 if success else 1)
