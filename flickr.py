#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import FLICKR_URL
import flickr_api

class Flickr():
  def __init__(self, url):
    self.user = flickr_api.Person.getByUrl(url)
    self.photos = None
  
  def getInfo(self, photo):
    exif = photo.getExif()
    try:
      gps = photo.getLocation()
    except FlickrAPIError:
      return None

    r = {}
    r["id"] = photo.id
    r["title"] = photo.title
    r["thumbnail"] = photo.getPhotoFile("Square")
    r["photo_url"] = photo.getPageUrl()
    r["longitude"] = gps.longitude
    r["latitude"] = gps.latitude
    r["location_accuracy"] = gps.accuracy

    for e in exif:
      tag = e["tag"]
      raw = e["raw"]
      if tag == "Model":
        r["camera"] = raw
      if tag == "Lens":
        r["lens"] = raw
      if tag == "FNumber":
        r["fnumber"] = raw
      if tag == "ISO":
        r["iso"] = raw
      if tag == "FocalLength":
        r["focallength"] = raw
    return r

  def loadPhotos(self):   
    page = 1
    photos = []
    while True:
      res = self.user.getPublicPhotos(page=page,per_page=200)
      photos += res.data
#break
      if page >= res.info.get("pages"):
        break
      page += 1
      """
      break
      """
    # Add exif
    self.flickrobj = photos
    self.photos = filter(lambda l: l != None, map(lambda l: self.getInfo(l), photos))

if __name__ == "__main__": 
  f = Flickr(FLICKR_URL)
  f.loadPhotos()
