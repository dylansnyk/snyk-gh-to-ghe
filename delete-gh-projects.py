import requests
import sys

SNYK_TOKEN = ''

dry_run = False
if '--dry-run' in set(sys.argv):
    dry_run = True

def get_orgs():
    url = "https://api.snyk.io/rest/orgs?version=2023-06-23~beta&limit=100"

    payload = {}
    headers = {
        'Accept': 'application/vnd.api+json',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_targets_page(base_url, next_url):

    # Add "next url" on to the BASE URL
    url = base_url + next_url

    headers = {
        'Accept': 'application/vnd.api+json',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    return requests.request("GET", url, headers=headers)


def get_all_targets(org_id):
    base_url = "https://api.snyk.io/rest"

    next_url = f"/orgs/{org_id}/targets?version=2023-06-23~beta&limit=100&origin=github"

    all_targets = []

    while next_url is not None:
        res = get_targets_page(base_url, next_url).json()

        if 'next' in res['links']:
            next_url = res['links']['next']
        else:
            next_url = None

        # add to list
        all_targets.extend(res['data'])

    return all_targets


def delete_target(org_id, target_id):
    url = f"https://api.snyk.io/rest/orgs/{org_id}/targets/{target_id}?version=2023-06-23~beta"

    headers = {
        'Accept': 'application/vnd.api+json',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    return requests.request("DELETE", url, headers=headers)



orgs = get_orgs()['data']

for org in orgs:
    org_id = org['id']

    val = input(f"{org['attributes']['name']} (q to quit, s to skip): ")
    if val == 'q':
        exit()
    if val == 's':
        continue

    repos = get_all_targets(org_id)
    for repo in repos:
        print(' >', repo['id'], repo['attributes']['displayName'])
        if not dry_run:
            res = delete_target(org_id, repo['id'])
            print('  ', res.status_code)
