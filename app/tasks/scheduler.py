from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

jobstores = {
    "default": SQLAlchemyJobStore(url="postgresql+psycopg2://user:password@db:5432/database")
}

job_defaults = {
    "coalesce": False,
    "max_instances": 1,
}

scheduler = AsyncIOScheduler(jobstores=jobstores, job_defaults=job_defaults)

def schedule_product_update(artikul: str):
    scheduler.add_job(
        func=fetch_product_updates,
        trigger="interval",
        args=[artikul],
        seconds=1800,
        id=f"product_update_{artikul}",
        replace_existing=True,
    )

async def fetch_product_updates(artikul: str):
    print(f"Fetching updates for product {artikul}")
