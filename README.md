# Assigment_on_Monitoring_Scaling_Automation

A system that automatically manages the lifecycle of a web application hosted on  EC2 instances, monitors its health, and reacts to changes in traffic by scaling resources.  Furthermore, administrators receive notifications regarding the infrastructure's health and scaling events

This project provides a fully automated system for deploying, managing, and scaling a web application on AWS using **boto3**. The system includes EC2 instances for hosting the web application, an Application Load Balancer (ALB), Auto Scaling Groups (ASG) for dynamic scaling, and SNS notifications for real-time alerts on infrastructure health and scaling events.

## Features

- **S3 for Static Files**: Automatically creates an S3 bucket to store the web application's static assets.
- **EC2 Instances**: Launches and configures EC2 instances as web servers (e.g., Apache or Nginx).
- **Application Load Balancer (ALB)**: Configures an ALB to distribute traffic across the EC2 instances.
- **Auto Scaling Group (ASG)**: Automatically scales the number of EC2 instances based on traffic and CPU usage.
- **SNS Notifications**: Sends notifications to administrators for infrastructure health issues and scaling events.
- **Infrastructure Automation**: A single Python script deploys and tears down the entire infrastructure.

### 1. Web Application Deployment: 

- Create an S3 bucket to store your web application's static files
- ### s3.py: Create S3 bucket "s31-deploywebapp"
- S3 Policy:
- {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::s31-deploywebapp/*"
        }
    ]
}
- Off all public access
- Enabled Static website hosting

- ### EC2.py:  Uses boto3 to launch an EC2 instance with a specific AMI, and configure it to act as a web server (Nginx).

- # Deploy the Web Application on EC2: Once the EC2 instance is running, Copy web application files from S3 or from a local repository onto the EC2 instance

### 2. Load Balancing with ELB: 

- # ELB.py: Create an Application Load Balancer (ALB): Using boto3, create an ALB, Target Group and Listener
- # Register EC2 Instances to ALB.

### 3.Auto Scaling Group (ASG) Configuration:

- # ASG.py : Create an Auto Scaling Group (ASG)  Using `boto3`and deployed EC2 instance as a template. 

### 4. SNS Notifications: 

 - # SNS.py :Set up different SNS topics for different alerts (e.g., health issues, scaling events, high traffic).
 - # lambda.py : Integrate SNS with Lambda so that administrators receive SMS or email notifications.

### 5. Infrastructure Automation: 

 - # infra_automation.py : A single script using boto3 that creates entire infrastructure and Teardown everything (refer Teardown.py as well) when application is no longer needed ( as per script it will decommsion after 1 hour)



  




