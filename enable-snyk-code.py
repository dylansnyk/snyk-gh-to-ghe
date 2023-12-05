import requests

SNYK_TOKEN = ''

def get_orgs():
    url = "https://api.snyk.io/rest/orgs?version=2023-10-24~beta&limit=100"

    payload = {}
    headers = {
        'Accept': 'application/vnd.api+json',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def enable_snyk_code(org_id):

    url = f'https://api.snyk.io/rest/orgs/{org_id}/settings/code?version=2023-10-24~experimental'

    payload = {
        "data": {
            "type": "code_settings",
            "id": org_id,
            "attributes": {
            "sast_enabled": True
            }
        }
    }
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f'token {SNYK_TOKEN}'
    }

    return requests.request("PATCH", url, headers=headers, json=payload)


orgs = get_orgs()['data']

for org in orgs:
    print(org['id'], org['attributes']['name'])
    res = enable_snyk_code(org['id'])
    print(' >', res.status_code, '\n')

