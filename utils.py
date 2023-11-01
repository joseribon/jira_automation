import pandas as pd
from jira import JIRA
from datetime import datetime, date, time, timedelta
import holidays
import pytz


# Define extraction fields
fields = [
    'issuetype',
    'summary',
    'customfield_10020',
    'status',
    'customfield_10026',
    'priority',
    'assignee',
    'reporter',
    'labels',
    'resolution',
    'resolutiondate',
    'created',
    'changelog',
]

# Function to extract deployment date



# Function to process Acceptance Criteria text
def process_criteria(criteria_str: str) -> str:
    if type(criteria_str) == str:
        items = criteria_str.split(';')
        formatted_items = '\n'.join([f"* {item.strip()}" for item in items if item.strip()])
        description_text = "*+Acceptance Criteria+*\n" + formatted_items

        return description_text
    else:
        return None


# Convert Jira string dates into datetime objects
def to_datetime(jira_datetime: str) -> datetime:
    if jira_datetime:
        dt = datetime.strptime(jira_datetime, '%Y-%m-%dT%H:%M:%S.%f%z')
        et_timezone = pytz.timezone('US/Eastern')
        dt = dt.astimezone(et_timezone)
        dt = dt.replace(tzinfo=None)
        return dt
    else:
        return None

# Function to extract time spent on a specific given status
def get_status_hours(issue: JIRA, status: str) -> float:
    start = None
    end = None
    total_hours = 0

    worklogs = issue.changelog

    for worklog in reversed(worklogs.histories):
        for change in worklog.items:
            if change.field == "status" and change.toString == status and not start:
                start = to_datetime(worklog.created)
            elif change.field == "status" and change.toString != status and change.fromString == status and start:
                end = to_datetime(worklog.created)
                total_hours += business_hours(start, end)
                start = None
                end = None

    if issue.fields.status.name == status and start:
        end = datetime.now()
        total_hours += business_hours(start, end)

    return round(total_hours,1)

# Function to get the latest sprint addition date
def get_addition_date(issue: JIRA) -> date:
    worklogs = issue.changelog

    addition_date = None

    for worklog in worklogs.histories:
        for change in worklog.items:
            if change.field == "Sprint":
                addition_date = to_datetime(worklog.created).date()

    return addition_date

# Check if it is Loka Friday off


# Function to get business hours between two time stamps
def business_hours(start: datetime, end: datetime, country='US', schedule_start=9, schedule_end=17) -> float:
    holiday_list = holidays.CountryHoliday(country, years=[start.year, end.year])
    current_date = start.date()
    end_date = end.date()
    total_hours = 0.0

    while current_date <= end_date:
        if current_date.weekday() < 5 and current_date not in holiday_list:
            work_start = datetime.combine(current_date, time(schedule_start, 0))
            work_end = datetime.combine(current_date, time(schedule_end, 0))

            if current_date == start.date():
                work_start = max(work_start, start)
            if current_date == end.date():
                work_end = min(work_end, end)

            time_difference = work_end - work_start
            hours = time_difference.seconds / 3600.0
            
            total_hours += hours

        current_date += timedelta(days=1)

    return total_hours

# Function to get Epic
def get_epic(issue: JIRA) -> str:
    epics = {
        "ILFI-6": "DevOps",
        "ILFI-7": "BackEnd",
        "ILFI-8": "FrontEnd",
    }
    epic = issue.fields.customfield_10014
    if epic in epics.keys():
        epic = epics[epic]
        return epic
    else:
        return None


# Function to get Sprint
def get_sprint(issue: JIRA) -> str:
    sprint = issue.fields.customfield_10020
    if type(sprint) == list:
        if len(sprint) > 1:
            sprint = sprint[-1].name
        elif len(sprint) == 1:
            sprint = sprint[0].name
        else:
            sprint = ""
    elif sprint == None:
        sprint = ""
    
    return sprint

# DF function to convert list to dictionary for epics processing

