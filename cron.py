import urllib.request
import simplejson
#from WeatherAPI.WeatherGrab.views import getweatherdetails
import requests


#TODO Call from DB to configureplace
request = requests.Request
request.url = 'http://sparkapp.pythonanywhere.com/?details=place:sakleshpur|daysflag:True|wind:True|'
message = resp = urllib.request.urlopen(url).read()
numbers = '9164531299'
url = 'http://api.textlocal.in/send/?'
user =  "username=" + "raghucssit@gmail.com"
hash = "&hash=" + "2846fb8a13c7d7cee4117e8aa7adc3d45d5afd8e"
sender = "&sender=" + "TXTLCL"
data = user + hash + numbers + message + sender;
resp = urllib.request.urlopen(url%data).read()