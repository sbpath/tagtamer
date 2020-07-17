How to install the Tag Tamer solution

Version - 1

Author: Bill Dry - bdry@amazon.com - +1-919-345-7347

Tag Tamer Installation Procedure

Before you begin (Prerequisites):

a) Identity the target AWS account where you would like to deploy Tag Tamer

b) Identify the EC2 Key Pair you will use to access the Tag Tamer Web App EC2 instance

c) Identify the IAM role that AWS CloudFormation will use to deploy DynamoDB, EC2 & IAM resources

d) Request access from Bill Dry bdry@amazon.com to this AMI --> ami-019b202a2877f4671 <-- for your target AWS account

Step 1 - Download the AWS CloudFormation template at the following link.  It specifies the Tag Tamer solution infrastructure.

https://github.com/billdry/tag-tamer/blob/master/installation%20procedures/tagtamer-infrastructure.template

Step 2 - Deploy the CloudFormation Template downloaded in step 1 into your AWS account.  You will need an EC2 Key Pair and a IAM Role with CloudFormation deployment permissions for DynamoDB, EC2 & IAM

Step 3 - Verify the correct operation of the Tag Tamer Web App by browsing to https://<EC2_INSTANCE_PUBLIC_IP_ADDRESS> Where "EC2_INSTANCE_PUBLIC_IP_ADDRESS" is listed in the CloudFormation outputs.

END OF PROCEDURE
