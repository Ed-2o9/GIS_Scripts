import arcpy
import os

# Grabs first parameter from script tool. This should be the feature that needs names.
inputFtN = arcpy.GetParameter(0)

# Grabs second parameter. This should be the grid feature.
inputGrid = arcpy.GetParameter(1)

# SQL query for selection of Nulls and names that contain by XXX.
queryState = "FACILITYID IS NULL Or FACILITYID LIKE '%XXX%' Or FACILITYID LIKE '%_'"

# Search for Nulls in the feature that needs a name.
arcpy.SelectLayerByAttribute_management(inputFtN, "NEW_SELECTION", queryState)

# Creates a temporary feature layer from the selected items
arcpy.MakeFeatureLayer_management(inputFtN, "FtN_lyr")

# Creates a variable that holds the layer name made in the previous step.
Ftn_Layer = "FtN_lyr"

# Gets the count of the features in FtN_lyr
result = arcpy.GetCount_management("FtN_lyr")

# Creates the text for the message that tells how many features are selected
message1 = "Number of features selected " + str(result)

# Adds message to scripting tool details
arcpy.AddMessage(message1)

# Selects inputGrid that intersects the layer of nulls
arcpy.SelectLayerByLocation_management(inputGrid, "INTERSECT", Ftn_Layer)

# Creates a temporary feature layer from the selected Grids
arcpy.MakeFeatureLayer_management(inputGrid, "inGrid_lyr")

# Creates a variable that holds the layer name made in the previous step.
Grid_Layer = "inGrid_lyr"

# Stores a count of selected Grids as a variable.
result2 = arcpy.GetCount_management(Grid_Layer)

# Stores the message to be shown in a variable.
message2 = "Number of Grids selected " + str(result2)

# Displays the message in tool details.
arcpy.AddMessage(message2)

arcpy.SelectLayerByAttribute_management(inputGrid, 'CLEAR_SELECTION')
arcpy.SelectLayerByAttribute_management(inputFtN, 'CLEAR_SELECTION')

# Creates a list to store grid numbers.
GridNumList = []
# Creates a list to store facilityID.
datalist = []
# Create a string that will later notate the data type.
dataType = ""
# Determine Data type
with arcpy.da.SearchCursor(inputFtN, 'FACILITYID') as cursor:
    for D in cursor:
        datalist.append(str(D))

if ("SV" in datalist[0]):
    dataType = "SV"
if ("WL" in datalist[0]):
    dataType = "WL"
arcpy.AddMessage(dataType)

# 1. Creates a cursor on the selected Grids.
# 2. Creates messages showing the Grid numbers.
# 3. Appends the Grid number for that row into a list.
with arcpy.da.SearchCursor(Grid_Layer, "NewGridNo") as cursor:
    for row in cursor:
        arcpy.AddMessage(row)
        rowStr = str(row)
        rowStr = rowStr[2:7]
        GridNumList.append(rowStr)

# 1.Loops through grid numbers selecting that grid.
for grid in GridNumList:
    rowquery = """{} LIKE '%{}%'""".format("NewGridNo", str(grid))
    arcpy.AddMessage(rowquery)
    arcpy.SelectLayerByAttribute_management(inputGrid, "NEW_SELECTION", rowquery)
# Select from the input feature that intersects the selected Grid.
    arcpy.SelectLayerByLocation_management(inputFtN, "INTERSECT", inputGrid)
# Printing out selected point count to check if it's working.
    pCount = arcpy.GetCount_management(inputFtN)
    arcpy.AddMessage(pCount)
    vcount = 0
    vname = ""


# Start an update cursor to go through FACILITYID attribute.
    with arcpy.da.UpdateCursor(inputFtN, 'FACILITYID') as cursor:
        for x in cursor:
# Check to see if it's a System Valve and count it.
            if (dataType in str(x)) and ("XXX" not in str(x)):
                vcount = vcount + 1
# Check to see if it is not named properly or maybe a stupid hydrant that snuck in here.
            if (dataType not in str(x) or "XXX" in str(x)) and ("FH" not in str(x)):
                vcount = vcount + 1
                if vcount < 100:
                    vname = str(grid) + "_" + dataType + "0" + str(vcount)
                if vcount > 100:
                    vname = str(grid) + "_" + dataType + str(vcount)
# Updates the Features Facility ID
                arcpy.AddMessage(vname)
                x = vname
                cursor.updateRow([x])

