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

# Deploy the web application onto the EC2 instance:

# Load Balancing with ELB
def create_load_balancer_and_register_targets(instance_id):
    
    elbv2 = boto3.client('elbv2', region_name=region)
    try:
        # Create Load Balancer
        response_lb = elbv2.create_load_balancer(
            Name=lb_name,
            Subnets=[subnet_id1, subnet_id2],
            SecurityGroups=[security_group_id],
            Scheme='internet-facing',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': lb_name
                },
            ],
            Type='application',
            IpAddressType='ipv4'
        )
        load_balancer_arn=response_lb['LoadBalancers'][0]['LoadBalancerArn']
        print(f"Load Balancer created successfully: {response_lb['LoadBalancers'][0]['LoadBalancerArn']}")
        # Create Target Group
        response_tg = elbv2.create_target_group(
            Name=tg_name,
            Protocol='HTTP',
            Port=80,
            VpcId=vpc_id,
            HealthCheckProtocol='HTTP',
            HealthCheckPort='80',
            HealthCheckPath='/',
            TargetType='instance'
        )
        print(f"Target Group created successfully: {response_tg['TargetGroups'][0]['TargetGroupArn']}")
        target_group_arn=response_tg['TargetGroups'][0]['TargetGroupArn']
        # Register target group
        response_reg = elbv2.register_targets(
            TargetGroupArn=response_tg['TargetGroups'][0]['TargetGroupArn'],
            Targets=[
                {
                    'Id': instance_id,
                    'Port': 80
                },
            ]
        )
        print(f"Instance {instance_id} registered successfully in the target group.")
    except Exception as e:
        print(f"Error: {e}")
    # Create a listener
    elbv2.create_listener(LoadBalancerArn=load_balancer_arn,Protocol='HTTP',Port=80,
    DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group_arn}]
    )
    outputs = [load_balancer_arn,target_group_arn]
    return outputs 

#create_load_balancer_and_register_targets(instance_id)