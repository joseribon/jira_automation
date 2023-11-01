import pandas as pd
from jira import JIRA
from datetime import datetime
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
jql = 'project=ILFI'

issues = impactica_jira.search_issues(jql_str=jql, maxResults=False, expand='changelog')

for n in range(len(issues_data.index)):
    for issue in issues:
        summary = issue.fields.summary
        key = issue.key
        if issues_data.iloc[n]['Summary'] == summary:
            description = issues_data.iloc[n]['Description']
            description = None if pd.isna(description) else description
            acceptance = issues_data.iloc[n]['Acceptance Criteria']
            acceptance = process_criteria(acceptance)
            if not pd.isna(acceptance):
                description += f'\n\n{acceptance}'
            
            issue.update(fields={'description': description})
            print(f"{key} issues' acceptance criteria has been added.")


# Close Jira client instance
impactica_jira.close()