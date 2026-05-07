from app.db.base_class import Base
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.models.subscription import Subscription
from app.models.prompt import Prompt, PromptTemplate
from app.models.api_usage import ApiUsageLog

# This ensures all models are imported and registered with Base.metadata before Alembic imports Base.
