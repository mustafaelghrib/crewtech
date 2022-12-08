#!/usr/bin/python

import argparse
import http.client
import json
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument("--env", help="Current Environment")
parser.add_argument("--token", help="CircleCI Token")
parser.add_argument("--owner", help="CircleCI Owner ID")

args = parser.parse_args()

circle_token = args.token
circle_owner_id = args.owner
env = args.env

connection = http.client.HTTPSConnection("circleci.com")
headers = {
    "Circle-Token": circle_token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

contexts_url = f"/api/v2/context?owner-id={circle_owner_id}"
connection.request("GET", contexts_url, headers=headers)
contexts = json.loads(connection.getresponse().read().decode("utf-8"))

context_id = ""

for item in contexts["items"]:
    if env in item["name"]:
        context_id = item["id"]

env_variables_url = f"/api/v2/context/{context_id}/environment-variable?page-token={circle_token}"
connection.request("GET", env_variables_url, headers=headers)
variables = json.loads(connection.getresponse().read().decode("utf-8"))

while variables["next_page_token"] is not None:
    next_page_token = variables["next_page_token"]
    next_env_variables_url = f"{env_variables_url}?page-token={next_page_token}"
    connection.request("GET", next_env_variables_url, headers=headers)
    next_variables = json.loads(connection.getresponse().read().decode("utf-8"))
    variables["next_page_token"] = next_variables["next_page_token"]
    variables["items"] += next_variables["items"]

env_vars = ""

for var in variables["items"]:
    env_vars += f'{var["variable"]}=${var["variable"]}%s\\n\n'

command = f'touch .env.{env};' \
          f'printf "\n{env_vars}" > .env.{env};'

ret = subprocess.run(command, capture_output=True, shell=True)
print(ret.stdout.decode())
