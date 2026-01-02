import boto3    #for aws
import os
from src.constants import AWS_ACCESS_KEY_ID_ENV_KEY, AWS_SECRET_ACCESS_KEY_ENV_KEY, REGION_NAME


class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        """
        Docstring for __init__
        
        :param self: This class will use aws access key and secret access key from environment variables
        to create an S3 client and resource.
        """

        if S3Client.s3_client is None or S3Client.s3_resource is None:
            __access_key = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            __secret__access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

            if __access_key is None or __secret__access_key is None:
                raise Exception(f"Env variable for {AWS_ACCESS_KEY_ID_ENV_KEY} or {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set yet")
            

            S3Client.s3_resource = boto3.resource('s3',
                                                aws_access_key_id=__access_key,
                                                aws_secret_access_key=__secret__access_key,
                                                region_name=region_name
                                                )
            S3Client.s3_client = boto3.client('s3',
                                              aws_access_key_id=__access_key,
                                              aws_secret_access_key=__secret__access_key,
                                              region_name=region_name
                                              )
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client