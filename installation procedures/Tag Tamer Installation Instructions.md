# How to install the Tag Tamer solution

Version - 1

Author: Bill Dry - bdry@amazon.com - +1-919-345-7347

Tag Tamer Installation Procedure

Before you begin (Prerequisites):

a) Identity the target AWS account where you would like to deploy Tag Tamer

b) Identify the EC2 Key Pair you will use to access the Tag Tamer Web App EC2 instance

c) Identify the IAM role that AWS CloudFormation will use to deploy DynamoDB, EC2 & IAM resources

d) Identify Certificate to use for ALB if Loadbalancer needs to be deployed in public subnet. If needed to install self-signed certificate, Instructions provided below.

e) Request access from Bill Dry bdry@amazon.com to this AMI --> ami-02a35aaef5d96cafb <-- for your target AWS account

Customer can either deploy Tagtamer solution in private subnet or public subnet. If being deployed in public, certificate is required for ALB setup.

# Solution1: EC2 deployed in Private subnet 

Step 1 - Download the AWS CloudFormation template at the following link.  It specifies the Tag Tamer solution infrastructure.

https://github.com/billdry/tag-tamer/blob/master/installation%20procedures/tagtamer_v2_private.yaml 

Step 2 - Deploy the CloudFormation Template downloaded in step 1 into your AWS account.  You will need an EC2 Key Pair, VPC, Private Subnet and a IAM Role with CloudFormation deployment permissions for DynamoDB, EC2 & IAM

Step 3 - Verify the correct operation of the Tag Tamer Web App by browsing to https://<EC2_INSTANCE_PUBLIC_IP_ADDRESS> Where "EC2_INSTANCE_PUBLIC_IP_ADDRESS" is listed in the CloudFormation outputs.

# Solution2: ALB deployed Public subnet and EC2 in Private subnet 

Step 1 - Download the AWS CloudFormation template at the following link.  It specifies the Tag Tamer solution infrastructure.

https://github.com/billdry/tag-tamer/blob/master/installation%20procedures/tagtamer_v2_public.yaml 

Step 2 - Deploy the CloudFormation Template downloaded in step 1 into your AWS account.  You will need an EC2 Key Pair, VPC, Private/Public Subnets, Certificate and a IAM Role with CloudFormation deployment permissions for DynamoDB, EC2 & IAM

Step 3 - Verify the correct operation of the Tag Tamer Web App by browsing to https://<EC2_INSTANCE_PUBLIC_IP_ADDRESS> Where "EC2_INSTANCE_PUBLIC_IP_ADDRESS" is listed in the CloudFormation outputs.

# How to create self-signed certificate and import to AWS account
```shell
openssl genrsa 2048 > my-aws-private.key
openssl req -new -x509 -nodes -sha1 -days 3650 -extensions v3_ca -key my-aws-private.key > my-aws-public.crt
openssl pkcs12 -inkey my-aws-private.key -in my-aws-public.crt -export -out my-aws-public.p12
aws acm import-certificate --certificate fileb://my-aws-public.crt --private-key fileb://my-aws-private.ke
```


END OF PROCEDURE
