class DublinBikes():

	
	def __init__(self, fileName):

		# INPUTS
		# fileName: the file name of the file containing the API key

		# ATTRIBUTES
		self.fileName = fileName

	
	def apiKey(self):
	
		# OUTPUT
		## Dublin Bikes API key
		## https://developer.jcdecaux.com/#/opendata/vls?page=getstarted

		# creating the DB API key
		with open(self.fileName, "r") as f: # make a file the contains your api key
			theKey = f.readline()
			dbKey = "&apiKey=" + theKey

		# output
		return dbKey

	
	def data_modification_position(theDict):

		# INPUT: dictionary
		# OUTPUT: a list in which the constituant dictionaries have each had a sub-dictionary removed and replaced by two key value pairs

		# modify lat and lon
		lat = theDict['position']['lat']
		lon = theDict['position']['lng']
		del theDict['position']
		theDict['lat'] = lat
		theDict['lon'] = lon

		return theDict

	
	def data_modification_last_update(theDict):

		# INPUT: dictionary
		# OUTPUT: a list in which the constituant dictionaries have each had a Unix UTC timestamp changed to a human readable string

		# imports
		from time import gmtime, strftime

		theInt = theDict['last_update']

		# convert from miliseconds to seconds
		theInt = int(theInt / 1000)

		# convert to human readable time
		theInt = gmtime(theInt)

		theDict['last_update'] = strftime("%Y %b %d %H:%M:%S", theInt)

		# return
		return theDict


	def boolean_to_sql(theBoolean):

		# INPUT: a Boolean value
		# OUTPUT: 1 for True; 0 for otherwise

		if theBoolean == True:
			return 1
		else:
			return 0

	def data_modification_boolean_to_sql(theDict):

		# INPUT: dictionary
		# OUTPUT: dictionary with boolean values appropriate for sql

		theDict['banking'] = DublinBikes.boolean_to_sql(theDict['banking'])
		theDict['bonus'] = DublinBikes.boolean_to_sql(theDict['bonus'])

		return theDict


	def status_to_sql(theStatus):

		# INPUT: the status of a DB station
		# OUTPUT: 1 for OPEN; 0 for otherwise

		if theStatus == 'OPEN':
			return 1
		else:
			return 0


	def data_modification_status_to_sql(theDict):

		# INPUT: dictionary
		# OUTPUT: dictionary with status values appropriate for sql

		theDict['status'] = DublinBikes.status_to_sql(theDict['status'])

		return theDict

	
	def getData(self):

		# OUTPUT
		## Python list of dictionary entries of the Dublin Bikes contract

		# imports
		import json
		import urllib.request
		import urllib.error
		import time

		# url
		api = self.apiKey()
		url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin" + api

		# get data
		got_data = False
		
		while got_data is False:

			try:
				with urllib.request.urlopen(url) as response:
					stringData = response.read()
					listData = json.loads(stringData)

				got_data = True
			
			except:
				# DB api may be down or otherwise inaccessible; give it some time
				time.sleep(60)


		# modifications
		for d in listData:
			DublinBikes.data_modification_position(d)
			DublinBikes.data_modification_last_update(d)
			DublinBikes.data_modification_boolean_to_sql(d)
			DublinBikes.data_modification_status_to_sql(d)

		# output
		return listData
	

# # DublinBikes tests
# db = DublinBikes("apiDB.txt")
# dbKey = db.apiKey()
# dbData = db.getData()
# print(dbKey)
# print(dbData)