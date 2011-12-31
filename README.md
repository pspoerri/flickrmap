Flickr Map
==========

A simple Google Maps Flickr Profile viewer. 

You can see it "live" on http://map.pascalspoerri.ch

Install
-------

```
git clone git@github.com:moeeeep/flickrmap.git
sudo apt-get install python-flickrapi
```

You're done. 

Configuration
-------------
Create a new config file: config.py

And set the following settings:

```python
TITLE = "Title"
GOOGLE_MAPS_KEY = "Google API Key"
GOOGLE_ANALYTICS = "analytics key" ## Not needed (if you don't want to run Analytics, put some random value here...)

FLICKR_USER = "13538696@N02
FLICKR_API_KEY   = "flickr api key"
FLICKR_API_SECRET = "flickr api secret" ## Not needed right now
```

Running
-------

You can start it with:

```
 python __init__.py
```
