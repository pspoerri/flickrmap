#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from jinja2 import Environment, PackageLoader, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

import flickr
import config
import json

app = Flask(__name__)
app.static_path="static"
app.static_url_path="static/"

f = flickr.Flickr(config.FLICKR_URL)
f.loadPhotos()
json_photos = []
for photo in f.photos:
  r = {}
  r["title"] = photo["title"]
  r["latitude"] = photo["latitude"]
  r["longitude"] = photo["longitude"]
  r["content"] = u"""<a href="{link}/lightbox/" target="_blank"><img src="{thumbnail}" alt="{title}"></a> <b>{title}</b>""".format(
      link=photo["photo_url"], thumbnail=photo["thumbnail"], title=photo["title"])
  json_photos.append(r)

@app.route("/json")
def return_photos():
    return json.dumps({"markers": json_photos})

@app.route("/")
def main():
    template = env.get_template('map.htm')
    return template.render(title=config.TITLE, google_api_key=config.GOOGLE_MAPS_KEY)

if __name__ == "__main__":
    app.run(port=6000,host="0.0.0.0")
