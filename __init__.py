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

from flask import Flask
from jinja2 import Environment, PackageLoader, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
import math

import flickr
import config
import json

app = Flask(__name__)
app.static_path="static"
app.static_url_path="static/"

f = flickr.Flickr(config.FLICKR_USER)
per_page = 50

@app.route("/json")
def return_info():
    return json.dumps({"pages": int(math.ceil(len(f.photos)/float(per_page)))})

@app.route("/json/<page>")
def return_page(page):
    p = int(page)
    return json.dumps({"markers": f.photos[(p-1)*per_page:p*per_page]})

@app.route("/")
def main():
    template = env.get_template('map.htm')
    return template.render(title=config.TITLE, 
        google_api_key=config.GOOGLE_MAPS_KEY,
        google_analytics=config.GOOGLE_ANALYTICS)

if __name__ == "__main__":
#    app.debug = True
    app.run(port=15000)
