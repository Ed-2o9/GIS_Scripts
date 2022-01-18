#This tool compares two feature layers of census data to determine what data changed per block between the dates.

import arcpy

# Variable for 2020 census data
input2020 = arcpy.GetParameter(0)


# Variable for 2010 census data
input2010 = arcpy.GetParameter(1)

# Variable for the list of 2010 blockID
block10 = []

# Variable for search cursor field.
sfield= 'BLOCKCE'

# Search cursor to create the list of census blocks from 2010
with arcpy.da.SearchCursor(input2010, sfield) as cursor:
    blockid = str(row)
    blockid = blockid.replace(")", "")
    blockid = blockid.replace("(", "")
    blockid = blockid.replace(",", "")