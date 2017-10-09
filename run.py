import arcpy
import building_heights as bh

# Aquire Licenses
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

dir_path = r'C:\Users\brownr\Desktop\bh\bh_data'
delta = r'\\metanoia\geodata\PW\sw_tech\Charlottesville_Lidar\DEM\delta_sp_f'
prj = r'\\metanoia\geodata\PW\sw_tech\Coordinate_Systems\NAD 1983 StatePlane Virginia South FIPS 4502 (US Feet).prj'    
struc = r'Database Connections\Connection to GISPRDDB direct connect.sde\cvgis.CITY.Buildings\cvgis.CITY.structure_existing_area'

#bh.random_points(struc, dir_path)
#bh.elevation_data(dir_path + r'\Ran_Points.shp', delta)
bh.footprint_elevation(dir_path + r'\temp.shp', dir_path + r'Ran_Points', 
  dir_path, 'BIN')