import boto3
from botocore.exceptions import ClientError

# Replace with your actual values
region='us-west-2'
vpc_id='vpc-0321f38a7b594180d'
subnet_id='subnet-03ca36de9a927fe8e'
subnet_id1='subnet-03ca36de9a927fe8e'
subnet_id2='subnet-06bd72b2e4cb41d10'
security_group_id='sg-0effcd90abb742125'
keypair_name='arpit-key-ec2'
image_id='ami-0e42b3cc568cd07e3'
instance_type='t4g.micro'
template_name='arpit-asg-template'
bucket_name='s3-deploywebapp'
instance_name='EC2-DeployWebApp'
lb_name='LB-DeployWebApp'
tg_name='TG-DeployWebApp'
asg_name='ASG-DeployWebApp'

# Create an S3 bucket
def create_s3_bucket():
    s3 = boto3.client('s3', region_name=region)
    try:
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f"Bucket '{bucket_name}' created successfully.")
            print("Uploading the index.html file to s3 bucket")
        else:
            print(f"Failed to create bucket '{bucket_name}'.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists and is owned by you.")
        elif error_code == 'BucketAlreadyExists':
            print(f"Bucket '{bucket_name}' already exists and is owned by someone else.")
        else:
            print(f"Unexpected error: {e}")
            
create_s3_bucket()


