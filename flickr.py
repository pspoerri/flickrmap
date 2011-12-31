#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import FLICKR_USER, FLICKR_API_KEY
import flickrapi
import json

class Flickr():
  def __init__(self, user_id):
    self.flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, format='json')
    self.flickr.cache = flickrapi.SimpleCache(timeout=300, max_entries=200)
    self.user_id = user_id
    self.loadPhotos()
    self.json_dump = None
  def loadPhotos(self):
    print "Loading photos for user {user}".format(user=self.user_id)
    
    page = 1
    photos = []
    while True:
        print "Page", page
        result = self.flickr.people_getPublicPhotos(user_id=self.user_id, page=page, extras="geo,icon_server,description,url_sq, url_t, url_s, url_m, url_z, url_l,path_alias")
#        print result[14:-1]
        j = json.loads(result[14:-1])
        photos += j["photos"]["photo"]
        current_page = j["photos"]["page"]
        if current_page >= j["photos"]["pages"]:
          break
    
        page += 1
    self.f_photos = photos 
    self.photos = map(lambda l: self.getInfo(l), self.f_photos)

  def getFlickrPage(self, photo):
    return "http://www.flickr.com/photos/{user}/{photo_id}".format(
        user=photo["pathalias"], photo_id=photo["id"])
  
  def getInfo(self, photo):
    r = {}
    r["id"] = photo["id"]
    r["title"] = photo["title"]
    r["thumbnail"] = photo["url_sq"]
    r["photo_url"] = self.getFlickrPage(photo)+"/lightbox/"
    r["longitude"] = photo["longitude"]
    r["latitude"] = photo["latitude"]
    r["location_accuracy"] = photo["accuracy"]
    return r

  def toJson(self):
    if self.json_dump == None:
      json_photos = []
      for photo in self.photos:
        r = {}
        r["title"] = photo["title"]
        r["latitude"] = photo["latitude"]
        r["longitude"] = photo["longitude"]
        r["content"] = u"""<a href="{link}/lightbox/" target="_blank"><img src="{thumbnail}" alt="{title}"></a> <b>{title}</b>""".format(
            link=photo["photo_url"], thumbnail=photo["thumbnail"], title=photo["title"])
        json_photos.append(r)
      self.json_dump = json.dumps(json_photos)
    return self.json_dump

if __name__ == "__main__": 
  f = Flickr(FLICKR_USER)
  print f.photos
