import boto3
from botocore.exceptions import ClientError
import json

def lambda_handler(event, context):
    sns = boto3.client('sns')
    message = event['Records'][0]['Sns']['Message']
    subject = event['Records'][0]['Sns']['Subject']
    # Define the administrator's email and phone number
    admin_email = 'akanshajairath123@gmail.com'
    admin_phone = '+1234567890'
    try:
        # Send email notification
        sns.publish(
            TopicArn='arn:aws:sns:us-west-2:975050024946:HealthIssues',
            Message=message,
            Subject=subject
        )
        print(f"Successfully sent email notification to {admin_email}")
        # Send SMS notification
        sns.publish(
            PhoneNumber=admin_phone,
            Message=message
        )
        print(f"Successfully sent SMS notification to {admin_phone}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return {
        'statusCode': 200,
        'body': json.dumps('Notifications sent successfully!')
    }