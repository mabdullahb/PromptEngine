from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.api.deps import get_db, get_current_user, get_current_subscription
from app.models.user import User
from app.models.subscription import PlanType, Subscription
from app.services.billing_service import billing_service

router = APIRouter()

@router.get("/plans")
async def get_plans():
    """List available subscription plans."""
    return [
        {"id": "free", "name": "Free", "price": 0, "features": ["10 enhancements/day", "Community support"]},
        {"id": "pro", "name": "Pro", "price": 19.99, "features": ["1000 enhancements/day", "Priority support", "Early access"]},
        {"id": "team", "name": "Team", "price": 49.99, "features": ["Unlimited enhancements", "Shared workspace", "Custom models"]}
    ]

@router.post("/checkout/{plan}")
async def create_checkout(
    plan: PlanType,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a Stripe checkout session for a plan."""
    if plan == PlanType.FREE:
        raise HTTPException(status_code=400, detail="Cannot checkout for free plan")
        
    session = billing_service.create_checkout_session(
        user_id=str(current_user.id),
        email=current_user.email,
        plan=plan
    )
    return {"checkout_url": session.url}

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Webhook for Stripe events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = billing_service.handle_webhook(payload, sig_header)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/portal")
async def billing_portal(
    subscription: Subscription = Depends(get_current_subscription)
):
    """Create a Stripe billing portal session."""
    if not subscription.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No active Stripe customer found")
        
    session = billing_service.create_portal_session(subscription.stripe_customer_id)
    return {"portal_url": session.url}
