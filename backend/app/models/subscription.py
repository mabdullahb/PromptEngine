from sqlalchemy import Column, String, ForeignKey, Enum, DateTime, Uuid
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class PlanType(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    TEAM = "team"

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"

class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    plan_type = Column(Enum(PlanType), default=PlanType.FREE, nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="subscription")
