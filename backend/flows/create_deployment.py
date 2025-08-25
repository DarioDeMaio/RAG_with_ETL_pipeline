from prefect.deployments import Deployment
from prefect.server.schemas.schedules import IntervalSchedule
from datetime import timedelta
from ingest_periodic import periodic_ingest

def main():
    schedule = IntervalSchedule(interval=timedelta(minutes=1))

    deployment = Deployment.build_from_flow(
        flow=periodic_ingest,
        name="12h-ingest",
        schedule=schedule,
        work_queue_name="default",
    )

    deployment.apply()

if __name__ == "__main__":
    main()