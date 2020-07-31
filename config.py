#!/usr/bin/env python3

# copyright 2020 Bill Dry
# Getter & setter for AWS Config Rules

# Import AWS module for python
import boto3
# Import JSON
import json

# Define AWS Config class to get/set items using Boto3
class config:
    
    #Class constructor
    def __init__(self, region):
        self.region = region
        self.config_client = boto3.client('config', region_name=self.region)

    #Get REQUIRED_TAGS Config Rule name & input parameters
    def get_config_rule(self, config_rule_id):
        response = dict()
        all_config_rules = dict()
        response = self.config_client.describe_config_rules()
        all_config_rules = response['ConfigRules'][0]
        
        config_rule = dict()
        input_parameters_dict = dict()
        if all_config_rules['Source']['SourceIdentifier'] == 'REQUIRED_TAGS':
            input_parameters_dict = json.loads(all_config_rules['InputParameters'])
            config_rule['ConfigRuleName'] = all_config_rules['ConfigRuleName']
            for key, value in input_parameters_dict.items():
                config_rule[key] = value
        
        return config_rule

    #Get REQUIRED_TAGS Config Rule names & ID's
    def get_config_rules_ids_names(self):
        response = dict()
        all_config_rules = dict()
        response = self.config_client.describe_config_rules()
        all_config_rules = response['ConfigRules']

        config_rules_ids_names = dict()
        for configRule in all_config_rules:
            if configRule['Source']['SourceIdentifier'] == 'REQUIRED_TAGS':
                config_rules_ids_names[configRule['ConfigRuleId']] = configRule['ConfigRuleName']
        
        return config_rules_ids_names

    #Set REQUIRED_TAGS Config Rule
    def set_config_rules(self, tag_groups_keys_values, config_rule_id):
        
        # convert selected Tag Groups into JSON for Boto3:
        input_parameters_json = json.dumps(tag_groups_keys_values)
        
        self.config_client.put_config_rule(
            ConfigRule={
                'ConfigRuleId': config_rule_id,
                'InputParameters': input_parameters_json,
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'REQUIRED_TAGS'
                }    
            }
        )
