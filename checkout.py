import requests
import json
import urllib3
import argparse
import os

parser = argparse.ArgumentParser(
    prog="checkout.py",
    description="checkout all gitlab projects",
    epilog="Text at the bottom of help",
)
parser.add_argument("--username", help="Gitlab username")
parser.add_argument("--token", help="Gitlab api token")
args = parser.parse_args()

if args.token == None:
    parser.print_help()
    exit(1)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = args.token
username = args.username
pageSize = 100
pageNo = 1
size = pageSize

projects = []

while size == pageSize:
    url = (
        "https://gitlab.com/api/v4/projects?private_token="
        + token
        + "&membership=true&order_by=name&per_page="
        + str(pageSize)
        + "&page="
        + str(pageNo)
    )
    print(url)
    response = requests.get(url, verify=False)
    # print(response.content)
    j = json.loads(response.content)
    for x in range(len(j)):
        projects.append(
            {
                "name": j[x]["name"],
                "path": j[x]["path"],
                "url": j[x]["http_url_to_repo"],
            }
        )
        # print(str(x) + " = " + j[x]["name"])
        # print(j[x])
    size = len(j)
    pageNo += 1

for x in range(len(projects)):
    print(
        str(x)
        + " = "
        + projects[x]["name"]
        + "\t=\t"
        + projects[x]["path"]
        + "\t=\t"
        + projects[x]["url"]
    )
    if os.path.isdir(projects[x]["path"]):
        print(projects[x]["path"] + " existed")
        os.system("cd " + str(projects[x]["path"]) + "; git pull")
    else:
        url = projects[x]["url"]
        url = url.replace(
            "https://", "https://" + str(username) + ":" + str(token) + "@"
        )
        os.system("git config user.email peter@quantr.hk;git clone " + url)
