from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from app.models.api_usage import ApiUsageLog
from app.models.prompt import Prompt

class UsageService:
    PROVIDER_RATES = {
        "openai": {"prompt": 0.000005, "completion": 0.000015}, # $5/$15 per 1M
        "groq": {"prompt": 0.00000005, "completion": 0.00000005}, # $0.05 per 1M
        "gemini": {"prompt": 0.0000035, "completion": 0.0000105},
        "openrouter": {"prompt": 0.000002, "completion": 0.000006},
    }

    async def get_user_stats(self, db: AsyncSession, user_id: str):
        """Aggregates usage stats for a user over the last 30 days."""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # 1. Total prompts enhanced
        prompt_count_query = select(func.count(Prompt.id)).where(
            and_(Prompt.user_id == user_id, Prompt.created_at >= thirty_days_ago)
        )
        prompt_count = (await db.execute(prompt_count_query)).scalar() or 0

        # 2. Total tokens and estimated cost
        usage_query = select(
            ApiUsageLog.provider,
            func.sum(ApiUsageLog.prompt_tokens).label("prompt_sum"),
            func.sum(ApiUsageLog.completion_tokens).label("completion_sum"),
            func.sum(ApiUsageLog.total_tokens).label("total_sum")
        ).where(
            and_(ApiUsageLog.user_id == user_id, ApiUsageLog.created_at >= thirty_days_ago)
        ).group_by(ApiUsageLog.provider)
        
        usage_results = (await db.execute(usage_query)).all()
        
        total_tokens = 0
        total_cost = 0.0
        
        for row in usage_results:
            provider = row.provider.lower()
            total_tokens += row.total_sum or 0
            
            rates = self.PROVIDER_RATES.get(provider, self.PROVIDER_RATES["openai"])
            cost = (row.prompt_sum * rates["prompt"]) + (row.completion_sum * rates["completion"])
            total_cost += cost

        # 3. Efficiency / Time Saved (Approx 5 mins per manual prompt engineering session)
        time_saved_minutes = prompt_count * 5

        return {
            "period": "Last 30 Days",
            "total_prompts": prompt_count,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(total_cost, 4),
            "time_saved_hours": round(time_saved_minutes / 60, 1)
        }

usage_service = UsageService()
