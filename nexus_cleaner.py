from base64 import decode
from multiprocessing.connection import answer_challenge
from operator import index
import os
from webbrowser import get
from dotenv import load_dotenv
import requests
import json

load_dotenv()

repo = os.environ["REPOS"].split(",")
auth = (os.environ["NEXUS_USER"], os.environ["NEXUS_PASSWORD"])
base_url = 'https://' + os.environ["NEXUS_DOMAIN"] + '/service/rest/v1/components'

def getImages(url, repo):
  params = {'repository': repo}
  continuationToken = 1
  imagesFormating = []
  imagesList = []
  while continuationToken is not None:
    response = requests.get(url, auth=(auth[0],auth[1]), params=params)
    response = response.json()
    if "continuationToken" in response:
      cToken = {"continuationToken": response["continuationToken"]}
      continuationToken = cToken['continuationToken']
      params['continuationToken'] = continuationToken
      images = response['items']
      for image in images:
        imageName = image['name']
        imageVersion = image['version']
        imageID = image['id']
        imageFormat = '|{"id": "' + imageID + '", ' + '"name": "' + imageName + '", ' + '"version": "' + imageVersion + '"}'
        imagesFormating.append(imageFormat)
    imagesList.append(imagesFormating)
  return imagesList

def formatImages(url, repo):
  images = getImages(url, repo)
  imagesString = ''.join(map(str, images))
  imagesCleanString = imagesString.translate({ ord(c): None for c in "[']" })
  imageList = imagesCleanString.split("|")
  del imageList[0]
  return imageList

# В процессе
def sortedImages(url, repo):
  if repo != "nuget-hosted":
    images = formatImages(url, repo)
    for i in images:
      print(i)
    # print(images[1])
  else:
    print("This In nuget")

print(sortedImages(base_url, repo[0]))