# imports
import time
from JSON.jsonDB import DublinBikes
from JSON.jsonOW import OpenWeather

class ProjectData():

	def __init__(self, apiDB, apiOW):
		
		# INPUTS
		# apiDB: the file name of the file containing the Dublin Bikes API key
		# apiOW: the file name of the file containing the Open Weather API key

		# ATTRIBUTES
		self.apiDB = apiDB
		self.apiOW = apiOW


	def getData(self):

		# get Dublin Bikes data
		DB = DublinBikes(self.apiDB).getData()

		# combine Dublin Bikes and Open Weather Data
		count = 0 # related to the Open Weather 60 calls a minute
		start = time.time() # related to the Open Weather 60 calls a minute
		for db in DB:
			
			# OW 60 calls per minute accomodation
			if count == 60:
				wait = max(0, 60 - (time.time() - start))
				time.sleep(wait)
				count = 0
				start = time.time()
			# count
			count += 1

			# get the Open Weather data
			lat = db['lat']
			lon = db['lon']
			OW = OpenWeather(self.apiOW).getData(lat, lon)

			# combine Dublin Bikes and Open Weather data
			for ow in OW:
				db[ow] = OW[ow]

		# return
		return DB
