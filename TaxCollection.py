# Import Libraries
from arcgis.gis import GIS
from arcgis import features
import pandas as pd
import glob
import arcpy
from arcpy import env
import os

arcpy.env.overwriteOutput = True

# Connect to the GIS
gis = GIS(username="****", password="****")
#print(gis.properties.user.username)

# read the initial csv
rent = pd.read_csv("D:\\Esri\\rent_2022.csv")

# assign variable to current timestamp to make unique file to add to portal
import datetime as dt
now = int(dt.datetime.now().timestamp())

# add the csv as an item
item_prop = {'title':'TAX collection spreadsheet_' + str(now)}
csv_item = gis.content.add(item_properties=item_prop, data="D:\\Esri\\rent_2022.csv")
# publish the csv item into a feature layer
cities_item = csv_item.publish()
csv_item.publish()

# read the second csv set
rent_new = pd.read_csv("D:\\Esri\\rent_2022_D.csv")

env.workspace = r"D:\Esri\TaxCollection\TaxCollection.gdb"

# specifying the path to csv files
path = r"D:\Esri\Rent"
pathNames = os.listdir(path)
os.listdir(path)

# csv files in the path
files = glob.glob(path + "/*.csv")

x = 0
for file in files:
    arcpy.TableToTable_conversion(file, r"D:\Esri\TaxCollection\TaxCollection.gdb",
                                  f"{pathNames[x]}")
    x += 1

# list of fields for search cursor
sField = ['First_Name', 'Last_Name', 'Room', 'Rent', 'lat', 'long']
# field names to be used in a csv
TaxesFields = ["First_Name,Last_Name,Room,Rent,lat,long"]

Taxes = "Taxes"
# create a search cursor
sCursor = []
with arcpy.da.SearchCursor(Taxes,sField) as sCursor:
    for row in sCursor:
        rowText = f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}"
        TaxesFields.append(rowText)
del sCursor

# Write hotels to a CSV file
textBody = '\n'.join(TaxesFields)
csvFile = open(r"D:\Esri\AllTaxes.csv", "w")
csvFile.write(textBody)
csvFile.close()

# Get and print a list of tables
tables = arcpy.ListTables()

# Adding new data to AllTaxes1
NewTaxes = [""]

# list of fields for search cursor
sField = ['First_Name', 'Last_Name', 'Room', 'Rent', 'lat', 'long']

#TaxesNew = "Taxes_New"
sCursor = []
y = 0
for table in tables:
    with arcpy.da.SearchCursor(f"{tables[y]}", sField) as sCursor:
        for row in sCursor:
            rowText = f"{row[0]}, {row[1]},{row[2]},{row[3]},{row[4]},{row[5]}"
            NewTaxes.append(rowText)
    del sCursor
    y += 1
    # write the new data to the existing csv
    textBody = "\n".join(NewTaxes)
    New_csvFile = open(r"D:\Esri\AllTaxes.csv", "a")
    New_csvFile.write(textBody)
    New_csvFile.close()

from arcgis.features import FeatureLayerCollection
Taxes_collection = FeatureLayerCollection.fromitem(cities_item)

#call the overwrite() method which can be accessed using the manager property
Taxes_collection.manager.overwrite(r"D:\Esri\AllTaxes.csv")
