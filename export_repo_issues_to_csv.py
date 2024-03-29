"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests
import configparser

config = configparser.ConfigParser()
config.read('./pass.ini')
GITHUB_USER = config['credentials']['GITHUB_USER']
GITHUB_PASSWORD = config['credentials']['GITHUB_PASSWORD']
REPO = config['repo']['REPO']  # format is username/repo

ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?state=all' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    for issue in r.json():
        csvout.writerow([issue['number'], issue['url'], issue['state'], issue['title'], issue['body'], issue['created_at'], issue['updated_at'], issue['closed_at']])


r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
f = open(csvfile, 'w', encoding='utf-8')
csvout = csv.writer(f)
csvout.writerow(('id', 'url', 'state', 'Title', 'Body', 'Created At', 'Updated At', 'Closed At'))
write_issues(r)
page = 0
#more pages? examine the 'link' header returned
while (1):
    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
                    
        print('page %i\nlink'%page,pages['next'])
        page = page +1
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)
        if pages['next'] == pages['last']:
            break
            
f.close()
