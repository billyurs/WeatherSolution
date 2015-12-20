from django.http import HttpResponse
import urllib.request
import simplejson
#import request

def getweatherdetails(request):
    querydetails = request.GET.get("details","").split("|")
    daysflag = False
    hoursdet = 0
    daysno=''
    windDet = False
    for par in querydetails:
        if 'place' in par:
            placenamelist = par.split(':')[1:]
        elif 'daysflag' in par:
            daysflag = True
        elif 'hoursdet' in par:
            hoursdet = int(par.split(':')[1])
        elif 'daysno' in par:
            daysno = int(par.split(':')[1])
        elif 'wind' in par:
            windDet = True
    weatherJSON = {}
    for place in placenamelist:
        place = place.replace(' ','%20')
        url = 'http://api.openweathermap.org/data/2.5/weather?q='+place+',in&appid=2de143494c0b295cca9337e1e96b00e0'
        resp = urllib.request.urlopen(url).read()
        try:
            data = simplejson.load(resp)
        except:
            data = eval(resp)
        if daysflag == True:
            coordinates = data['coord']
            latitude , longitude = str(coordinates.get('lat', '')), str(coordinates.get('lon', ''))
            url = 'http://api.openweathermap.org/data/2.5/forecast?lat='+latitude+'&lon='+longitude+'&appid=2de143494c0b295cca9337e1e96b00e0'
            resp =urllib.request.urlopen(url).read()
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
            tempJson = {}
            listJson = []
            for key in listDet:
                #if today == key.get('dt_txt',''):
                iterJson = {}
                iterJson['Date'] = key.get('dt_txt','')
                iterJson['Exact Temperature'] = convertKelvinToCelcuis(request, key.get('main', {}).get('temp','Not Available Right Now'))
                iterJson['Max Temperature'] =  convertKelvinToCelcuis(request, key.get('main', {}).get('temp_max','Not Available Right Now'))
                iterJson['Min Temperature'] = convertKelvinToCelcuis(request, key.get('main', {}).get('temp_min','Not Available Right Now'))
                descritpion = key.get('weather', {})
                iterJson['Exact Description'] = descritpion[0].get('description', 'No Data Right Now') +":"+ descritpion[0].get('main', '')
                time  = time + hoursdet
                if windDet == True:
                    iterJson['WindDegree'] = data.get('wind', {}).get('deg', '')
                    iterJson['speed'] = data.get('wind', {}).get('speed', '')
                #tempJson[key.get('dt_txt','')] = iterJson
                listJson.append(iterJson)
            weatherJSON['weather'] = listJson
        else:
            #weatherJSON['DateTime'] = data.get('dt_txt','')
            tempjson = {}
            tempjson['Exact Temperature'] = convertKelvinToCelcuis(request, data.get('main', {}).get('temp','Not Available Right Now'))
            tempjson['Max Temperature'] =  convertKelvinToCelcuis(request, data.get('main', {}).get('temp_max','Not Available Right Now'))
            tempjson['Min Temperature'] = convertKelvinToCelcuis(request, data.get('main', {}).get('temp_min','Not Available Right Now'))
            descritpion = data.get('weather', {})
            tempjson['Exact Description'] = descritpion[0].get('description', 'No Data Right Now') +":"+ descritpion[0].get('main', '')
            weatherJSON[data.get('dt_txt','weather')] = tempjson
    return HttpResponse(simplejson.dumps(weatherJSON))

def convertKelvinToCelcuis(request, temp):
    celsuis = temp - 273.15
    return str(float(celsuis))

def payment(request):
    import paypalrestsdk
    paypalrestsdk.configure({
      'mode': 'sandbox',
      'client_id': 'EBWKjlELKMYqRNQ6sYvFo64FtaRLRR5BdHEESmha49TM',
      'client_secret': 'EO422dn3gQLgDbuwqTjzrFgFtaRLRR5BdHEESmha49TM'
    })
    payment = paypalrestsdk.Payment({
  "intent": "sale",
  "payer": {
    "payment_method": "credit_card",
    "funding_instruments": [{
      "credit_card":{
        "type": "visa",
        "number": "4446283280247004",
        "expire_month": "11",
        "expire_year": "2018",
        "cvv2": "874",
        "first_name": "Joe",
        "last_name": "Shopper" }}]},
  "transactions": [{
    "amount": {
      "total": "12",
      "currency": "USD" },
    "description": "creating a direct payment with credit card" }]})

    status = payment.create()
    return HttpResponse(status)



