"""

Notify a developer via Slack if he/she has a Jira issue with a merged Pull Request
and the Jira issue's status is not equal to 'Done'

Args:
    -s Jira server URL
    -u Jira server username
    -p Jira server password

Example:

    $ python jira_notify.py -s https://my.jira.com -u username -p password

"""

import time
import json
import argparse
from jira import JIRA

SERVER = "https://jira.dhis2.org"
PROJECT = "DHIS2"
jira_options = {"server": SERVER}

def init_jira(args):
    """ initialize connection to Jira server """
    return JIRA(options=jira_options, basic_auth=(args.username, args.password))

def get_dev_status(jira, issue_id):
    """ get the pull request data for the issue id """

    dev_status = SERVER + "/rest/dev-status/1.0"
    _issue = 'issue/summary?issueId=%s' % issue_id
    _args = '_=%s' % int(time.time())
    req_url = '%s/%s&amp;%s' % (dev_status, _issue, _args)
    response = jira._session.get(req_url)
    raw_data = json.loads(response.content)
    return raw_data

def notify():
    """ TODO! """
    print("notify!")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Notify Jira users of issues with incorrect status')
    parser.add_argument('-s', '--server', help='Jira server URL', default=SERVER)
    parser.add_argument('-u', '--username', help='Username', required=True)
    parser.add_argument('-p', '--password', help='Password', required=True)

    jira_api = init_jira(parser.parse_args())

    # get issues for project
    issues_in_proj = jira_api.search_issues('project=' + PROJECT)

    for issue in issues_in_proj:
        # print('{}: {}  (status: {})'.format(issue.key, issue.fields.summary, issue.fields.status))
        status = issue.fields.status
        pr_status_raw = get_dev_status(jira_api, issue.id)
        pr_status = pr_status_raw['summary']['pullrequest']['overall']['state']
        if status:
            # print('! {}'.format(status))
            if str(status) == 'In Progress' and pr_status == 'MERGED':
                print('> {} - status: {} - {} - pr: {}'\
                    .format(issue.key, status, issue.fields.assignee, pr_status))
                notify()
