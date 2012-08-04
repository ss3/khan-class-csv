import csv
import json
import sys
import urllib

import oauth_login
import test_oauth_client

CONSUMER_KEY = "key"
CONSUMER_SECRET = "secret"
SERVER_URL = "http://www.khanacademy.org"

OAUTH_CLIENT = test_oauth_client.TestOAuthClient(
    SERVER_URL, CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = oauth_login.get_access_token(OAUTH_CLIENT)


def khan_get(resource_url):
    return OAUTH_CLIENT.access_resource(resource_url, ACCESS_TOKEN)


def khan_get_json(resource_url):
    return json.loads(khan_get(resource_url))


def khan_allstudents(coach_email=None):
    if coach_email:
        suffix = '&coach_email=%s' % urllib.quote(coach_email)
    else:
        suffix = ''
    return khan_get_json(
        '/api/v1/user/students/progressreport?list_id=allstudents' + suffix)


def khan_user(email=None):
    if email:
        suffix = '?email=%s' % urllib.quote(email)
    else:
        suffix = ''
    return khan_get_json('/api/v1/user' + suffix)

out = csv.writer(sys.stdout)
out.writerow([
    'Student',
    'Energy Points',
    'Number of Proficient Exercises',
    'Meteorite Badges',
    'Moon Badges',
    'Earth Badges',
    'Sun Badges',
    'Black Hole Badges',
    'Challenge Patches',
])

allstudents = khan_allstudents()
for student in sorted(allstudents['exercise_data'],
                      key=lambda s: s['nickname']):
    user = khan_user(student['email'])
    out.writerow([
        user['nickname'],
        user['points'],
        len(user['all_proficient_exercises']),
        user['badge_counts']['0'],  # Meteorite
        user['badge_counts']['1'],  # Moon
        user['badge_counts']['2'],  # Earth
        user['badge_counts']['3'],  # Sun
        user['badge_counts']['4'],  # Black Hole
        user['badge_counts']['5'],  # Challenge Patches
    ])
