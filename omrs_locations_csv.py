#!/usr/bin/env python

#from azure_sso import authenticate_via_azure
import argparse
import yaml
import requests
import json
import csv

# Default configuration
DEFAULT_CONFIG_FILE = 'omrs.yml'
DEFAULT_USER = 'admin'
DEFAULT_PASSWORD = 'Admin123'

#azure_session = authenticate_via_azure()

# Command line parsing
parser = argparse.ArgumentParser(description='OpenMRS REST API Client for Location Operations')
subparsers = parser.add_subparsers()

parser.add_argument('--config', '-c', metavar='PATH', default=DEFAULT_CONFIG_FILE, help='Path to configuration file')
parser.add_argument('--base_url', '-b', metavar='URL', help='URL of OpenMRS API up through version number without ending slash')
parser.add_argument('--user', '-u', metavar='USERNAME', default=DEFAULT_USER, help='Username for authentication to API')
parser.add_argument('--pw', '-p', metavar='PASSWORD', default=DEFAULT_PASSWORD, help='Password for authentication to API')
parser.add_argument('--quiet', '-q', action='store_true')
parser.add_argument('--csv', '-csv', metavar='CSV_PATH', help='Path to CSV file with location data')

parser_locations = subparsers.add_parser('locations', description='List locations')
parser_locations.set_defaults(func='locations')

parser_addlocation = subparsers.add_parser('addlocation', description='Add a new location')
parser_addlocation.add_argument('--name', '-n', required=True, help='Name of the new location')
parser_addlocation.add_argument('--description', '-d', help='Description for the new location')
parser_addlocation.add_argument('--tags', '-t', help='Comma-separated tags associated with the new location')
parser_addlocation.add_argument('--country', '-co', help='Country of the new location')
parser_addlocation.add_argument('--parentLocation', '-pl', help='Parent location name')
parser_addlocation.set_defaults(func='addlocation')

parser_updatelocation = subparsers.add_parser('updatelocation', description='Update an existing location')
parser_updatelocation.add_argument('--uuid', '-u', required=True, help='UUID of the location to be updated')
parser_updatelocation.add_argument('--name', '-n', help='New name of the location')
parser_updatelocation.add_argument('--description', '-d', help='New description for the location')
parser_updatelocation.add_argument('--tags', '-t', help='New tags for the location, comma-separated')
parser_updatelocation.add_argument('--country', '-c', help='New country for the location')
parser_updatelocation.add_argument('--parentLocation', '-pl', help='Name of the new parent location')
parser_updatelocation.set_defaults(func='updatelocation')

args = parser.parse_args()

config = yaml.safe_load(open(args.config))
base_url = config.get('base_url')
api = f'{base_url}/ws/rest/v1'
user = config['user']
pw = config['pw']

def openmrs_get(url):
    '''Request a list of results from API and return them'''
    resp = requests.get(url, auth=(user, pw))
    resp.raise_for_status()
    return resp.json().get('results', [])

    '''Request a list of results from API and return them'''
   # resp = azure_session.get(url)  # Use the authenticated session here
   # resp.raise_for_status()
   # return resp.json().get('results', [])

def openmrs_post(url, data_json):
    '''Create a new resource and return its uuid'''
    headers = {'Content-type': 'application/json'}
    resp = requests.post(url, data_json, headers=headers, auth=(user, pw))
    resp.raise_for_status()
    return resp.json()['uuid']

    '''Create a new resource and return its uuid'''
    #headers = {'Content-type': 'application/json'}
    #resp = azure_session.post(url, data_json, headers=headers)  # Use the authenticated session here
    #resp.raise_for_status()
    #return resp.json()['uuid']

def get_location_uuid_by_name(name):
    '''Retrieve location UUID by its name'''
    url = f'{api}/location?q={name}'
    results = openmrs_get(url)
    if results:
        return results[0]['uuid']
    return None

def get_tag_uuid(tag_name):
    '''Retrieve the UUID of a tag by its name'''
    url = f'{api}/locationtag?q={tag_name}'
    results = openmrs_get(url)
    if results:
        return results[0]['uuid']
    return None

def does_location_exist_by_uuid(uuid):
    '''Check if a location exists in OpenMRS by its UUID'''
    url = f'{api}/location/{uuid}'
    resp = requests.get(url, auth=(user, pw))
    return resp.status_code == 200

def create_location(uuid=None, name=None, description=None, tags=None, country=None, parentLocationName=None):
    '''Create a location in OpenMRS'''
    url = f'{api}/location'
    data = {'name': name}
    if uuid:
        data['uuid'] = uuid
    if description:
        data['description'] = description
    if tags:
        tag_uuids = [get_tag_uuid(tag.strip()) for tag in tags.split(',')]
        data['tags'] = tag_uuids
    if country:
        data['country'] = country
    if parentLocationName:
        parentLocationUuid = get_location_uuid_by_name(parentLocationName)
        if parentLocationUuid:
            data['parentLocation'] = {'uuid': parentLocationUuid}
    return openmrs_post(url, json.dumps(data))

def update_location(uuid, name=None, description=None, tags=None, country=None, parentLocationName=None):
    '''Update a location in OpenMRS'''
    url = f'{api}/location/{uuid}'
    data = {}
    if name:
        data['name'] = name
    if description:
        data['description'] = description
    if tags:
        tag_uuids = [get_tag_uuid(tag.strip()) for tag in tags.split(',')]
        data['tags'] = tag_uuids
    if country:
        data['country'] = country
    if parentLocationName:
        parentLocationUuid = get_location_uuid_by_name(parentLocationName)
        if parentLocationUuid:
            data['parentLocation'] = {'uuid': parentLocationUuid}
    return openmrs_post(url, json.dumps(data))

def parse_csv(csv_path):
    locations = []
    with open(csv_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')  # <-- Specify the delimiter here
        for row in reader:
            print(f"Read row: {row}")  # Debug statement
            locations.append(row)
    return locations


# At the beginning of the main function
def main():
    '''Main function to handle CLI commands'''
    
    print(f"Parsed Arguments: {args}")

    silence = args.quiet
    
    if args.csv:
        print("Processing CSV file...")
        locations_from_csv = parse_csv(args.csv)
        
        if not locations_from_csv:
            print("No locations found in the provided CSV.")
            return

        for loc in locations_from_csv:
            uuid = loc.get('UUID', None)
            if uuid and does_location_exist_by_uuid(uuid):
                # Update the location if UUID exists in OpenMRS
                print(f"Updating location with UUID {uuid}...")  # Debug statement
                update_location(
                    uuid=uuid,
                    name=loc['name'],
                    description=loc.get('Description', None),
                    tags=loc.get('Tags', None),
                    country=loc.get('Country', None),
                    parentLocationName=loc.get('ParentLocation', None)
                )
                if not silence:
                    print(f"Updated location with UUID {uuid}!")
            elif uuid: 
                # Create a new location using the UUID from the CSV if it doesn't exist in OpenMRS
                print(f"Creating a new location with UUID {uuid}...")  # Debug statement
                create_location(
                    uuid=uuid,
                    name=loc['name'],
                    description=loc.get('Description', None),
                    tags=loc.get('Tags', None),
                    country=loc.get('Country', None),
                    parentLocationName=loc.get('ParentLocation', None)
                )
                if not silence:
                    print(f"Created a new location with UUID {uuid}!")
    else:
        print("No CSV file provided. Exiting.")

if __name__ == '__main__':
    main()
