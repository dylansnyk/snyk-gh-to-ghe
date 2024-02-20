# Snyk GH -> GHE migration

For each script, add your `SNYK_TOKEN` and any other required variable at the top of the python file.

## Enable Snyk Code across all orgs

1. Update the `SNYK_TOKEN`.
2. Run `python enable-snyk-code.py`

## Add the GHE integration across all repos

1. Choose one Snyk Org to set up the GHE integration in the Snyk UI. Adjust the integration settings as needed.
2. Update the `SNYK_TOKEN` and the `SOURCE_ORG`, which is the org that has the integration configured.
3. Run `python copy-ghe-integration.py`

Note: this script can also be used to sync the settings across your Snyk orgs (for GHE)

## Import all existing GitHub projects via the "GitHub Enterprise" integration

1. Update the `SNYK_TOKEN`.
2. Run `python reimport-repos.py --dry-run` to review all organizations and repos to be imported. The script will require user input for each org.
3. Run `python reimport-repos.py` to execute the same process, but actually trigger the import for each repo.

## Delete old GitHub projects

1. Update `SNYK_TOKEN`
2. Run `python delete-gh-projects.py --dry-run` to review all repos that will be deleted.
3. Run `python delete-gh-projects.py` to execute the same process, but actually delete each repo.
