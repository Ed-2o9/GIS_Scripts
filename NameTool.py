import arcpy
import os

# Grabs first parameter from script tool. This should be the feature that needs names.
inputFtN = arcpy.GetParameter(0)

# Grabs second parameter. This should be the grid feature.
inputGrid = arcpy.GetParameter(1)

# SQL query for selection of Nulls and names that contain by XXX.
queryState = "FACILITYID IS NULL Or FACILITYID LIKE '%XXX%'"

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
arcpy.SelectLayerByLocation_management(inputGrid,"INTERSECT", Ftn_Layer)

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

# Creates a list to store grid numbers.
GridNumList=[]

# 1. Creates a cursor on the selected Grids.
# 2. Creates messages showing the Grid numbers.
# 3. Appends the Grid number for that row into a list.
cursor = arcpy.da.SearchCursor(Grid_Layer, "NewGridNo")
for row in cursor:
    arcpy.AddMessage(row)
    rowStr = str(row)
    rowStr = rowStr[2:7]
    GridNumList.append(rowStr)

# Loops through grid numbers selecting that grid.
for grid in GridNumList:
    rowquery = """{} LIKE '%{}%'""".format("NewGridNo", str(grid))
    arcpy.AddMessage(rowquery)
    arcpy.SelectLayerByAttribute_management(inputGrid,"NEW_SELECTION", rowquery)