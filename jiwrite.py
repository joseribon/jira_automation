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
issues_data = pd.read_excel('SP xlsx - Sprint 1.xlsx')


for n in range(len(issues_data.index)):
    # Getting the data
    key = issues_data.iloc[n]['Issue Key']
    sps = int(issues_data.iloc[n]['Consensus'])

    # Fetching issue of interest
    issue = impactica_jira.issue(key)


    # Writing the data
    issue.update(fields={'customfield_10026': sps})

    print(f"Issue {key}'s SPs field successfully updated")




# Close Jira client instance
impactica_jira.close()