#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Tag Tamer's role-based tagger run by AWS Lambda

# Import AWS modules for python
import boto3
from boto3.dynamodb.conditions import Key, Attr
# Import JSON
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('roles')
    

    role_arn = event['userIdentity']['sessionContext']['sessionIssuer']['arn']
    #print("Role ARN: ", role_arn)
    resource_id = event['responseElements']['instancesSet']['items'][0]['instanceId'] 

    #Get a specified role and assigned tags 
    def get_role_tags(role_arn):
        response = dict()
        response = table.get_item(
            Key={
                'role_arn': role_arn
            },
            ProjectionExpression="tags"
        )
        tags = list()
        tags = response['Item']['tags']
        return tags

    role_tags = get_role_tags(role_arn)

    creator = dict()
    creator["Key"] = "Created by"
    creator["Value"] = role_arn

    role_tags.append(creator)
    
    #print("Role & Tags", role_tags)

    def set_resources_tags(resource_id, role_tags):

        selected_resource_type = boto3.resource('ec2')
        unit = 'instances'
        resources_updated_tags = dict()
        
        print("Resource ID:", resource_id)

        if unit == 'instances':
            try:
                resource_tag_list = []
                instance = selected_resource_type.Instance(resource_id)
                resource_tag_list = instance.create_tags(
                    Tags=role_tags
                )
                applied_tags = list()
                for tag in resource_tag_list:
                    tag_kv = {}
                    tag_kv["Key"] = tag.key
                    tag_kv["Value"] = tag.value
                    applied_tags.append(tag_kv)
                resources_updated_tags[resource_id] = applied_tags
            except:
                resources_updated_tags["No Resources Found"] = "No Tags Applied"
        return resources_updated_tags

    resource_tags = dict()
    resource_tags = set_resources_tags(resource_id, role_tags)
    #print("Resource ID & Tags: ", resource_tags)
    return {
        'statusCode': 200,
        'body': json.dumps(resource_tags)
    }
