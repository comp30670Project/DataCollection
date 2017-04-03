# imports
import mysql
import mysql.connector

class sqlConfig():

	def __init__(self, configFile):

		# INPUTS
		# configFile: the name of the file containing the sql configuration information

		# Attributes
		self.configFile = configFile

	def sql_configuration_dictionary(self):
		
		theDict = {}
		with open(self.configFile, "r") as f:
			for line in f:
				content = line.strip().split(":")
				theDict[content[0]] = content[1]
		return theDict


class sqlTable():

	def __init__(self, configFile):

		# INPUTS
		# configFile: the name of the file containing the sql configuration information
		# dbCommand: dictionary containing the tuples containing the sql code to create a table
		
		# Attributes
		self.configFile = configFile

	def create(self):

		# configuration dictionary
		config = sqlConfig(self.configFile).sql_configuration_dictionary()

		# establish the connection
		cnx = mysql.connector.connect(**config)

		# create cursor object
		cursor = cnx.cursor()

		# use database
		cnx.database = config['database']

		# create the table
		dbTable = {}
		dbTable['dbProject'] = ("CREATE TABLE dbProject (""dbID int(11) AUTO_INCREMENT, ""number int(11), ""name VARCHAR(4),  ""address VARCHAR(64), ""banking tinyint(1), ""bonus tinyint(1), ""status tinyint(1), ""contract_name VARCHAR(4), ""bike_stands INT(3), ""available_bike_stands INT(3), ""available_bikes INT(3), ""last_update char(20), ""lat decimal(18,9), ""lon decimal(18,9), ""Weather VARCHAR(32), ""Temp DECIMAL(4,2), ""TempMin DECIMAL(4,2), ""TempMax DECIMAL(4,2), ""Pressure INT(6), ""Windspeed DECIMAL(5,2), ""WindDegree INT(3), ""Sunrise CHAR(20), ""SunSet CHAR(20), ""PRIMARY KEY (dbID)"") ")
		for key, value in dbTable.items():

			try:
				cursor.execute(value)

			except mysql.connector.Error as err:
				pass

		# close the cursor and connection
		cursor.close()
		cnx.close()

	def add_data(self, dataList):

		# INPUT
		# dataList: Python list resulting form jsonData.py

		# configuration dictionary
		config = sqlConfig(self.configFile).sql_configuration_dictionary()

		# establish the connection
		cnx = mysql.connector.connect(**config)

		# create cursor object
		cursor = cnx.cursor()

		sql = "insert into dbProject(number, name, address, banking, bonus, status, contract_name, bike_stands, available_bike_stands, available_bikes, last_update, lat, lon, Weather, Temp, TempMin, TempMax, Pressure, WindSpeed, WindDegree, SunRise, SunSet) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

		# iterate over items to update
		for d in dataList:
			dv = tuple(d.values())
			cursor.execute(sql, dv)

		# commit the changes
		cnx.commit()

		# close the cursor and connection
		cursor.close()
		cnx.close()