import stripe
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.subscription import PlanType, SubscriptionStatus, Subscription
from app.core.logging import logger

stripe.api_key = settings.STRIPE_SECRET_KEY

class BillingService:
    # Map Stripe Price IDs to Plan Types
    # In production, these would be in environment variables
    PRICE_TO_PLAN = {
        "price_pro_id": PlanType.PRO,
        "price_team_id": PlanType.TEAM
    }

    async def create_checkout_session(self, user_id: str, email: str, plan: PlanType):
        """Creates a Stripe Checkout Session for subscription."""
        price_ids = {
            PlanType.PRO: "price_pro_id",
            PlanType.TEAM: "price_team_id"
        }
        
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email=email,
                line_items=[{
                    'price': price_ids.get(plan),
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{settings.BACKEND_CORS_ORIGINS[0]}/dashboard?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.BACKEND_CORS_ORIGINS[0]}/dashboard/settings",
                metadata={"user_id": user_id, "plan": plan.value}
            )
            return session
        except Exception as e:
            logger.error(f"Stripe Session Error: {e}")
            raise

    async def create_portal_session(self, customer_id: str):
        """Creates a billing portal session for managing subscriptions."""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=f"{settings.BACKEND_CORS_ORIGINS[0]}/dashboard/settings",
            )
            return session
        except Exception as e:
            logger.error(f"Stripe Portal Error: {e}")
            raise

    async def get_invoices(self, customer_id: str) -> List[dict]:
        """Fetches invoice history for a customer."""
        try:
            invoices = stripe.Invoice.list(customer=customer_id, limit=10)
            return [
                {
                    "id": inv.id,
                    "amount": inv.amount_paid / 100,
                    "currency": inv.currency,
                    "status": inv.status,
                    "date": inv.created,
                    "pdf": inv.invoice_pdf
                } for inv in invoices.data
            ]
        except Exception as e:
            logger.error(f"Fetch Invoices Error: {e}")
            return []

    async def sync_subscription(self, db: AsyncSession, stripe_sub_id: str):
        """Synchronizes database subscription state with Stripe."""
        try:
            stripe_sub = stripe.Subscription.retrieve(stripe_sub_id)
            customer_id = stripe_sub.customer
            
            # Find subscription in DB
            query = select(Subscription).where(Subscription.stripe_subscription_id == stripe_sub_id)
            result = await db.execute(query)
            db_sub = result.scalar_one_none()
            
            if not db_sub:
                logger.warning(f"Subscription {stripe_sub_id} not found in DB for sync.")
                return

            # Map status
            status_map = {
                "active": SubscriptionStatus.ACTIVE,
                "trialing": SubscriptionStatus.ACTIVE,
                "past_due": SubscriptionStatus.PAST_DUE,
                "canceled": SubscriptionStatus.CANCELED,
                "incomplete": SubscriptionStatus.PAST_DUE
            }
            
            db_sub.status = status_map.get(stripe_sub.status, SubscriptionStatus.CANCELED)
            db_sub.current_period_end = stripe_sub.current_period_end
            
            # Update plan if changed
            price_id = stripe_sub['items']['data'][0]['price']['id']
            db_sub.plan_type = self.PRICE_TO_PLAN.get(price_id, PlanType.FREE)
            
            await db.commit()
            logger.info(f"Synced subscription {stripe_sub_id} for user {db_sub.user_id}")
            
        except Exception as e:
            logger.error(f"Sync Subscription Error: {e}")

    async def handle_webhook(self, db: AsyncSession, payload: str, sig_header: str):
        """Processes Stripe webhook events and updates database."""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:
            logger.error(f"Webhook Signature Error: {e}")
            raise

        event_type = event['type']
        data_object = event['data']['object']

        if event_type == 'checkout.session.completed':
            user_id = data_object['metadata'].get('user_id')
            stripe_sub_id = data_object.get('subscription')
            customer_id = data_object.get('customer')
            
            if user_id:
                query = select(Subscription).where(Subscription.user_id == user_id)
                result = await db.execute(query)
                db_sub = result.scalar_one_none()
                
                if db_sub:
                    db_sub.stripe_subscription_id = stripe_sub_id
                    db_sub.stripe_customer_id = customer_id
                    await db.commit()
                    await self.sync_subscription(db, stripe_sub_id)

        elif event_type in ['customer.subscription.updated', 'customer.subscription.deleted']:
            await self.sync_subscription(db, data_object['id'])

        elif event_type == 'invoice.payment_failed':
            # Potentially notify user via email
            logger.warning(f"Payment failed for customer {data_object['customer']}")

        return event

billing_service = BillingService()
