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

# SNS Notifications:
def create_sns_topic(topic_name):
    try:
        sns = boto3.client('sns')
        response = sns.create_topic(Name=topic_name)
        print(f"Successfully created topic '{topic_name}' with ARN: {response['TopicArn']}")
        return response['TopicArn']
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

def subscribe_lambda_to_topic(topic_arn, lambda_arn):
    try:
        sns = boto3.client('sns')
        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol='lambda',
            Endpoint=lambda_arn
        )
        print(f"Successfully subscribed Lambda function to topic {topic_arn} with subscription ARN: {response['SubscriptionArn']}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
'''
topics = ['HealthIssues', 'ScalingEvents', 'HighTraffic']
topic_arns = {}

# Create topics and store their ARNs
for topic in topics:
    arn = create_sns_topic(topic)
    if arn:
        topic_arns[topic] = arn
# Subscribe Lambda function to topics
lambda_arn = 'arn:aws:lambda:us-west-2:975050024946:function:Infra_healthcheck'
for topic_arn in topic_arns.values():
    subscribe_lambda_to_topic(topic_arn, lambda_arn)
'''