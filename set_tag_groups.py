#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Setter updating tag groups in DynamoDB

# Import AWS module for python
import boto3
from boto3.dynamodb.conditions import Key, Attr

#This class instantiates & updates Tag Tamer Tag Groups
class set_tag_group:

    #Class constructor
    def __init__(self, region):
        self.tag_groups = {}
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table('tag_groups')
    
    #Setter to instantiate a new Tag Group adding its tag key & range of tag values
    def create_tag_group(self, tag_group_name, tag_group_key_name, tag_group_value_options):
        put_item_response = self.table.put_item(
            Item={
                "tag_group_name": tag_group_name,
                "resource_type": "all",
                "key_name": tag_group_key_name,
                "key_values": tag_group_value_options
            },
            ReturnValues='NONE',
        )
        return put_item_response

    #Setter to update a tag's possible range of values
    def update_tag_group(self, tag_group_name, tag_group_key_name, tag_group_value_options):
        update_item_response = self.table.update_item(
            Key={
                "tag_group_name": tag_group_name
            },
            UpdateExpression="set resource_type = :rt, key_name = :kn, key_values = :kv",
            ExpressionAttributeValues={
                ":rt": "all",
                ":kn": tag_group_key_name,
                ":kv": tag_group_value_options
            },
            ReturnValues='NONE',
        )
        return update_item_response

