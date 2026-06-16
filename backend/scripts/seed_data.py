"""Seed default data: fix packages and admin user."""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.models.models import User, UserRole, FixPackage
from sqlalchemy import select
import bcrypt as _bcrypt

async def seed():
    print("🌱 Seeding default data...")
    async with AsyncSessionLocal() as db:
        # Check if admin exists
        result = await db.execute(select(User).where(User.email == "admin@velvethour.com"))
        admin = result.scalar_one_or_none()
        if not admin:
            admin = User(
                id="admin-001",
                email="admin@velvethour.com",
                password_hash=_bcrypt.hashpw(b"admin123", _bcrypt.gensalt()).decode(),
                name="Admin",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin)
            print("✅ Admin user created (admin@velvethour.com / admin123)")
        else:
            print("👤 Admin user already exists")

        # Check if fix packages exist
        result = await db.execute(select(FixPackage))
        existing = result.scalars().all()
        if not existing:
            packages = [
                FixPackage(id="quick_fix", name="Quick Fix", price_cents=2900,
                          estimated_days=1, is_bundle=False,
                          description="Simple text/code change for a single issue"),
                FixPackage(id="standard_fix", name="Standard Fix", price_cents=7900,
                          estimated_days=2, is_bundle=False,
                          description="Moderate complexity fix for one category"),
                FixPackage(id="category_fix", name="Category Fix", price_cents=14900,
                          estimated_days=3, is_bundle=False,
                          description="Full optimization of one audit category"),
                FixPackage(id="bundle_fix", name="Bundle Fix", price_cents=29900,
                          estimated_days=5, is_bundle=True,
                          description="3-5 related fixes across categories"),
            ]
            for pkg in packages:
                db.add(pkg)
            print("✅ Fix packages created (Quick $29, Standard $79, Category $149, Bundle $299)")
        else:
            print(f"👤 {len(existing)} fix packages already exist")

        await db.commit()
        print("🌱 Seed complete!")

if __name__ == "__main__":
    asyncio.run(seed())