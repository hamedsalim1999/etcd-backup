import os
import boto3
import logging
from botocore.exceptions import ClientError
import os
env_endpoint_url = os.environ.get('ENDPOINT_URL')
env_aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
env_aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
env_file_path= os.environ.get('FILE_PATH')
env_object_name = os.environ.get('OBJECT_NAME')
def upload(env_endpoint_url,env_aws_access_key_id,env_aws_secret_access_key,env_file_path,env_object_name):
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
            bucket = s3_resource.Bucket('etcd-backup')
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