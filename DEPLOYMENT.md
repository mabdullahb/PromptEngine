# PromptEngine Production Deployment Guide

This guide details the steps to deploy PromptEngine to a production environment using Docker and Nginx.

## Prerequisites
- Docker & Docker Compose
- Domain Name with SSL (Certbot/Cloudflare)
- Stripe Account (for billing)
- AI Provider API Keys (OpenAI, Groq, etc.)

## 1. Environment Configuration
Create a `.env` file in the root directory:
```env
# Database
POSTGRES_USER=secure_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=promptengine

# Security
SECRET_KEY=generate_a_long_random_string
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AI Providers
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Production
ENV=production
LOG_FORMAT=json
BACKEND_CORS_ORIGINS=["https://app.promptengine.ai"]
```

## 2. Infrastructure Setup
Use the production-ready compose file:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## 3. Database Initialization
Seed the initial admin account and plans:
```bash
docker exec -it promptengine_backend python -m app.db.seeds
```

## 4. Monitoring
- **Logs**: Access JSON logs via `docker logs promptengine_backend`.
- **Health**: Monitor `https://api.promptengine.ai/api/v1/health/detailed`.
- **Errors**: Configure `SENTRY_DSN` for real-time crash reporting.

## 5. Security Checklist
- [ ] Change all default passwords.
- [ ] Ensure `Strict-Transport-Security` is active.
- [ ] Validate Stripe webhook signature settings.
- [ ] Restrict database access to the internal network.
