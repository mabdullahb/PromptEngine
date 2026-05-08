import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole
from app.models.subscription import Subscription, PlanType, SubscriptionStatus
from app.core.security import get_password_hash
from app.core.logging import logger

async def seed_data():
    async with AsyncSessionLocal() as db:
        # 1. Create Admin User
        admin_email = "admin@promptengine.ai"
        admin_user = await db.run_sync(lambda s: s.query(User).filter_by(email=admin_email).first())
        
        if not admin_user:
            admin_user = User(
                email=admin_email,
                hashed_password=get_password_hash("admin_secure_password_2026"),
                full_name="Platform Administrator",
                role=UserRole.ADMIN,
                is_active=True,
                has_onboarded=True
            )
            db.add(admin_user)
            await db.flush()
            
            # Create Team Subscription for Admin
            admin_sub = Subscription(
                user_id=admin_user.id,
                plan_type=PlanType.TEAM,
                status=SubscriptionStatus.ACTIVE
            )
            db.add(admin_sub)
            logger.info("Admin user and team subscription seeded.")
        
        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed_data())
