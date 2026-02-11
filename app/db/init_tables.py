# this code is to create tables in database

import asyncio
from app.db.session import engine
from app.db.base_class import Base
from app.models import expense, budget, user

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # create_all is a sync function, thats why we need to wrap it around ,run_sync

if __name__ == "__main__":
    asyncio.run(init_models())  
