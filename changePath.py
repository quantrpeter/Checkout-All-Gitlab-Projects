import requests
import json
import urllib3
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="changePath.py",
    description="change all git path",
)
parser.add_argument("--dir", help="directory")
args = parser.parse_args()

if args.dir == None:
    parser.print_help()
    exit(1)
    
from os import listdir

for f in listdir(args.dir):
	if (Path(args.dir+'/'+f+'/'+'.git').is_dir()):
		print(f)
		temp=os.popen("cd "+args.dir+'/'+f+"; git remote show origin | grep Push").read()
		temp=temp.split("URL:")[1].strip()
		if "https://gitlab.com" in temp:
			newUrl=temp.replace("gitlab.com", "gitlab.quantr.hk")
			print(temp+" > "+newUrl)
			print("cd "+args.dir+'/'+f+"; git remote set-url origin "+newUrl)
			os.popen("cd "+args.dir+'/'+f+"; git remote set-url origin "+newUrl).read()
