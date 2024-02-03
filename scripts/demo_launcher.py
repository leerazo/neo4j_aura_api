#! /usr/bin/env python3

from dotenv import dotenv_values
import time


import os
import dotenv
import json
import subprocess
import datetime
import argparse
from urllib.parse import urljoin
import neo4j
import graphdatascience

# TEMP CONSTANTS
api_base = 'https://api.neo4j.io/'

# CHANGE THIS
#tmp_dir = '/Users/lrazo/.tmp' 
tmp_dir = '/Users/lrazo/Frigomex Dropbox/Lee Razo/__tech/sysadmin/tmp/neo4j_demo_launcher' 
deployment_dir = os.path.join(tmp_dir, 'demo_deployments')
credential_dir = os.path.join(tmp_dir, 'aura_credentials')
auth_dir = os.path.join(tmp_dir, 'aura_api_auth')

# I'll need to replace this later with either something interactive or a standard JSON template that will contain this information. 
default_cred_file = os.path.join(tmp_dir, "neo4j-api-creds.txt") 

cred_file = default_cred_file

"""
def list_tenants(access_token, api_base, tenant_id=None):
    #api_endpoint = 'https://api.neo4j.io/v1/tenants'

    api_endpoint = urljoin(api_base, '/v1/tenants')

    aura_tenants = {}

    if tenant_id:
        api_endpoint += '/' + tenant_id

    print()
    print('api_endpoint:', api_endpoint)
    print()

    list_cmd = "curl -s -X 'GET' '{}' -H 'accept: application/json' -H 'Authorization: Bearer {}'".format(api_endpoint, access_token)
    
    list_tenants = dict(json.loads(subprocess.check_output(list_cmd, shell=True)))['data']
    for item in list_tenants:
        aura_tenants[item['id']] = {}
        aura_tenants[item['id']]['id'] = item['id'] 
        aura_tenants[item['id']]['name'] = item['name'] 

    return aura_tenants


def tenant_info(access_token, api_base, tenant_id):
    api_endpoint = urljoin(api_base, '/v1/tenants/' + tenant_id)

    tenant_data = {}

    print()
    print('api_endpoint:', api_endpoint)
    print()

    info_cmd = "curl -s -X 'GET' '{}' -H 'accept: application/json' -H 'Authorization: Bearer {}'".format(api_endpoint, access_token)
#    print('info_cmd:')
#    print(info_cmd)

    tenant_info = json.loads(subprocess.check_output(info_cmd, shell=True))['data']
#    print('tenant_info:', tenant_info)

    print()
    for item in tenant_info:
        #print(item, '=', tenant_info[item])
        tenant_data[tenant_info['id']] = {}
        tenant_data[tenant_info['id']]['tenant_id'] = tenant_info['id']
        tenant_data[tenant_info['id']]['tenant_name'] = tenant_info['name'] 
        tenant_data[tenant_info['id']]['instance_configurations'] = list(tenant_info['instance_configurations'])

    return tenant_data


def list_instances(access_token, api_base, tenant_id=None):
    api_endpoint = urljoin(api_base, '/v1/instances') 

    aura_instances = {}

    print()
    print('api_endpoint:', api_endpoint)
    print()

    list_cmd = "curl -s -X 'GET' '{}' -H 'accept: application/json' -H 'Authorization: Bearer {}'".format(api_endpoint, access_token)
#    print('list_cmd:')
#    print(list_cmd)

    list_instances = json.loads(subprocess.check_output(list_cmd, shell=True))['data']
    print('aura_instances:')
    for instance in list_instances:
        print(instance)
        aura_instances[instance['id']] = {}
        aura_instances[instance['id']]['instance_id'] = instance['id'] 
        aura_instances[instance['id']]['instance_name'] = instance['name'] 
        aura_instances[instance['id']]['cloud_provider'] = instance['cloud_provider'] 
        aura_instances[instance['id']]['tenant_id'] = instance['tenant_id'] 

    return aura_instances


def instance_info(access_token, api_base, instance_id):
    api_endpoint = urljoin(api_base, '/v1/instances/' + instance_id)

    instance_data = {}

    print()
    print('api_endpoint:', api_endpoint)
    print()

    info_cmd = "curl -s -X 'GET' '{}' -H 'accept: application/json' -H 'Authorization: Bearer {}'".format(api_endpoint, access_token)

    api_response = json.loads(subprocess.check_output(info_cmd, shell=True))
    print('api_response:', api_response)

    if 'data' in api_response:
        response_data = api_response['data']
        print('response_data:')
        print(response_data)
        instance_status = response_data['status']
        print('instance_status:', instance_status)

    return response_data

def update_instance(access_token, api_base, instance_id, instance_name, instance_size):
    api_endpoint = urljoin(api_base, '/v1/instances/' + instance_id)

    print()
    print('api_endpoint:', api_endpoint)
    print()

    request_body = {}
    if instance_name:
        request_body['name'] = instance_name
    if instance_size:
        request_body['memory'] = str(instance_size) + "GB"

    json_request_body = json.dumps(request_body)
    print('json_request_body:', json_request_body)

    curl_cmd = "curl -s -X 'PATCH' '{}' -H 'accept: application/json' -H 'Authorization: Bearer {}' -H 'Content-Type: application/json'".format(api_endpoint, access_token)
    curl_cmd += " -d '{}'".format(json_request_body)
    print('curl_cmd:')
    print(curl_cmd)

    api_response = json.loads(subprocess.check_output(curl_cmd, shell=True))

    print('Instance updated:')
    print(api_response)


def delete_instance(access_token, api_base, instance_id):
    api_endpoint = urljoin(api_base, '/v1/instances/' + instance_id)

    print()
    print('api_endpoint:', api_endpoint)
    print()

    curl_cmd = "curl -s -X 'DELETE' '{}' -H 'accept: application/json' -H 'Authorization: Bearer {}'".format(api_endpoint, access_token)

    print("curl_cmd:")
    print(curl_cmd)

    api_response = json.loads(subprocess.check_output(curl_cmd, shell=True))

    print('api_response:')
    print(api_response)

    if 'data' in api_response:
        instance_id = api_response['data']['id']
        instance_name = api_response['data']['name']
        print('instance_id:', instance_id)
        print('instance_name:', instance_name)

        cred_filename = os.path.join(tmp_dir, 'Neo4j-' + instance_id + '-' + instance_name + '.txt')
        print('cred_filename:', cred_filename)
        
        # Delete the credential file if it still exists
        print('Deleting instance credential file {}'.format(cred_filename))
        if os.path.isfile(cred_filename):
            os.system('rm ' + cred_filename)
    
def display_dict(dictionary, description=None):
    if description:
        print(description)
    
    for l1 in dictionary:
        print(l1, 'is of type', type(dictionary[l1]))
        if isinstance(dictionary[l1], str):
            print(l1 + ': ' + dictionary[l1])
        elif isinstance(dictionary[l1], dict):
            for l2 in dictionary[l1]:
                print('\t' + l2, 'is of type', type(dictionary[l1][l2]))
                if isinstance(dictionary[l1][l2], str):
                    print('\t' + l2 + ': ' + dictionary[l1][l2])
                elif isinstance(dictionary[l1][l2], list):
                    print('\t' + l2 + ':' )
                    for l3 in dictionary[l1][l2]:
                        print('\t\t' + str(l3))
"""

##### START NEW FROM HERE ####

def backslash_escape(string):

    special_characters = [' ',"^","$","&","|","?","*","+","(",")","\'"]

    # Remove any existing backslashes
    new_string = string.replace("\\", "")

    # Replace any special characters with escape slash
    for i in special_characters:
        new_string = new_string.replace(i,"\\"+i)
    return new_string


def read_configfile(config_file):
    print(config_file)
    parameters = dict(dotenv_values(config_file))
    return parameters

# Input API credentials file and output dictionary with CLIENT_ID CLIENT_SECRET and CLIENT_NAME
def get_creds(credentials_file=None):
    if credentials_file:
        api_creds = dotenv.dotenv_values(credentials_file)
    return dict(api_creds)

def refresh_token(api_creds, api_base, tmp_dir):
    api_endpoint = urljoin(api_base, '/oauth/token')

    auth_dir = os.path.join(tmp_dir, 'aura_api_auth')

    if not os.path.isdir(auth_dir):
        mkdir_cmd = 'mkdir ' + backslash_escape(auth_dir)
        print(mkdir_cmd)
        os.system(mkdir_cmd)

    #Check if tmp_dir exists
    token_file = os.path.join(auth_dir, 'bearer_token')
    if os.path.isdir(tmp_dir):
        if os.path.isfile(token_file):
            token_file_exists = True
    else:
        confirm_create = input('Create tmp directory {}? '.format(tmp_dir))
        if confirm_create.casefold() == 'y':
            mkdir_cmd = 'mkdir ' + tmp_dir
            os.system(mkdir_cmd) 
            
    curl_cmd = "curl --request POST '{}' --user '{}:{}' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'grant_type=client_credentials'".format(api_endpoint, api_creds['CLIENT_ID'], api_creds['CLIENT_SECRET'], api_creds['CLIENT_NAME'])
    result = json.loads(subprocess.check_output(curl_cmd, shell=True))
    access_token = result['access_token']
    expires_in = result['expires_in']

    now = datetime.datetime.now()
    expiration = (now + datetime.timedelta(0, expires_in)).isoformat()

    bearer_token = {
        'access_token': access_token,
        'expiration': expiration
    }

    with open(token_file, "w") as outfile:
        json.dump(bearer_token, outfile, indent=4)

    access_token = bearer_token['access_token']
    return access_token 

# Check if token is valid for at least 5 more minutes (later on can add a variable to adjust the time window)
def validate_token(bearer_token):
    token_valid = False
    token_expiration = datetime.datetime.fromisoformat(str(bearer_token['expiration']))
    delta_time = (token_expiration - datetime.datetime.now()).total_seconds()

    print('delta_time:', delta_time)

    # Make sure token has at least 5 more minutes of validity left
    if delta_time > 300:
        print('token_expiration:', token_expiration)
        print('Token is valid for {} more minutes'.format(delta_time/60)) 
        token_valid = True

    return token_valid

# Input API credentials ans return an access token for the API
def authenticate_api(api_creds, api_base, tmp_dir):

    api_endpoint = urljoin(api_base, '/oauth/token')
    token_file_exists = False 
    valid_token = False

    #Check if tmp_dir exists
    token_file = os.path.join(tmp_dir, 'bearer_token')
    if os.path.isdir(tmp_dir):
        if os.path.isfile(token_file):
            token_file_exists = True
    else:
        confirm_create = input('Create tmp directory {}? '.format(tmp_dir))
        if confirm_create.casefold() == 'y':
            mkdir_cmd = 'mkdir ' + backslash_escape(tmp_dir)
            os.system(mkdir_cmd)


    if token_file_exists:
        with open(token_file, "r") as infile:
            bearer_token = json.load(infile)

        valid_token = validate_token(bearer_token)

    # If there is no valid token, then generate a new one
    if valid_token:
        access_token = bearer_token['access_token']
    else:
        access_token = refresh_token(api_creds, api_base, tmp_dir)

    return access_token

def get_timestamp():
    current_localtime = time.localtime()
    timestamp = str(current_localtime[0]).zfill(4) + \
                     str(current_localtime[1]).zfill(2) + \
                     str(current_localtime[2]).zfill(2) + \
                     "T" + \
                    str(current_localtime[3]).zfill(2) + \
                    str(current_localtime[4]).zfill(2) + \
                    str(current_localtime[5]).zfill(2) 

    return timestamp


def deploy_instance(access_token, api_base, instance_params):
    api_endpoint = urljoin(api_base, '/v1/instances')

#    instance_name = instance_params['INSTANCE_NAMEBASE']
    instance_name = instance_params['INSTANCE_NAMEBASE'] + '_' + get_timestamp()
    print('instance_name:', instance_name)

    instance_details = {}

    # ENTER A STEP HERE TO VALIDATE CONFIG BEFORE DEPLOYING

    print()
    print('api_endpoint:', api_endpoint)
    print()
    request_body = {
        "version": instance_params['NEO4J_VERSION'],
        "region": instance_params['REGION'],
        "memory": str(instance_params['INSTANCE_SIZE']) + 'GB',
        "name": instance_name,
        "type": instance_params['INSTANCE_TYPE'],
        "tenant_id": instance_params['AURA_TENANT'],
        "cloud_provider": instance_params['CLOUD_PROVIDER'], 
    }

    print('request_body:')
    print(json.dumps(request_body, indent=4))

    print('request body type (before):', type(request_body))
    json_request_body = json.dumps(request_body)
    print('request body type (after):', type(json_request_body))

    curl_cmd = "curl -s -X 'POST' '{}' -H 'accept: application/json' -H 'Authorization: Bearer {}' -H 'Content-Type: application/json'".format(api_endpoint, access_token)
    curl_cmd += " -d '{}'".format(json_request_body)
    print('curl_cmd:')
    print(curl_cmd)
    api_response = json.loads(subprocess.check_output(curl_cmd, shell=True))

    print('New instance created:')
    print(api_response)
    
    response_data = api_response['data']
    
    instance_details['id'] = response_data['id']
    instance_details['name'] = response_data['name']
    instance_details['connection_url'] = response_data['connection_url']
    instance_details['password'] = response_data['password']
    instance_details['username'] = response_data['username']
    instance_details['cloud_provider'] = response_data['cloud_provider']
    instance_details['region'] = response_data['region']
    instance_details['tenant_id'] = response_data['tenant_id']
    instance_details['type'] = response_data['type']

    print()
    print('instance_details:')
    for item in instance_details:
        print(item, '=', instance_details[item])
    print()

    return instance_details

def export_credentials(instance_details):
    filename = 'Neo4j-' + instance_details['id'] + '-' + instance_details['name'] + '.txt' 
    credentials_file = ""
    credentials_file += 'NEO4J_URI=' + instance_details['connection_url'] + '\n'
    credentials_file += 'NEO4J_USERNAME=' + instance_details['username'] + '\n'
    credentials_file += 'NEO4J_PASSWORD=' + instance_details['password'] + '\n'
    credentials_file += 'NEO4J_INSTANCEID=' + instance_details['id'] + '\n'
    credentials_file += 'NEO4J_INSTANCENAME=' + instance_details['name'] + '\n'

#    credential_dir = os.path.join(tmp_dir, 'aura_credentials')
    if not os.path.isdir(credential_dir):
        mkdir_cmd = 'mkdir ' + backslash_escape(credential_dir)
        os.system(mkdir_cmd)

    cred_file = os.path.join(credential_dir, filename)

    print('\nWriting Aura instance credentials to file {}'.format(cred_file))
    with open(cred_file, 'w') as f:
        f.write(credentials_file)
    return cred_file

def export_envfile(environment_variables, export_dir=tmp_dir):
    print('deployment_file:', environment_variables)
    print('TYPE:', type(environment_variables))
    print(environment_variables)

#    export_dir = tmp_dir

#    if subdir:
#        export_dir = os.path.join(tmp_dir, subdir)

    print('export_dir:', export_dir)
    env_file = os.path.join(export_dir, environment_variables['DEPLOYMENT_NAME'] + '.txt')

    if not os.path.isdir(export_dir):
        mkdir_cmd = 'mkdir ' + backslash_escape(export_dir)
        print(mkdir_cmd)
        os.system(mkdir_cmd)

    print('\nWriting demo deployment details to file {}'.format(env_file))
    with open(env_file, 'w') as f:
        f.write(json.dumps(environment_variables, indent=4))
    return env_file

def deploy_demo(deployment_parameters):
    print('[in function] deployment_parameters:')
    print(deployment_parameters)
    cred_file = deployment_parameters['API_CREDENTIALS']
    print('cred_file:', cred_file)
    credentials = get_creds(cred_file)
    print('credentials:', credentials)
    bearer_token = authenticate_api(credentials, api_base, tmp_dir)
    print('bearer_token:', bearer_token)

    # Deploy the configure instance(s)
    instance_details = deploy_instance(bearer_token, api_base, deployment_parameters)
    demo_name = deployment_parameters['DEMO_NAME'] 
    deployment_name = str(demo_name) + '_' + str(get_timestamp()) 
    print()
    print('instance_details:')
    print(instance_details)

    instance_credentials = export_credentials(instance_details)

    deployment_details = {
        'DEMO_NAME' : demo_name,
        'DEPLOYMENT_NAME' : deployment_name,
        'NEO4J_INSTANCENAME' : instance_details['name'],
        'NEO4J_URI' : instance_details['connection_url'],
        'NEO4J_USERNAME' : instance_details['username'],
        'NEO4J_PASSWORD' : instance_details['password'],
        'NEO4J_CREDENTIALS': instance_credentials,
    }
 
    deployment_file = export_envfile(deployment_details, export_dir=deployment_dir)
    print('DEPLOYMENT_FILE:', deployment_file)

def list_deployments(deployment_dir):
    deployments = {} 
    for dirname, subdir, filelist in os.walk(deployment_dir):
        for file in filelist:
            file_abspath = os.path.join(dirname, file)
            print('file_abspath:', file_abspath)
            f = open(file_abspath)
            deployment_dict = json.load(f)
            deployments[deployment_dict['DEPLOYMENT_NAME']] = deployment_dict

    return deployments

def parseargs(defaults=None, config_files=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--deploy-demo', metavar="DEMO_CONFIG", help="Aura API credentials file")
    parser.add_argument('--deploy-instance', action='store_true', help="Deploy new Aura instance")
    parser.add_argument('--list', action='store_true', help="Deploy new Aura instance")
    parser.add_argument('--authenticate', metavar="CREDENTIALS_FILE", help="Aura API credentials file")
    parser.add_argument('--refresh-token', action='store_true', help="Refresh bearer token")
    args = parser.parse_args()	
    return vars(args)

def main():
    args = parseargs()

    # Read in parameters from demo config ENV file. 
    # NOTE: Later on can do this with JSON as well
    if args['deploy_demo']:
        deployment_parameters = read_configfile(args['deploy_demo'])
        deploy_demo(deployment_parameters)

    if args['authenticate']:
        cred_file = args['authenticate']
        credentials = get_creds(cred_file)
        bearer_token = authenticate_api(credentials, api_base, tmp_dir)

    if args['list']:
        deployments = list_deployments(deployment_dir)
        print('\nDeployments:')
        print(json.dumps(deployments, indent=4))
        print()

if __name__ == '__main__':
    main()
