from base64 import decode
from cgi import print_arguments
from multiprocessing.connection import answer_challenge
from operator import index
import os
import re
from unicodedata import name
from unittest import result
from webbrowser import get
from dotenv import load_dotenv
import requests
import itertools
import json

load_dotenv()

repo = os.environ["REPOS"].split(",")
auth = (os.environ["NEXUS_USER"], os.environ["NEXUS_PASSWORD"])
base_url = 'https://' + os.environ["NEXUS_DOMAIN"] + '/service/rest/v1/components'

def getImages(url, repo):
  params = {'repository': repo}
  images = []
  while True:
    response = requests.get(url, auth=(auth[0],auth[1]), params=params)
    response = response.json()
    for image in response['items']:
      imageName = image['name']
      imageVersion = image['version']
      imageID = image['id']
      imageFormat = {
        "id" : imageID,
        "name" : imageName,
        "version" : imageVersion
        }
      images.append(imageFormat)

    continuationToken = response['continuationToken']

    if continuationToken is None:
      break

    cToken = {"continuationToken": response["continuationToken"]}
    continuationToken = cToken['continuationToken']
    params['continuationToken'] = continuationToken

  return images


def deleteList(url, repo):
  if repo != "nuget-hosted":
    images = getImages(url, repo)
    images.sort(key=lambda image: image['name'])
    imagesList = itertools.groupby(images, lambda image: image['name'])

    for name, group in imagesList:
      print('name', name)
      for i in group:
        version = i['version']
        result = re.search(r'\D', version[0])
        if result == None:
          print(version)
    # print(imagesNameList)
  else:
    print("This In nuget")

print(deleteList(base_url, repo))