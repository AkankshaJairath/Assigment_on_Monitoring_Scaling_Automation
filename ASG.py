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

# Auto Scaling Group (ASG) Configuration
def create_auto_scaling_group(target_group_arn):
    autoscaling = boto3.client('autoscaling', region_name=region)
    try:
        # Create Auto Scaling Group using the Launch Template
        autoscaling.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchTemplate={
                'LaunchTemplateName': template_name,
                'Version': '$Latest'  # Use the latest version of the template
            },
            MinSize=0,
            MaxSize=2,
            DesiredCapacity=0,
            VPCZoneIdentifier=subnet_id,
            TargetGroupARNs=[target_group_arn]
        )
        print("Auto Scaling Group created successfully.")
        # Configure scaling policies for CPU utilization
        scaling_policy = autoscaling.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName='scale-out',
            PolicyType='TargetTrackingScaling',
            TargetTrackingConfiguration={
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ASGAverageCPUUtilization'
                },
                'TargetValue': 50.0
            }
        )
        print(f"CPU utilization scaling policy created successfully: {scaling_policy['PolicyARN']}")
        # Configure scaling policies for network traffic
        scaling_policy = autoscaling.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName='scale-out-network-traffic',
            PolicyType='TargetTrackingScaling',
            TargetTrackingConfiguration={
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ASGAverageNetworkIn'
                },
                'TargetValue': 1000000  # Adjust the target value as needed
            }
        )
        print(f"Network traffic scaling policy created successfully: {scaling_policy['PolicyARN']}")
    except Exception as e:
        print(f"Error: {e}")

#create_auto_scaling_group()