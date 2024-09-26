from s3 import create_s3_bucket
from EC2 import create_ec2_instance
from ELB import create_load_balancer_and_register_targets
from ASG import create_auto_scaling_group
from SNS import create_sns_topic,subscribe_lambda_to_topic
from Teardown import teardown_infrastructure
import time
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



create_s3_bucket()

instance_id=create_ec2_instance()
print(f"Instance id = {instance_id}")
load_balancer_output=create_load_balancer_and_register_targets(instance_id=instance_id)
load_balancer_arn = load_balancer_output[0]
target_group_arn = load_balancer_output[1]

ASG=create_auto_scaling_group(target_group_arn=target_group_arn)
print(ASG)



# Topic Creation
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
print(f"printing topic arn before assignment: \n{topic_arns}")



#Waiting for an hour before terminating the infrastructure
time.sleep(60*60)

#
#Terminating the infrastructure.......
#
teardown_infrastructure(instance_ids=instance_id,
                        load_balancer_arn=load_balancer_arn,
                        target_group_arn=target_group_arn,
                        asg_name=asg_name,
                        sns_topic_arns=topic_arns)