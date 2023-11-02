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

def get_org_ghe_id(org_id):
    url = f'https://api.snyk.io/v1/org/{org_id}/integrations'

    payload = {}
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['github-enterprise']


def get_projects_page(base_url, next_url):

    # Add "next url" on to the BASE URL
    url = base_url + next_url

    headers = {
        'Accept': 'application/vnd.api+json',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    return requests.request("GET", url, headers=headers)


def get_all_repos(org_id):
    base_url = "https://api.snyk.io/rest"

    next_url = f"/orgs/{org_id}/projects?version=2023-06-23&limit=100&origins=github"

    all_projects = []

    while next_url is not None:
        res = get_projects_page(base_url, next_url).json()

        if 'next' in res['links']:
            next_url = res['links']['next']
        else:
            next_url = None

        # add to list
        all_projects.extend(res['data'])

    repo_dict = {}

    for project in all_projects:
        repo = project['attributes']['name'].split(':')[0]
        # print(project['attributes']['name'])
        owner = repo.split('/')[0]

        name = repo.split('/')[1]
        if name.find('(') != -1:
            name = name[:name.find('(')]

        branch = project['attributes']['target_reference']
        repo_dict[repo] = {
            'owner': owner,
            'name': name,
            'branch': branch
        }
    
    return list(repo_dict.values())

def import_repo(org_id, integration_id, repo):
    url = f'https://api.snyk.io/v1/org/{org_id}/integrations/{integration_id}/import'

    payload = {
        'target': repo
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'token {SNYK_TOKEN}'
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return response

orgs = get_orgs()['data']

for org in orgs:
    org_id = org['id']

    val = input(f"{org['attributes']['name']} (n to quit): ")
    if val == 'n':
        exit()

    print(org_id, org['attributes']['name'])
    ghe_id = get_org_ghe_id(org_id)

    repos = get_all_repos(org_id)
    for repo in repos:
        print(' >', repo)
        res = import_repo(org_id, ghe_id, repo)
        print(res.status_code)