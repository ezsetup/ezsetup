import boto3

ec2 = boto3.resource('ec2', aws_access_key_id='AWS_ACCESS_KEY_ID',
                     aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
                     region_name='us-west-2')

images = ec2.images.filter(Filters=[{
    'Name': 'name',
    'Values': ['Image Name']
}])
