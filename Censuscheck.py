#This tool compares two feature layers of census data to determine what data changed per block between the dates.

import arcpy

# Set workspace to default geodatabase
arcpy.env.workspace = "S:\GIS REPOSITORY\GIS_2021\GIS_Projects\Census_21_Confirm\Census_21_Confirm.gdb"

# Variable for 2020 census data
input2020 = arcpy.GetParameter(0)

# Variable for 2010 census data
input2010 = arcpy.GetParameter(1)

# Variable for the list of 2010 blockID
block10 = []

# Variable for search cursor field.
sfield= 'BLOCKCE'

count = 0

# Dictionary for 2010 Housing number.
house10 = {}

# Dictionary for 2010 Population number.
pop10 = {}


# Search cursor to create the list of census blocks from 2010
with arcpy.da.SearchCursor(input2010, sfield) as cursor:
    for row in cursor:
        blockid = str(row[0])
        blockid = blockid.replace(")", "")
        blockid = blockid.replace("(", "")
        blockid = blockid.replace(",", "")
        block10.append(blockid)


for b in block10:
    count += 1
    # Variable to hold selection variable.
    rowquery = """{} = '{}'""".format("BLOCKCE", str(b))
    arcpy.AddMessage(rowquery)
    # Select 2010 census block from list.
    arcpy.SelectLayerByAttribute_management(input2010, "NEW_SELECTION", rowquery)

    # Grab 2020 census blocks with their center located in the 2010 block.
    arcpy.SelectLayerByLocation_management(input2020, "HAVE_THEIR_CENTER_IN", input2010)

    arcpy.AddMessage(count)
