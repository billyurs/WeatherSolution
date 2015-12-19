from django.http import HttpResponse
import urllib2
import request
import simplejson

def getweatherdetails(request, placename, daysflag = False,hoursdet = 0,daysno='', windDet = False):
    placenamelist = placename.split('|')
    weatherJSON = {}
    for place in placenamelist:
        place = place.replace(' ','%20')
        url = 'http://api.openweathermap.org/data/2.5/weather?q='+place+',in&appid=2de143494c0b295cca9337e1e96b00e0'
        resp = data = urllib2.urlopen(url).read()
        try:
            data = simplejson.load(resp)
        except:
            data = eval(resp)
        if daysflag == True:
            coordinates = data['coord']
            latitude , longitude = str(coordinates.get('lat', '')), str(coordinates.get('lon', ''))
            url = 'http://api.openweathermap.org/data/2.5/forecast?lat='+latitude+'&lon='+longitude+'&appid=2de143494c0b295cca9337e1e96b00e0'
            resp = data = urllib2.urlopen(url).read()
            try:
                data = simplejson.load(resp)
            except:
                data = eval(resp)
            listDet = data.get('list', {})
            import datetime
            today = datetime.datetime.today().strftime('%m-%d-%Y-%H-%M')
            time = int(today.split('-')[3])
            moddiffofTime = time % 3
            time += moddiffofTime
            today = today.split('-')[0] +"-"+ today.split('-')[1] +"-"+ today.split('-')[2]+" "+str(time)+":00:00"
            for key in listDet:
                if today == key.get('dt_txt',''):
                    weatherJSON['DateTime'] = key.get('dt_txt','')
                    weatherJSON['Exact Temperature'] = convertKelvinToCelcuis(request, key.get('main', {}).get('temp','Not Available Right Now'))
                    weatherJSON['Max Temperature'] =  convertKelvinToCelcuis(request, key.get('main', {}).get('temp_max','Not Available Right Now'))
                    weatherJSON['Min Temperature'] = convertKelvinToCelcuis(request, key.get('main', {}).get('temp_min','Not Available Right Now'))
                    descritpion = key.get('weather', {})
                    weatherJSON['Exact Description'] = descritpion.get('description', 'No Data Right Now') + descritpion.get('main', '')
                    time  = time + hoursdet
        else:
            weatherJSON['DateTime'] = data.get('dt_txt','')
            weatherJSON['Exact Temperature'] = convertKelvinToCelcuis(request, data.get('main', {}).get('temp','Not Available Right Now'))
            weatherJSON['Max Temperature'] =  convertKelvinToCelcuis(request, data.get('main', {}).get('temp_max','Not Available Right Now'))
            weatherJSON['Min Temperature'] = convertKelvinToCelcuis(request, data.get('main', {}).get('temp_min','Not Available Right Now'))
            descritpion = data.get('weather', {})
            weatherJSON['Exact Description'] = descritpion.get('description', 'No Data Right Now') + descritpion.get('main', '')
        if windDet == True:
            weatherJSON['WindDegree'] = data.get('wind', {}).get('deg', '')
            weatherJSON['speed'] = data.get('wind', {}).get('speed', '')
            weatherJSON = simplejson.dumps(weatherJSON)
    HttpResponse(weatherJSON)

def convertKelvinToCelcuis(request, temp):
    celsuis = temp - 273.15
    return str(float(celsuis))
