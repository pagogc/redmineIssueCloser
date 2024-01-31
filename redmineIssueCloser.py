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
request_status_ids = config.get('Settings', 'request_status_ids')
myproject_id= config.get('Settings', 'project_id')
close_status_id = None
older_than_days = None

try:
    close_status_id = int(config.get('Settings', 'close_status_id'))
except ValueError:
    print("Invalid close_status_id");
    sys.exit()

try:
    older_than_days = int(config.get('Settings', 'older_than_days'))
except ValueError:
    print("Invalid older_than_days");
    sys.exit()

if redmine_url is None:
    print(f"redmine_url not set")
    sys.exit()
if redmine_token is None:
    print(f"redmine_token not set")
    sys.exit()
if myproject_id is None:
    print(f"project_id not set")
    sys.exit()
if request_status_ids is None:
    print(f"request_status_ids not set")
    sys.exit()
if close_status_id is None:
    print(f"close_status_id not set")
    sys.exit()
if older_than_days is None:
    print(f"older_than_days not set")
    sys.exit()

request_id_list = request_status_ids.split(',')
current_time = datetime.utcnow()
seven_days_ago = current_time - timedelta(days=older_than_days)
timestamp_string = seven_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
filter_expression = "<=" + timestamp_string
redmine = redminelib.Redmine(redmine_url, key=redmine_token)
for statusid in request_id_list:
    issues_to_close = redmine.issue.filter(project_id=myproject_id,status_id=statusid, updated_on=filter_expression)
    for issue in issues_to_close:
        print(issue.id)
        if not debug:
            redmine.issue.update(issue.id,status_id=close_status_id)

