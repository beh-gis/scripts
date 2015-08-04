import arcpy
from arcpy import env
env.overwriteOutput = True

geogsList = ['h','s']
radbufListFn = ['r0050m','r0100m','r0250m','r0500m','r1000m']
netbufListFn = ['n1000m']

print 'copy land areas and define projection and clean up fields'
for i in geogsList:
	for j in radbufListFn:
		print i + j
		arcpy.DefineProjection_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/merge/"+i+j+"/merge.shp","PROJCS['NAD_1983_StatePlane_New_York_Long_Island_FIPS_3104_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',984250.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-74.0],PARAMETER['Standard_Parallel_1',40.66666666666666],PARAMETER['Standard_Parallel_2',41.03333333333333],PARAMETER['Latitude_Of_Origin',40.16666666666666],UNIT['Foot_US',0.3048006096012192]]")
		arcpy.FeatureClassToFeatureClass_conversion("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/merge/"+i+j+"/merge.shp","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs",i+j+"_land.shp")
		arcpy.AddField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_land.shp","land_area","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_land.shp","land_area","!shape.area@squaremeters!","PYTHON_9.3","#")
		arcpy.DeleteField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_land.shp","y;x;ORIG_FID")

print 'add field and calc orig buffer area'
for i in geogsList:
	for j in radbufListFn:
		print i + j
		arcpy.AddField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_cir.shp","orig_area","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_cir.shp","orig_area","!shape.area@squaremeters!","PYTHON_9.3","#")

print 'export both orig and land area to csv'
for i in geogsList:
	for j in radbufListFn:
		arcpy.ExportXYv_stats("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_cir.shp","uid;orig_area","COMMA","V:/GIS/projects/naas/tasks/201502_naas_locations/data/tables/geogs/"+i+j+"_cir.csv","ADD_FIELD_NAMES")
		arcpy.ExportXYv_stats("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_land.shp","uid;land_area","COMMA","V:/GIS/projects/naas/tasks/201502_naas_locations/data/tables/geogs/"+i+j+"_land.csv","ADD_FIELD_NAMES")

print 'add field and calc network buffer area'
for i in geogsList:
	for j in netbufListFn:
		print i + j
		arcpy.AddField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+".shp","netb_area","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+".shp","netb_area","!shape.area@squaremeters!","PYTHON_9.3","#")

print 'export network buffer area to csv'
for i in geogsList:
	for j in netbufListFn:
		arcpy.ExportXYv_stats("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+".shp","uid;netb_area","COMMA","V:/GIS/projects/naas/tasks/201502_naas_locations/data/tables/geogs/"+i+j+".csv","ADD_FIELD_NAMES")

##########################################

print 'for radial buffers'

print 'intersect and then dissolve land areas and census 00 and 10'
for i in geogsList:
	for j in radbufListFn:
		arcpy.Intersect_analysis("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_land.shp #;V:/GIS/projects/naas/data/input/census/geogs/nyct2000.shp #","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00.shp","ALL","#","INPUT")
		arcpy.Intersect_analysis("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+"_land.shp #;V:/GIS/projects/naas/data/input/census/geogs/nyct2010.shp #","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10.shp","ALL","#","INPUT")
		arcpy.Dissolve_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00.shp","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","uid;geoid;ct2000area","#","MULTI_PART","DISSOLVE_LINES")
		arcpy.Dissolve_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10.shp","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","uid;geoid;ct2010area","#","MULTI_PART","DISSOLVE_LINES")

print 'add and calc new areas'
for i in geogsList:
	for j in radbufListFn:
		arcpy.AddField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","newarea","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","newarea","!shape.area@squaremeters!","PYTHON_9.3","#")
		arcpy.AddField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","newarea","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","newarea","!shape.area@squaremeters!","PYTHON_9.3","#")

print 'export intersects to csv'
for i in geogsList:
	for j in radbufListFn:
		arcpy.ExportXYv_stats("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","uid;geoid;ct2000area;newarea","COMMA","V:/GIS/projects/naas/tasks/201502_naas_locations/data/tables/census/"+i+j+"_land_int_ct00_dis.csv","ADD_FIELD_NAMES")
		arcpy.ExportXYv_stats("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","uid;geoid;ct2010area;newarea","COMMA","V:/GIS/projects/naas/tasks/201502_naas_locations/data/tables/census/"+i+j+"_land_int_ct10_dis.csv","ADD_FIELD_NAMES")

##########################################

print 'for network buffers'

print 'intersect and then dissolve land areas and census 00 and 10'
for i in geogsList:
	for j in netbufListFn:
		arcpy.Intersect_analysis("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+".shp #;V:/GIS/projects/naas/data/input/census/geogs/nyct2000.shp #","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00.shp","ALL","#","INPUT")
		arcpy.Intersect_analysis("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/geogs/"+i+j+".shp #;V:/GIS/projects/naas/data/input/census/geogs/nyct2010.shp #","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10.shp","ALL","#","INPUT")
		arcpy.Dissolve_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00.shp","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","uid;geoid;ct2000area","#","MULTI_PART","DISSOLVE_LINES")
		arcpy.Dissolve_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10.shp","V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","uid;geoid;ct2010area","#","MULTI_PART","DISSOLVE_LINES")

print 'add and calc new areas'
for i in geogsList:
	for j in netbufListFn:
		arcpy.AddField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","newarea","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","newarea","!shape.area@squaremeters!","PYTHON_9.3","#")
		arcpy.AddField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","newarea","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","newarea","!shape.area@squaremeters!","PYTHON_9.3","#")

print 'export intersects to csv'
for i in geogsList:
	for j in netbufListFn:
		arcpy.ExportXYv_stats("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct00_dis.shp","uid;geoid;ct2000area;newarea","COMMA","V:/GIS/projects/naas/tasks/201502_naas_locations/data/tables/census/"+i+j+"_land_int_ct00_dis.csv","ADD_FIELD_NAMES")
		arcpy.ExportXYv_stats("V:/GIS/projects/naas/tasks/201502_naas_locations/data/processing/census/"+i+j+"_land_int_ct10_dis.shp","uid;geoid;ct2010area;newarea","COMMA","V:/GIS/projects/naas/tasks/201502_naas_locations/data/tables/census/"+i+j+"_land_int_ct10_dis.csv","ADD_FIELD_NAMES")
