#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyleft 2011 Pascal Spörri <pascal.spoerri@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from config import FLICKR_USER, FLICKR_API_KEY, FLICKR_API_SECRET
import flickrapi
import json

class Flickr():
  def __init__(self, user_id):
    self.flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format='json', store_token=False)
    self.flickr.cache = flickrapi.SimpleCache(timeout=300, max_entries=200)
    self.user_id = user_id
    self.loadPhotos()
  def loadPhotos(self):
    print "Loading photos for user {user}".format(user=self.user_id)
    
    page = 1
    photos = []
    while True:
        print "Page", page
        result = self.flickr.people_getPublicPhotos(user_id=self.user_id, page=page, extras="geo,icon_server,description,url_sq, url_t, url_s, url_m, url_z, url_l,path_alias")
        j = json.loads(result)
        photos += j["photos"]["photo"]
        current_page = j["photos"]["page"]
        if current_page >= j["photos"]["pages"]:
          break
    
        page += 1
    self.f_photos = photos 
    self.photos = filter(lambda l: l["longitude"] != 0.0 and l["latitude"] != 0.0, map(lambda l: self.getInfo(l), self.f_photos))
    
  def getFlickrPage(self, photo):
    return "http://www.flickr.com/photos/{user}/{photo_id}".format(
        user=photo["pathalias"], photo_id=photo["id"])
  
  def getInfo(self, photo):
    r = {}
    r["id"] = photo["id"]
    r["title"] = photo["title"]
    r["thumbnail"] = photo["url_sq"]
    r["photo_url"] = self.getFlickrPage(photo)
    r["longitude"] = photo["longitude"]
    r["latitude"] = photo["latitude"]
    r["location_accuracy"] = photo["accuracy"]
    r["content"] = u'<a href="{link}/lightbox/" target="_blank"><img src="{thumbnail}" alt="{title}"></a> <b>{title}</b>'.format(
            link=r["photo_url"], thumbnail=r["thumbnail"], title=r["title"])
    return r


if __name__ == "__main__": 
  f = Flickr(FLICKR_USER)
  print f.photos
