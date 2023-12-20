import pulumi
import pulumi_aws as aws

# Create a new security group that allows HTTP traffic on port 80.
security_group = aws.ec2.SecurityGroup('allow_http',
    description='Allow HTTP inbound traffic',
    egress=[aws.ec2.SecurityGroupEgressArgs(
        description='Allow all outbound traffic',
        from_port=0,
        to_port=0,
        protocol='-1',
        cidr_blocks=['0.0.0.0/0'],
    )],
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        description='Allow HTTP inbound traffic',
        from_port=80,
        to_port=80,
        protocol='tcp',
        cidr_blocks=['0.0.0.0/0'],
    )]
)

# Find the latest Ubuntu 20.04 AMI in the us-west-2 region.
ami = aws.ec2.get_ami(most_recent=True,
    owners=["099720109477"],  # Ubuntu's owner ID
    filters=[aws.ec2.GetAmiFilterArgs(
        name='name',
        values=['ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*'],
    )]
)

# UserData script to install NGINX.
user_data = """#!/bin/bash
apt update
apt install -y nginx
systemctl start nginx
"""

# Create a new EC2 instance, using the latest Ubuntu AMI and the user data to install NGINX.
instance = aws.ec2.Instance('web-server',
    instance_type='t2.micro',
    vpc_security_group_ids=[security_group.id],
    ami=ami.id,
    user_data=user_data,
    tags={
        'Name': 'web-server-instance'
    },
    # Associating a public IP address so that the NGINX server can be accessed over the internet.
    associate_public_ip_address=True,
)

# Export the public IP of the EC2 instance to access our NGINX server.
pulumi.export('public_ip', instance.public_ip)