from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv, find_dotenv
from faker import Faker
import csv
import os
import string
import random
from datetime import datetime


fake = Faker()
password_characters = string.ascii_letters + string.digits + "m"
num_employees = 100

today_ = datetime.today().strftime("%d%m%Y")
CSV_LOCAL = f"employees_data_{today_}.csv"
OBJECT_NAME = f"employees_data/{CSV_LOCAL}"


def make_csv(path: str, rows: int = 100):
    with open(path, "w", newline='') as file:
        filenames = ['first_name', 'last_name', 'job_title', 'department', 'email', 'address', 'phone_number', 'salary', 'password']
        writer = csv.DictWriter(file, fieldnames=filenames)


        writer.writeheader()

        for _ in range(rows):
            writer.writerow({
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "job_title": fake.job(),
                "department": fake.job(),
                "email": fake.email(),
                "address": fake.city(),
                "phone_number": fake.phone_number(),
                "salary": fake.random_number(digits=5),
                "password": ''.join(random.choice(password_characters) for _ in range(8))
            })
            

def file_upload_to_gcs(project_id, credentials, bucket_name, source_file_name, destination_blob_name):

    if isinstance(credentials, str):
        credentials = service_account.Credentials.from_service_account_file(credentials)

    client = storage.Client(project=project_id, credentials=credentials)
    bucket = client.bucket(bucket_name)

    print("writing the fiel")
    blob = bucket.blob(destination_blob_name)

    # Uploading the file
    blob.upload_from_filename(source_file_name)
    
    print(f"File uploaded {source_file_name} to gs://{bucket_name}{destination_blob_name} successfully....")


def list_blob(project_id, credentials, bucket_name):

    if isinstance(credentials, str):
        credentials = service_account.Credentials.from_service_account_file(credentials)

    client = storage.Client(project=project_id, credentials=credentials)
    
    for b in client.list_blobs(bucket_name):
        print(b.name)

if __name__ == "__main__":

    load_dotenv(find_dotenv())

    # Load credentials
    project_id = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not all([project_id, bucket_name, credentials_path]):
        raise RuntimeError("Missing env vars: GCP_PROJECT, GCP_BUCKET_NAME, GOOGLE_APPLICATION_CREDENTIALS")

    make_csv(CSV_LOCAL, num_employees)
    
    creds = service_account.Credentials.from_service_account_file(credentials_path)
    

    file_upload_to_gcs(project_id, creds, bucket_name, CSV_LOCAL, OBJECT_NAME)
    
    # list_blob(project_id, creds, bucket_name)