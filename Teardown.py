import boto3
import time
def teardown_infrastructure(instance_ids,load_balancer_arn,target_group_arn,asg_name,sns_topic_arns):
    # Initialize clients
    ec2 = boto3.client('ec2')
    elb = boto3.client('elbv2')
    autoscaling = boto3.client('autoscaling')
    sns = boto3.client('sns')

    # Example: Terminate EC2 instances
    instance_ids=[instance_ids]
    ec2.terminate_instances(InstanceIds=instance_ids)
    print(f"Terminated EC2 instances: {', '.join(instance_ids)}")

    # Example: Delete the Application Load Balancer
    elb.delete_load_balancer(LoadBalancerArn=load_balancer_arn)
    print(f"Deleted ALB: {load_balancer_arn}")
    time.sleep(1*60)
    
    #Delete Target Group
    elb.delete_target_group(TargetGroupArn = target_group_arn)


    print(f"Deleted TG: {target_group_arn}")

    # Example: Delete the Auto Scaling Group
    autoscaling.delete_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        ForceDelete=True  # Force deletes the ASG even if instances are running
    )
    print(f"Deleted Auto Scaling Group: {asg_name}")

    # Example: Delete SNS topic
    for topic_arn in sns_topic_arns.values():
        sns.delete_topic(TopicArn=topic_arn)
        print(f"Deleted SNS Topic: {topic_arn}")
