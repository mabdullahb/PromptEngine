from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Initialize empty kwargs
engine_kwargs = {}

# PostgreSQL settings (Pooling is NOT supported by SQLite)
if not settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    engine_kwargs = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
    }
else:
    # SQLite specific fixes for async and threading
    # This prevents the "TypeError" in GitHub Actions
    engine_kwargs = {
        "connect_args": {"check_same_thread": False}
    }

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

    future=True,
    **engine_kwargs
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```
eof

### Step 2: Save the File
In VS Code, make sure you **Save** the file (press `Ctrl + S`). Once you save it, the red indicators in the editor should stabilize.

### Step 3: Run these Commands in the Terminal
Open your terminal at the bottom of VS Code and run these three commands exactly as written. This will clear the "red" status in Git and trigger the fix on GitHub.

1.  **Stage the fix:**
    ```bash
    git add backend/app/db/session.py
    ```
2.  **Commit the change:**
    ```bash
    git commit -m "fix: remove sqlalchemy pooling args for sqlite compatibility in CI"
    ```
3.  **Push to GitHub:**
    ```bash
    git push origin main