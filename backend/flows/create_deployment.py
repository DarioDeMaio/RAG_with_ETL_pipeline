from prefect.deployments import Deployment
from prefect.server.schemas.schedules import IntervalSchedule
from datetime import timedelta
from ingest_periodic import ingest_periodic
import os
import dotenv

dotenv.load_dotenv()

def main():
    schedule = IntervalSchedule(interval=timedelta(minutes=2))

    deployment = Deployment.build_from_flow(
        flow=ingest_periodic,
        name="12h-ingest",
        schedule=schedule,
        work_queue_name="default",
        parameters={
            "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME")
        }
    )

    deployment.apply()

if __name__ == "__main__":
    main()