import pandas as pd
from jira import JIRA
from keys import alicia, jira_user
from utils import *


# Jira Cloud connection details
user = jira_user
keys = alicia
server = 'https://impactica.atlassian.net/'
options = {'server': server}

# Initialise Jira client instance
impactica_jira = JIRA(options, basic_auth=(user,keys))

# Read input data from Excel
issues_data = pd.read_excel('create_tickets.xlsx')

# Project details
project_key = "ILFI"
issue_type = "Task"
epics = {
    "DevOps": "ILFI-6",
    "BackEnd": "ILFI-7",
    "FrontEnd": "ILFI-8",
}
reporters = {
    "DevOps": "60ad2da0317edd0071944ec1",
    "BackEnd": "5dd2d6ae354f4f0e51fd53ad",
    "FrontEnd": "712020:1d09bb11-0f31-4063-8ef2-1c2a64bd83f2",
}


for n in range(len(issues_data.index)):
    
    sps = issues_data.iloc[n]['SP']
    sps = None if pd.isna(sps) else int(sps)
    epic = epics[issues_data.iloc[n]['Epic']]
    summary = issues_data.iloc[n]['Summary']
    description = issues_data.iloc[n]['Description']
    description = None if pd.isna(description) else description
    reporter = reporters[issues_data.iloc[n]['Epic']]
    acceptance = issues_data.iloc[n]['Acceptance Criteria']
    acceptance = process_criteria(acceptance)
    if not pd.isna(acceptance):
        description += f'\n\n{acceptance}'


    # Creating issue
    new_issue = impactica_jira.create_issue(
        project = project_key,
        summary = summary,
        description = description,
        customfield_10026 = sps,
        issuetype = {'name': issue_type},
        reporter = {'id': reporter},
        customfield_10014 = epic,
        labels = ['NO-QA'] if epic != "ILFI-8" else []
    )

    print(f"Issue {new_issue.key} has been successfully created")



# Close Jira client instance
impactica_jira.close()