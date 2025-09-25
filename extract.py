from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv, find_dotenv
from faker import Faker
import csv
import random
import string
import os

load_dotenv(find_dotenv())


# Load credentials from environment variables
project_id = os.getenv('GCP_PROJECT_ID')
bucket_name = os.getenv('GCP_BUCKET_NAME')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

credentials = service_account.Credentials.from_service_account_file(credentials_path)

"""
num_employees = 100

fake = Faker()

password_characters = string.ascii_letters + string.digits + "m"



with open("employee_data.csv", mode='w', newline='') as file:
    fieldNames = ['first_name', 'last_name', 'job_title', 'department', 'email', 'address', 'phone_number', 'salary', 'password']
    writer = csv.DictWriter(file, fieldnames=fieldNames)

    writer.writeheader()
    for _ in range(num_employees):
        emp = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "job_title": fake.job(),
            "department": fake.job(),
            "email": fake.email(),
            "address": fake.city(),
            "phone_number": fake.phone_number(),
            "salary": fake.random_number(digits=5),
            "password": ''.join(random.choice(password_characters) for _ in range(8))
        }
        writer.writerow(emp)

def file_upload_to_gcp(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")



if __name__ == "__main__":
    source_file_name = "employee_data.csv"
    destination_blob_name = "employee_data.csv"

    # Uploading the file to the blob storage
    file_upload_to_gcp(bucket_name, source_file_name, destination_blob_name)

"""

def upload_blob():
    local_dir = "input"

    client = storage.Client(credentials=credentials, project=project_id)
    bucket = client.bucket(bucket_name)

    filenames = os.listdir(local_dir)

    for filename in filenames:
        full_file_path = os.path.join(local_dir, filename)
        blob = bucket.blob(filename)
        with open(full_file_path, "r") as fl:
            blob.upload_from_string(fl.read())
        print(f"File {filename} is uploaded successfully....")

def upload_file_to_blob():
    local_dir = "input"

    client = storage.Client(credentials=credentials, project=project_id)
    bucket = client.bucket(bucket_name)

    filenames = os.listdir(local_dir)

    for filename in filenames:
        full_file_path = os.path.join(local_dir, filename)
        blob = bucket.blob(filename)
        with open(full_file_path, "r") as fl:
            blob.upload_from_string(fl.read())
        print(f"File {filename} is uploaded successfully....")

def list_blob():
    client = storage.Client(credentials=credentials, project=project_id)
    bucket = client.bucket(bucket_name)

    # List blobs in the bucket
    blobs = bucket.list_blobs()
    for blob in blobs:
        print(blob.name)

if __name__ == "__main__":
    # upload_blob()
    list_blob()
    upload_file_to_blob()