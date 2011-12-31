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

f = flickr.Flickr(config.FLICKR_USER)

@app.route("/json")
def return_photos():
    return json.dumps({"markers": f.toJson()})

@app.route("/")
def main():
    template = env.get_template('map.htm')
    return template.render(title=config.TITLE, google_api_key=config.GOOGLE_MAPS_KEY)

if __name__ == "__main__":
#    app.debug = True
    app.run(port=15000)
