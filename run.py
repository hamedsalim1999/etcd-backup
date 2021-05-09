from datetime import datetime
from botocore.exceptions import ClientError
import etcd3
import json
import os
import sqlite3
import boto3
import logging
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


etcd_ip = os.getenv("ETCD_IP_ADDR")
etcd_port =os.getenv("ETCD_PORT")
env_endpoint_url = os.getenv("ENDPOINT_URL")
env_aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
env_aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
env_bucket_name = os.getenv("BUCKET_NAME")

# connecting to etcd database 
def etcd_connect(etcd_ip,etcd_port):
    etcd = etcd3.client(etcd_ip,etcd_port)
    return etcd.get_all()

# create sql file and connect to sql and crate table 
def sqlcon(dbname):
    try:
        sqliteConnection = sqlite3.connect(f'{dbname}.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        cursor.execute("CREATE TABLE IF NOT EXISTS etcd (key TEXT, value TEXT)")
        return cursor
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)

# insert obj to sql file 
def etcd_data_to_sql(obj,sql):
    for val,metadata in obj:
        sql.execute("INSERT INTO etcd (key , value) VALUES (?, ?)",(metadata.key.decode('utf-8'),val.decode('utf-8')))

# convert etcd file to json file 
def etcd_data_to_json(obj,file_name):
    json_dic ={}
    for val, metadata in obj:
        json_dic.update({metadata.key.decode('utf-8'):val.decode('utf-8')}) 
    with open(f'{file_name}.json', 'w') as json_file:
        json.dump(json_dic, json_file)
# upload date on ceph bucket 
def upload(env_endpoint_url,env_aws_access_key_id,env_aws_secret_access_key,env_file_path,env_object_name,bucket_name):
    logging.basicConfig(level=logging.INFO)
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=env_endpoint_url,
            aws_access_key_id=env_aws_access_key_id,
            aws_secret_access_key=env_aws_secret_access_key
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket = s3_resource.Bucket(bucket_name)
            file_path = env_file_path
            object_name = env_object_name
            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='private',
                    Body=file,
                    Key=object_name
                )
        except ClientError as e:
            logging.error(e)

# set datetime for write json and databsae file with time name 

obj = etcd_connect(etcd_ip,etcd_port)

datetime_name= datetime.now().strftime("%d. %B %Y %I:%M%p")

sqlfile = sqlcon(datetime_name)

etcd_data_to_sql(obj,datetime_name)

etcd_data_to_json(obj,datetime_name)

upload(env_endpoint_url,env_aws_access_key_id,env_aws_secret_access_key,f"{datetime_name}.db",f"/{datetime_name}.db",env_bucket_name)
upload(env_endpoint_url,env_aws_access_key_id,env_aws_secret_access_key,f"{datetime_name}.json",f"/{datetime_name}.json",env_bucket_name)