import arcpy
import building_heights as bh

# Aquire Licenses
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

dir_path = r'C:\Users\brownr\Desktop\bh\bh_data'
delta = r'\\metanoia\geodata\PW\sw_tech\Charlottesville_Lidar\DEM\delta_sp_f'
prj = r'\\metanoia\geodata\PW\sw_tech\Coordinate_Systems\NAD 1983 StatePlane Virginia South FIPS 4502 (US Feet).prj'    
struc = r'Database Connections\Connection to GISPRDDB direct connect.sde\cvgis.CITY.Buildings\cvgis.CITY.structure_existing_area'

#Create gdb to hold data
gdb = dir_path + r'\Building_Heights.gdb'
arcpy.CreateFileGDB_management(dir_path, 'Building_Heights.gdb')
#Set gdb as workspace
arcpy.env.workspace = gdb

#Create random points layer
bh.random_points(struc, 'random_points')
#Add elevation data to random points layer
bh.elevation_data('random_points', delta)
#Interset random_points layer with footprints 
bh.footprint_elevation('structure', 'random_points', 
  gdb, 'BIN')


# Returns licenses
arcpy.CheckInExtension('Spatial')
arcpy.CheckInExtension('3D')    