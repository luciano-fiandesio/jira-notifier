"""

Notify a developer via Slack if he/she has a Jira issue with a merged Pull Request
and the Jira issue's status is not equal to 'Done'

"""

import time
import json
from jira import JIRA

SERVER = "https://jira.dhis2.org"
PROJECT = "DHIS2"
jira_options = {"server": SERVER}
jira = JIRA(options=jira_options, basic_auth=(
    "username", "password"))
sess_get = jira._session.get


def get_dev_status(issue_id):
    """ get the pull request data for the issue id """
    dev_status = SERVER + "/rest/dev-status/1.0"
    _issue = 'issue/summary?issueId=%s' % issue_id
    _args = '_=%s' % int(time.time())
    req_url = '%s/%s&amp;%s' % (dev_status, _issue, _args)
    response = sess_get(req_url)
    raw_data = json.loads(response.content)
    return raw_data

def notify():
    """ TODO! """
    print("notify!")

if __name__ == "__main__":

    # get issues for project
    issues_in_proj = jira.search_issues('project=' + PROJECT)

    for issue in issues_in_proj:
        # print('{}: {}  (status: {})'.format(issue.key, issue.fields.summary, issue.fields.status))
        status = issue.fields.status
        pr_status_raw = get_dev_status(issue.id)
        pr_status = pr_status_raw['summary']['pullrequest']['overall']['state']
        if status:
            # print('! {}'.format(status))
            if str(status) == 'In Progress' and pr_status == 'MERGED':
                print('> {} - status: {} - {} - pr: {}'.format(issue.key,
                                                               status, issue.fields.assignee, pr_status))
                notify()
