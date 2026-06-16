"""Database setup script - run once to create all tables."""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import init_db, close_db


async def main():
    print("🗄️  Initializing Velvet Hour Audit database...")
    await init_db()
    print("✅ Database tables created successfully!")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())