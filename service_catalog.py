#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter & setter for AWS Service Catalog (SC) items.
# A Tag Group equals a group of SC TagOptions that all have the same Tag Key

# Import AWS module for python
import boto3
import botocore
# Import Collections module to manipulate dictionaries
import collections
from collections import defaultdict
# Import getter for TagOption Groups
import get_tag_groups
from get_tag_groups import get_tag_groups
# Import JSON parser
import json
# Import logging module
import logging

log = logging.getLogger(__name__)

# Define Service Catalog (SC) class to get/set items using Boto3
class service_catalog:
    
    #Class constructor
    def __init__(self, region):
        self.region = region
        self.service_catalog_client = boto3.client('servicecatalog', region_name=self.region)

    #Method to create an SC TagOption & return the TagOption ID
    def create_sc_tag_option(self, tag_key, tag_value):
        sc_response = dict()
        sc_response = self.service_catalog_client.create_tag_option(
            Key=tag_key,
            Value=tag_value
        )
        tag_option_id = sc_response['TagOptionDetail']['Id']
        return tag_option_id

    #Method to update an SC TagOption & return the TagOption ID
    def update_sc_tag_option(self, tag_key, tag_value):
        sc_response = dict()
        try:
            sc_response = self.service_catalog_client.update_tag_option(
                Key=tag_key,
                Value=tag_value
            )
            tag_option_id = sc_response['TagOptionDetail']['Id']
            return tag_option_id
        except botocore.exceptions.ClientError as error:
                log.error('Boto3 API returned error: \"%s\"', error)
    
    #Method to get all existing TagOptions from SC
    def get_sc_tag_options(self):
        sc_response = dict()
        try:
            sc_response = self.service_catalog_client.list_tag_options()
            return sc_response
        except botocore.exceptions.ClientError as error:
                log.error('Boto3 API returned error: \"%s\"', error)


    #Method to get all existing SC product template ID's & names
    def get_sc_product_templates(self):
        sc_response = dict()
        sc_response = self.service_catalog_client.search_products(
            SortBy='Title',
            SortOrder='ASCENDING'
        )
        sc_product_templates = list()
        sc_prod_templates_ids_names = dict()
        sc_product_templates = sc_response['ProductViewSummaries']
        for template in sc_product_templates:
            sc_prod_templates_ids_names[template['ProductId']] = template['Name']
        return sc_prod_templates_ids_names
    
    #Method to assign a Tag Group (TG) to an SC product_template 
    def assign_tg_sc_product_template(self, tag_group_name, sc_product_template_id):
        current_sc_tag_options = dict()
        sc_response = dict()
        tag_group_contents = dict()
        sc_tag_option_ids = list()
        sc_tag_option_values = list()

        #Instantiate a service catalog class instance
        sc_instance = service_catalog(self.region)

        #Get the key & values list for the requested Tag Group
        tag_group = get_tag_groups(self.region)
        tag_group_contents = tag_group.get_tag_group_key_values(tag_group_name)
        
        #Get the dictionary of current SC TagOptions
        current_sc_tag_options = sc_instance.get_sc_tag_options()

        #Get the TagOption ID's of all SC TagOptions that have the same key as the Tag Group parameter
        #If there's a key match, remember the corresponding value to see any Tag Group values are missing from SC
        for sc_tag_option in current_sc_tag_options['TagOptionDetails']:
            if sc_tag_option['Key'] == tag_group_contents['tag_group_key']:
                sc_tag_option_ids.append(sc_tag_option['Id'])
                sc_tag_option_values.append(sc_tag_option['Value'])

        #Create SC TagOptions for any Tag Group values not in SC for the specified Tag Group 
        if sc_tag_option_values:
            for value in sc_tag_option_values:
                if value not in tag_group_contents['tag_group_values']:
                    tag_option_id = sc_instance.create_sc_tag_option(tag_group_contents['tag_group_key'], value)
                    sc_tag_option_ids.append(tag_option_id)
        else:
            for tag_group_value in tag_group_contents['tag_group_values']:
                tag_option_id = sc_instance.create_sc_tag_option(tag_group_contents['tag_group_key'], tag_group_value)
                sc_tag_option_ids.append(tag_option_id)

        #Assign TagOption in the Tag Group to the specified SC product template if not already assigned 
        product_template_details = dict()
        product_template_details = self.service_catalog_client.describe_product_as_admin(
          Id=sc_product_template_id
        )
           
        existing_tag_options = list()
        existing_tag_options = product_template_details['TagOptions']
           
        existing_tag_option_ids = list()
        for tag_option in existing_tag_options:
            existing_tag_option_ids.append(tag_option['Id'])
       
        for to_id in sc_tag_option_ids:
            if to_id not in existing_tag_option_ids:
                sc_response = self.service_catalog_client.associate_tag_option_with_resource(
                    ResourceId=sc_product_template_id,
                    TagOptionId=to_id
                )
        
        #Return updated dictionary of TagOption keys & values for the SC product template
        product_template_details.clear()
        product_template_details = self.service_catalog_client.describe_product_as_admin(
          Id=sc_product_template_id
        )
           
        existing_tag_options.clear()
        existing_tag_options = product_template_details['TagOptions']
           
        existing_tag_option_key_values = defaultdict(list)
        for tag_option in existing_tag_options:
            existing_tag_option_key_values[tag_option['Key']].append(tag_option['Value'])
        
        return existing_tag_option_key_values