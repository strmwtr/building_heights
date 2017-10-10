import arcpy
import building_heights as bh

# Aquire Licenses
arcpy.CheckOutExtension('Spatial')
arcpy.CheckOutExtension('3D')

print '\n'
last_return = str(raw_input('File Path to last return raster: '))
print '\n'
ground_return = str(raw_input('File Path to ground return raster: '))
print '\n'
struc = str(raw_input('File Path to footprint data: '))
print '\n'
dir_path = str(raw_input('File Path to save output: '))
print '\n'
unique_id = str(raw_input('Unique ID field in footprint data: ')) 
print '\n'

def building_heights(last_return, ground_return, dir_path, struc, unique_id):
  '''Provide last_return and ground_return rasters, a directory to save 
  outputs, a footprint dataset, and the unique identifier in the footprint data
  '''
  print '-' * 8, ' Start ', '-' * 8
  #Create gdb to hold data
  gdb = dir_path + r'\Building_Heights.gdb'
  arcpy.CreateFileGDB_management(dir_path, 'Building_Heights.gdb')
  #Set gdb as workspace
  arcpy.env.workspace = gdb
  arcpy.env.overwriteOutput = True

  #Raster Processing 
  #Subtract ground raster from last return raster for delta raster
  bh.delta_raster(last_return, ground_return, dir_path)
  #Project delta raster to match footprint 
  bh.proj_rast(dir_path + r'\delta', dir_path, struc)
  #Fill projected delta raster
  bh.fill(dir_path + r'\delta_p', dir_path)

  #Vector Processing 
  #Copy footprints to new gdb
  arcpy.CopyFeatures_management(struc, 'footprint')
  #Create random points layer
  bh.random_points('footprint', gdb)
  #Add elevation data to random points layer
  bh.elevation_data('random_points', dir_path + r'\delta_raster')
  #Intersect random_points layer with footprints 
  bh.footprint_elevation('footprint', 'random_points', gdb, unique_id)
  #Join footprints to stats and create building_heights
  bh.create_building_heights_feature('footprint', 'stats', unique_id, 
    gdb)
  print '-' * 8, ' Done ', '-' * 9

#Call function
building_heights(last_return, ground_return, dir_path, struc, unique_id)

# Returns licenses
arcpy.CheckInExtension('Spatial')
arcpy.CheckInExtension('3D')    