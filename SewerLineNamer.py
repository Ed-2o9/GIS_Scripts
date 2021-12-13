import arcpy

# Grabs first parameter from script tool. This should be the feature that needs names.
inputFtN = arcpy.GetParameter(0)

# Grabs Manhole parameter
inputMH = arcpy.GetParameter(1)

# Grabs Grid parameter. This should be the grid feature.
inputGrid = arcpy.GetParameter(2)

# SQL query for selection of Nulls and names that contain by XXX.
queryState = "FACILITYID IS NULL OR FACILITYID = '1'"

#Select sewer line that need names
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

# Create a list to store sewer main object ID's.
MobjID = []

with arcpy.da.SearchCursor(Ftn_Layer, "OBJECTID") as cursor:
    for row in cursor:
        rowstr = str(row)
        rowstr = rowstr.replace(")","")
        rowstr = rowstr.replace("(" ,"")
        rowstr = rowstr.replace(",","")
        MobjID.append(rowstr)

mHole = []
for m in MobjID:
    rowquery = """{} = {}""".format("OBJECTID", str(m))
# Select the feature to be named by object ID.
    arcpy.SelectLayerByAttribute_management(inputFtN, "NEW_SELECTION", rowquery)
# Grab the intersecting Grid.
    arcpy.SelectLayerByLocation_management(inputGrid, "INTERSECT", inputFtN)
# Making the gridname to help create the FACILITYID.
    with arcpy.da.SearchCursor(inputGrid,"NewGridNo")as cursor:
        for row in cursor:
            gridname = str(row[0])
# Select manholes that intersect with the sewer line.
    arcpy.SelectLayerByLocation_management(inputMH, "INTERSECT", inputFtN)
# Create a variable that holds the manholes that intersect count.
    gcount = arcpy.GetCount_management(inputMH)
    if str(gcount) == "2" :
        with arcpy.da.SearchCursor(inputMH, "FACILITYID") as cursor:
            for row in cursor:
                mHole.append(str(row)[8:13])
        mhName1 = mHole.pop()
        mhName2 = mHole.pop()
        mlname = gridname + "_"+ mhName2 + mhName1
        mlname = mlname.replace("'", "")
    if str(gcount) == "1" :
        with arcpy.da.SearchCursor(inputMH, "FACILITYID") as cursor:
            for row in cursor:
                mHole.append(str(row)[8:13])
        mhName1 = mHole.pop()
        mhName2 = "MHXXX"
        mlname = gridname + "_" + mhName1 + mhName2
        mlname = mlname.replace("'", "")
    if str(gcount) == "0" :
        mhName1 = "MHXXX"
        mhName2 = "MHXXX"
        mlname = gridname + "_" + mhName1 + mhName2
        mlname = mlname.replace("'", "")

    arcpy.AddMessage(mlname)
    arcpy.AddMessage(gridname)

    with arcpy.da.UpdateCursor(inputFtN, "FACILITYID", rowquery) as cursor:
        for row in cursor:
            row = mlname

            arcpy.AddMessage(row)
            cursor.updateRow([row])
