from pandas import DataFrame
from jira import JIRA
from datetime import datetime
from keys import alicia, jira_user
from utils import *


# Get User extraction preferences (historical/sprint)
scope_options = ('historical','sprint')

preferences_complete = False
while preferences_complete == False:
    scope = input('Type the scope of the extraction (historical/sprint): ')

    if scope in scope_options:
        preferences_complete = True
    else:
        print('Input invalid. Please use the options within parenthesis.')

    

# Jira Cloud connection details

user = jira_user
keys = alicia
server = 'https://impactica.atlassian.net/'
options = {'server': server}

# Initialise Jira client instance
impactica_jira = JIRA(options, basic_auth=(user,keys))


# Assemble JQL queries
jql = 'project=ILFI'
if scope == 'sprint':
    jql += ' AND sprint in openSprints()'
elif scope == 'historical':
    jql += ' AND sprint is not EMPTY'

# Quesry for issues of interest
#issues = impactica_jira.search_issues(jql_str=jql, maxResults=False, fields=fields)
issues = impactica_jira.search_issues(jql_str=jql, maxResults=False, expand='changelog')

# Create and populate DataFrame
issues_data = []
for issue in issues:
    issues_data.append({
        'key': issue.key,
        'type': issue.fields.issuetype.name,
        'summary': issue.fields.summary,
        'epic': get_epic(issue),
        'sprint': get_sprint(issue),
        'status': issue.fields.status.name,
        'story points': issue.fields.customfield_10026,
        'priority': issue.fields.priority.name,
        'assignee': None if pd.isnull(issue.fields.assignee) else issue.fields.assignee.displayName,
        'reporter': issue.fields.reporter.displayName,
        'labels': ','.join(issue.fields.labels),
        'resolution': 'Not resolved' if pd.isnull(issue.fields.resolution) else issue.fields.resolution.name,
        'creation date': to_datetime(issue.fields.created),
        'addition date': get_addition_date(issue),
        'resolution date': to_datetime(issue.fields.resolutiondate),
        'Hours In Progress': get_status_hours(issue,'In Progress'),
        'Hours In Review': get_status_hours(issue,'In Review'),
        'Hours In QA': get_status_hours(issue,'QA'),
        })
df = DataFrame.from_records(issues_data)
df.to_excel('Sprint 4 - START.xlsx', index=False)
print(f'Jira {scope} data successfully extracted.')


# Close Jira client instance
impactica_jira.close()