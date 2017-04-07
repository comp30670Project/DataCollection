# imports
import time
import SQL.sqlClass as sc
import JSON.jsonData as jd

def getData(configFile, apiDB, apiOW):

	# create the SQL table (will ignore it if it already exists)
	projectTable = sc.sqlTable(configFile) # sqlTable object
	projectTable.create() # update the database

	# scrape the data
	jsonData = jd.ProjectData(apiDB, apiOW).getData()

	# populate the SQL table
	projectTable.add_data(jsonData)

# getData("SQL/sqlConfig.txt", "JSON/apiDB.txt", "JSON/apiOW.txt")

def scrapeData(configFile, apiDB, apiOW):

	while True:

		try:

			# set the start time
			start = time.time()

			# getData
			getData(configFile, apiDB, apiOW)

			# cycle every five minutes
			wait = max(0, 300 - time.time() + start)
			time.sleep(wait)

		except:

			# wait one minute until trying again
			time.sleep(60)


# make sure the program only runs as a stand alone entity; not as an add on
if __name__ == '__main__':
	scrapeData("SQL/sqlConfig.txt", "JSON/apiDB.txt", "JSON/apiOW.txt")
else:
	print("This function is only meant to run by itself, not imported.")