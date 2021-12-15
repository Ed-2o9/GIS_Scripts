##This tool searches for duplicates in a field and adds a number to the end.
## Started 12/10/21


import arcpy

# Get the first parameter. The feature layer you need to search for duplicates.
inputFt = arcpy.GetParameter(0)

# Get the second parameter. The attribute in the feature layer to search for dupes.
inputFtAtt = arcpy.GetParameter(1)

# Output dataset name
outData = str(inputFt) + "_Dupes"

# If the duplicate file exist, display message. If the dupe table does not exist, create one.
if arcpy.Exists(outData):
    arcpy.AddMessage("Data already exist.")
else:
    # Use FindIdentical to find duplicates.
    arcpy.management.FindIdentical(inputFt, outData, inputFtAtt,output_record_option = "ONLY_DUPLICATES")


# create the fields for the search cursor
scfield = ['IN_FID', 'FEAT_SEQ']
# create a count variable for the loop.
curcount = 0
# create two list for the attributes.
infid = []
featseq = []

# If duplicate file has been created, start the process to correct dupes.
if arcpy.Exists(outData):
   with arcpy.da.SearchCursor(outData, scfield) as cursor:
        for row in cursor:
            infid.append(row[0])
            featseq.append(row[1])
            curcount += 1

# Create the dupecount variable to count dupes.
dupecount = 0


for i in range(len(featseq)):
    # Sets variable to compare first to the second duplicate.
    if i == 0:
        h = i + 1

    # Sets variable to compare current duplicate to the previous duplicate.
    if i > 0:
        h = i - 1
    # Compares duplicates and if they are ==, increments dupecount.
    if featseq[i] == featseq[h]:
        dupecount += 1

    if featseq[i] != featseq[h]:
        dupecount = 1

    if dupecount >= 2:
        arcpy.AddMessage(infid[i])
        selectstat = "OBJECTID =" + str(infid[i])
        arcpy.SelectLayerByAttribute_management(inputFt, "NEW_SELECTION", selectstat )
        with arcpy.da.UpdateCursor(inputFt,str(inputFtAtt)) as cursor:
            for row in cursor:
                row[0] = str(row[0]) + "_" + str(dupecount)
                arcpy.AddMessage(row[0])
