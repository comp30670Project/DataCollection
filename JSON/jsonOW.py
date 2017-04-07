class OpenWeather():

	def __init__(self, fileName):

		# INPUTS
		# fileName: the file name of the file containing the API key

		# ATTRIBUTES
		self.fileName = fileName


	def apiKey(self):
		
		# OUTPUT
		## Open Weather API key

		# attach API key
		with open(self.fileName, "r") as f: # make af file the contains your api key
			theKey = f.readline()
			owID = "&appid=" + theKey

		# output
		return owID


	def data_modification_ow_times(theInt):

		# imports
		from time import gmtime, strftime

		# convert to human readable time
		theInt = gmtime(theInt)

		# return
		return strftime("%Y %b %d %H:%M:%S", theInt)


	def getData(self, lat, lon):

		# imports
		import json
		import urllib.request
		import time

		# url
		urlRoot = "http://api.openweathermap.org/data/2.5/weather?"
		urlUnits = "units=metric"
		urlLat = "&lat=" + str(lat)
		urlLon = "&lon=" + str(lon)
		api = self.apiKey()
		url = urlRoot + urlUnits + urlLat + urlLon + api

		# get data
		got_data = False
		while got_data is False:
			try:

				with urllib.request.urlopen(url) as response:
					stringData = response.read()
					dictData = json.loads(stringData)
					got_data = True
			except:
				# api may be down; sleep and try again
				time.sleep(60)

		# collect data from ow
		ow_weather = dictData['weather'][0] # dictionary object
		ow_main = dictData['main'] # dict object
		ow_wind = dictData['wind'] # dict object
		ow_sys = dictData['sys'] # dict object

		# make the data object to return
		ow = {}
		ow['Weather'] = ow_weather['description']
		ow['Temp'] = ow_main['temp']
		ow['TempMin'] = ow_main['temp_min']
		ow['TempMax'] = ow_main['temp_max']
		ow['Pressure'] = ow_main['pressure']
		ow['WindSpeed'] = ow_wind['speed']
		ow['WindDegree'] = ow_wind['deg']
		ow['SunRise'] = ow_sys['sunrise']
		ow['SunSet'] = ow_sys['sunset']

		# modififcations
		ow['SunRise'] = OpenWeather.data_modification_ow_times(ow['SunRise'])
		ow['SunSet'] = OpenWeather.data_modification_ow_times(ow['SunSet'])
		
		# return
		return ow

# # Open Weather Tests
# ow = OpenWeather("apiOW.txt")
# api = ow.apiKey()
# print(api)
# data = ow.getData(9, 135)
# print(data)