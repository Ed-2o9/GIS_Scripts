
import arcpy

inputftf = arcpy.GetParameter(0)


with arcpy.da.UpdateCursor(inputftf,"FACILITYID") as cursor:
    for row in cursor:
        if len(row) < 5 and row != "1" :
            row = "1"
            arcpy.AddMessage(str(row))
            cursor.updateRow([row])




