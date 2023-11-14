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
#issues_data = pd.read_excel('create_tickets.xlsx')
jql = 'project=ILFI'

issues = impactica_jira.search_issues(jql_str=jql, maxResults=False, expand='changelog')


for issue in issues:
    epic = get_epic(issue)
    key = issue.key
    issue_type = issue.fields.issuetype.name
    labels_list = issue.fields.labels


    # Insert edition logic
    if epic in ["BackEnd","DevOps"] and issue_type in ['Task','Sub-task'] and 'NO-QA' not in labels_list:
        labels_list.append('NO-QA')
        issue.update(fields={'labels': labels_list})
        print(f"{key} issues NO-QA tag has been added.")


# Close Jira client instance
impactica_jira.close()