import redminelib 
import logging
import sys

from datetime import datetime, timedelta, timezone
import configparser
import argparse

# closes all issues in project "ticketsystem" (999_Ticketsystem) that are
# - older then 14 days 
# - on status 3 (gelöst) or on status 8 (warte auf Rückmeldung)

# Needs url and token of redmine in a redmineIssueCloser.conf file or other file via --config argument
# 

parser = argparse.ArgumentParser(description='Description of your script.')
parser.add_argument('--config', help='Other redmineIssueCloser.conf name (optional)')
args = parser.parse_args()

configfile = args.config
if configfile is None:
    configfile = "redmineIssueCloser.conf"

config = configparser.ConfigParser()
config.read(configfile)

# Access values from the 'Settings' section
redmine_url = config.get('Settings', 'redmine_url')
redmine_token = config.get('Settings', 'redmine_token')
debug = config.getboolean('Settings', 'debug', fallback=False)

if redmine_url is None:
    print(f"redmine_url not set")
    sys.exit()
if redmine_token is None:
    print(f"redmine_token not set")
    sys.exit()

current_time = datetime.utcnow()
seven_days_ago = current_time - timedelta(days=14)
timestamp_string = seven_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
filter_expression = "<=" + timestamp_string
redmine = redminelib.Redmine(redmine_url, key=redmine_token)
issues_to_close = redmine.issue.filter(project_id='ticketsystem',status_id=3, updated_on=filter_expression)
for issue in issues_to_close:
    print(issue.id)
    if not debug:
        redmine.issue.update(issue.id,status_id=5)

print("------")
issues_to_close = redmine.issue.filter(project_id='ticketsystem',status_id=8, updated_on=filter_expression)
for issue in issues_to_close:
    print(issue.id)
    if not debug:
        redmine.issue.update(issue.id,status_id=5)
