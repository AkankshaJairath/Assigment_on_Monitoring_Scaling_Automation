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

# Launch an EC2 instance and configure it as a web server:
def create_ec2_instance():
    ec2 = boto3.resource('ec2', region_name=region)
    try:
        instances = ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName=keypair_name,
            SecurityGroupIds=[security_group_id],
            UserData='''#!/bin/bash
            sudo apt-get update -y
            sudo apt-get install nginx -y
            sudo systemctl start nginx
            sudo systemctl enable nginx
            echo "Hello World from $(hostname -f)" | sudo tee /usr/share/nginx/html/index.html
            ''',
            TagSpecifications=[
                {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': instance_name},
                    ]
                }
            ]  
        )
        instance = instances[0]
        instance.wait_until_running()
        instance.reload()
        if instance.state['Name'] == 'running':
            print(f"Instance '{instance.id}' created and running successfully.")
            return instance.id
        else:
            print(f"Instance '{instance.id}' creation failed.")
    except ClientError as e:
        print(f"Unexpected error: {e}")

#instance_id=create_ec2_instance()