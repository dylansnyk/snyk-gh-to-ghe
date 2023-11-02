import requests

SNYK_TOKEN = ''
SOURCE_ORG = ''

def get_orgs():
    url = "https://api.snyk.io/rest/orgs?version=2023-10-24~beta&limit=100"

    payload = {}
    headers = {
        'Accept': 'application/vnd.api+json',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_source_org_ghe_id():
    url = f'https://api.snyk.io/v1/org/{SOURCE_ORG}/integrations'

    payload = {}
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['github-enterprise']


def clone_integartion(target_org_id, ghe_id):
    url = f'https://api.snyk.io/v1/org/{SOURCE_ORG}/integrations/{ghe_id}/clone'

    payload = {
        'destinationOrgPublicId': target_org_id
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return response


orgs = get_orgs()['data']
ghe_id = get_source_org_ghe_id()

for org in orgs:
    org_id = org['id']
    org_name = org['attributes']['name']
    
    if org_id != SOURCE_ORG:
        print(org_id, org_name)

        res = clone_integartion(org_id, ghe_id)
        print(' >', res.status_code, res.json(), '\n')

