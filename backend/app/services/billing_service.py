import stripe
from typing import Optional
from app.core.config import settings
from app.models.subscription import PlanType, SubscriptionStatus
from app.core.logging import logger

stripe.api_key = settings.STRIPE_SECRET_KEY

class BillingService:
    def create_checkout_session(self, user_id: str, email: str, plan: PlanType):
        """Creates a Stripe Checkout Session for subscription."""
        # This is scaffolding, actual price IDs would come from config
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
                success_url="http://localhost:3000/dashboard?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:3000/dashboard/settings",
                metadata={"user_id": user_id, "plan": plan.value}
            )
            return session
        except Exception as e:
            logger.error(f"Stripe Session Error: {e}")
            raise

    def create_portal_session(self, customer_id: str):
        """Creates a billing portal session for managing subscriptions."""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url="http://localhost:3000/dashboard/settings",
            )
            return session
        except Exception as e:
            logger.error(f"Stripe Portal Error: {e}")
            raise

    def handle_webhook(self, payload: str, sig_header: str):
        """Handles Stripe webhook events."""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:
            logger.error(f"Webhook Signature Error: {e}")
            raise

        # Handle specific events
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Logic to update DB would go here via user_id in metadata
            logger.info(f"Subscription completed for user {session.metadata.get('user_id')}")
            
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            # Logic to cancel in DB
            logger.info(f"Subscription deleted for customer {subscription.customer}")

        return event

billing_service = BillingService()
