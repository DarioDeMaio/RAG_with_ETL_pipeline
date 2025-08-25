from prefect import flow, task
import boto3
import os
from ingest.add_to_db import update_croma_db

@task
def list_minio_file(bucket_name: str) -> list:
    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
    )
    paginator = s3.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=bucket_name):
        if "Contents" in page:
            for obj in page["Contents"]:
                keys.append(obj["Key"])
    return keys

@task
def process_file(bucket_name: str, key: str) -> None:
    update_croma_db(bucket_name, key, dest="tmp")

@flow
def ingest_periodic(bucket_name: str) -> None:
    keys = list_minio_file(bucket_name)
    for key in keys:
        process_file(bucket_name, key)