#uploading necessary libraries
import math as mt
import numpy as np
import re
import arcpy
from datetime import datetime

# Loading data from text file
txt_file = r"C:\Users\alexis.graciarodrigu\Desktop\Yenis Project\Parcel Documents\TXT Files ready\FILE NAME.txt"

# Read the file and split into words
try:
    with open(txt_file, 'r', encoding='utf-8') as file:
        text = file.read()
except:
    print("Failed to read with UTF-8, trying Latin1...")
    with open(txt_file, 'r', encoding='latin1') as file:
        text = file.read()

content = text.split()

# Initial coordinates
x = '3,167,783.51'
y = '13,876,355.85'

#removing the commasnd turning it into a float
start_x = float(x.replace(",", ""))
start_y = float(y.replace(",", ""))

#initializing empty variables
degrees = []
minutes = []
seconds = []
distances = []
directions = []
arc_length = []
DMS_degrees_curves = []
DMS_minutes_curves = []
DMS_seconds_curves = []

#Extracting degrees, minutes, seconds from content(txt_file splitted)
for i in range(len(content)):
     # Skip if the current entry is preceded by "delta angle of"
    if 'delta' in content[i-4:i] and 'angle' in content[i-4:i]:
        print(f"Skipping entry: {content[i]} because of 'delta angle of'")
        continue  # Skip further processing for this entry

    
    # Check if the current word contains a full degrees, minutes, and seconds format
    match_full = re.findall(r'(\d+)°(\d+)\'(\d+)"', content[i])
    if match_full:
        # If the full match is found, skip further degrees/minutes/seconds checks for this entry
        for degree, minute, second in match_full:
            degrees.append(float(degree))
            minutes.append(float(minute))
            seconds.append(float(second))
        continue  # Skip further checks for this entry since we already extracted the full set
    
    # Check if the current word indicates degrees in different formats
    if content[i] in ['degrees', 'deg.', 'DEG.', 'DEG .', 'DEG'] and content[i-4] != 'delta' and content[i-3] != 'angle':
        if content[i - 2] in ['South', 'south', 'SOUTH', 'North', 'north', 'NORTH', 'N', 'S']:
            # Look at the previous word (if available) for the number
            if i > 0:
                degrees_value = re.sub(r'\D', '', content[i - 1])  # Remove non-digit characters
                if degrees_value:  # Check if the result is not empty
                    degrees.append(float(degrees_value))
    
    # Check if the current word contains a number with the degree symbol
    match_degrees = re.findall(r'(\d+)°', content[i])
    if match_degrees and content[i - 1] in ['South', 'south', 'SOUTH', 'North', 'north', 'NORTH','N', 'S']:
        degrees.extend([float(m) for m in match_degrees])
    
    # Check if the current word contains a number with the minute symbol
    match_minutes = re.findall(r'(\d+)\'', content[i])
    if match_minutes and content[i - 2] in ['South', 'south', 'SOUTH', 'North', 'north', 'NORTH', 'N', 'S']:
        minutes.extend([float(m) for m in match_minutes])

    # Check if the current word contains a number with the second symbol
    match_seconds = re.findall(r'(\d+)"', content[i])               #defines the number next to '
    minutes_value_checking = re.findall(r'(\d+)\'', content[i-1])   #defines the number next to "
    match_degrees = re.findall(r'(\d+)°', content[i-2])             #defines the number next to °
    if minutes_value_checking and match_degrees and content[i + 1] in ['West', 'west', 'WEST','West,', 'East', 'east', 'EAST', 'East,', 'W', 'E']:                    #if statements checks that the seconds extracted is next to minutes and degrees             
        # print(content[i])
        seconds.extend([float(m) for m in match_seconds])

    # Alternatively, handle variations for minutes
    elif content[i] in ['minutes', 'min', 'mn', 'MIN.', 'mn.', 'min.'] and content[i-6] != 'delta' and content[i-5] != 'angle':
        if i > 0:
            minutes_value = re.sub(r'\D', '', content[i - 1])  # Remove non-digit characters
            if minutes_value:
                minutes.append(float(minutes_value))

    # Alternatively, handle variations for seconds
    elif content[i] in ['seconds', 'sec.', 'SEC.', 'seconds,'] and content[i-8] != 'delta' and content[i-7] != 'angle':
        if i > 0:
            seconds_value = re.sub(r'\D', '', content[i - 1])  # Remove non-digit characters
            if seconds_value:
                seconds.append(float(seconds_value))


#Extracting the distances that correspond to each coordinate
for i in range(len(content)):
    if content[i] in ['distance', 'DISTANCE', 'line,', 'Line,', 'Line', 'Lot', 'lot', 'right-of-way', 'Lots', 'Road,', 'Easement,']:
        
        # first if statement is for distances on files where the word distance is not specified
        if i + 2 < len(content):
            if content[i] in ['Line,', 'line,', 'Line', 'Road,', 'Easement,']:
                # print(content[i+2])
                distance_str = content[i + 1]
                # print(distance_str)
                # print(i)
                try:
                    distances.append(float(distance_str))
                except ValueError:
                    pass #Ignore if conversion fails
            elif content[i] in ['Lot', 'lot']:
                distance_str = content[i+2]
                # print(distance_str)
                # print(i)
                try:
                    distances.append(float(distance_str))
                    # print(distance_str)
                    # print(i)
                except ValueError:
                    pass #Ignore if conversion fails
            
            elif content[i] in ['Lots']:

                distance_str = content[i+4]
                # print(distance_str)
                # print(i)
                try:
                    distances.append(float(distance_str))
                    # print(distance_str)
                    # print(i)
                except ValueError:
                    pass #Ignore if conversion fails

            elif content[i] in ['right-of-way']:
                # print(content[i+7])
                distance_str = content[i+7]
                try:
                    distances.append(float(distance_str))
                except ValueError:
                    pass #Ignore if conversion fails

            elif content[i] in ['distance', 'DISTANCE']:
                distance_str = content[i + 2]
                distance_str = distance_str.replace(',','')
                try:   
                     distances.append(float(distance_str))
                      # print(distance_str)
                except ValueError:
                     pass  # Ignore if conversion fails

    elif content[i] in ['-', 'WEST-', 'West', 'EAST-', 'West,', 'East,', 'East']:   
        if i + 1 < len(content):
            if content[i] == ['-'] and content[i-1] != ['West', 'WEST', 'West,', 'East','EAST', 'East,', 'W', 'E']:
                pass
            elif content[i] == '-' and content[i-1] in ['WEST-', 'EAST-', 'West,', 'East,', 'East', 'WEST', 'West', 'W', 'E']:
                distance_str = content[i + 1].strip(' feet;')  # Clean up the string
                try:
                    distances.append(float(distance_str))
                except ValueError:
                    pass  # Ignore if conversion fails
            elif  content[i] in ['West', 'WEST', 'West,', 'East','EAST', 'East,', 'WEST-']:
                distance_str = content[i + 1].strip(' feet;')  # Clean up the string
                try:
                    distances.append(float(distance_str))
                except ValueError:
                    pass  # Ignore if conversion fails


#Checks to confirm it did not repeated a distances based on file txt format
for i in range(len(distances)):
    if len(distances) > len(degrees) and i >= 1:
        print('A consecutive repeated value has been removed from the list of distances')
        print('The extra value does not correspond to any DMS and has been mentioned to verbally describe a direction')
        if distances[i] == distances[i-1]:
            distances.remove(distances[i])

#Extracting the directions
for i in range(len(content)):
    if content[i] in ['North', 'NORTH', '.North', '.NORTH', 'N']:
        # Look ahead at the next word(s) for the number (degree) and handle both cases
        next_word = content[i + 1] if i + 1 < len(content) else ""

        # Case 1: The degree symbol is present (e.g., "87°")
        match_degrees_symbol = re.findall(r'(\d+)', next_word)

        # Case 2: The word "degrees" is explicitly mentioned after the number (e.g., "87 degrees")
        match_degrees_word = re.findall(r'(\d+)', content[i + 1]) if (i + 2 < len(content) and content[i + 2] in ['degrees', 'deg.', 'DEG.', 'DEG .']) else []
        # Check if either the degree symbol or the word "degrees" was found
        if match_degrees_symbol or match_degrees_word:
            degree_value = match_degrees_symbol[0] if match_degrees_symbol else match_degrees_word[0]
            directions.append('n')  # Append the direction 'n' for North
        # print(content[i])

    elif content[i] in ['South', 'SOUTH', 'South', '.South', '.SOUTH', 'S']:
        # Look ahead at the next word(s) for the number (degree) and handle both cases
        next_word = content[i + 1] if i + 1 < len(content) else ""
        # Case 1: The degree symbol is present (e.g., "87°")
        match_degrees_symbol = re.findall(r'(\d+)', next_word)
        # Case 2: The word "degrees" is explicitly mentioned after the number (e.g., "87 degrees")
        match_degrees_word = re.findall(r'(\d+)', content[i + 1]) if (i + 2 < len(content) and content[i + 2] in ['degrees', 'deg.', 'DEG.', 'DEG .']) else []
        
        # Check if either the degree symbol or the word "degrees" was found
        if match_degrees_symbol or match_degrees_word:
            degree_value = match_degrees_symbol[0] if match_degrees_symbol else match_degrees_word[0]
            directions.append('s')  # Append the direction 'n' for North
        # print(content[i])

    elif content[i] in ['East', 'EAST-',  'East,', 'EAST,', 'East.', 'E']:
    
        previous_word = content[i-1] if i - 1 >= 0 else ""
        #case 1: The seconds symbol is present ( e.g., "87' ")
        match_seconds_symbol = re.findall(r'(\d+)"', previous_word)
        # case 2: "seconds" is explicitly mentioned before the number (e.g., " 87 seconds")
        match_seconds_word = re.findall(r'(\d+)', content[i-2]) if (i-2 >= 0 and content[i-1] in ['seconds', 'sec.', 'SEC.', 'seconds,']) else []
        
        #chekc if either the seconds symbol or the word "seconds" was found
        if match_seconds_symbol or match_seconds_word:
            seconds_value = match_seconds_symbol[0] if match_seconds_symbol else match_seconds_word[0]
            directions.append('e')


    elif content[i] in ['West', 'WEST-',  'West,', 'WEST,', 'WEST', 'West.', 'W']:
        previous_word = content[i-1] if i - 1 >= 0 else ""
        #case 1: The seconds symbol is present ( e.g., "87' ")
        match_seconds_symbol = re.findall(r'(\d+)"', previous_word)
        # case 2: "seconds" is explicitly mentioned before the number (e.g., " 87 seconds")
        match_seconds_word = re.findall(r'(\d+)', content[i-2]) if (i-2 >= 0 and content[i-1] in ['seconds', 'sec.', 'SEC.', 'seconds,']) else []
        
        #chekc if either the seconds symbol or the word "seconds" was found
        if match_seconds_symbol or match_seconds_word:
            seconds_value = match_seconds_symbol[0] if match_seconds_symbol else match_seconds_word[0]
            directions.append('w')


#Extracts arc length for curves when included
for i in range(len(content)):
    if content[i] in ['arc']:
        if content[i+1] in ['length']:
            arc_length_str = content[i+3]
            try:
                arc_length.append(float(arc_length_str))
            except ValueError:
                pass #If conversion fails, skip
    elif content[i] in ['radius']:
        arc_length_str = content[i+2]
        try:
            arc_length.append(float(arc_length_str))
        except ValueError:
            pass #skip if conversion fails


#Extracts the degrees, minutes, seconds for the curves
#Additional Note: This part is not being used by the code but it will be used once curves are incorporated into the process
for i in range(len(content)):
    #case 1: curve angles are mentioned as delta angles
    if content[i] == 'delta' and content[i+1] == 'angle':
        DMS_degrees_str = content[i+3]
        DMS_minutes_str = content[i+5]
        DMS_seconds_str = content[i+7]
        try:
            DMS_degrees_curves.append(float(DMS_degrees_str))
            DMS_minutes_curves.append(float(DMS_minutes_str))
            DMS_seconds_curves.append(float(DMS_seconds_str))
        except ValueError:
            pass   #If conversion fails, skip

    #case 2: curve angles are mentioned as central angles
    elif content[i] == 'central' and content[i+1] == 'angle':
        # Check if the current word contains a number with the degree symbol
        DMS_degrees_str = re.findall(r'(\d+)°', content[i+3])
        if DMS_degrees_str:
            DMS_degrees_curves.extend([float(m) for m in DMS_degrees_str])
        DMS_minutes_str = re.findall(r'(\d+)\'', content[i+4])  #removes the minutes symbol next to the number
        if DMS_minutes_str:
            DMS_minutes_curves.extend([float(m) for m in DMS_minutes_str])
        DMS_seconds_str = re.findall(r'(\d+)",', content[i+5])  #removes the seconds symbol next to the number
        if DMS_seconds_str:
            DMS_seconds_curves.extend([float(m) for m in DMS_seconds_str])  #appropiately adds it to the variable since append does not work due to its format

degrees_size = len(degrees) 
minutes_size = len(minutes)
seconds_size = len(seconds) 
directions_size = len(directions)//2
distance_size = len(distances)

#if statements to check if it extracted degrees and minutes correctly 
if degrees_size != minutes_size or degrees_size != seconds_size or degrees_size != distance_size or degrees_size!= directions_size:
    print('PROBLEM in the extraction of degrees,minutes,seconds,distances,directions')
    print(" ")
    print('Hint: All lengths should be the same. The problem is in the variable with different length')
    print('degrees length = ', degrees_size)
    print('minutes length = ', minutes_size)
    print('seconds length = ', seconds_size)
    print('distances length = ', distance_size)
    print('directions length =', directions_size)
    
# Check the extracted values
print(' ')
print("Degrees:", degrees)
print("Minutes:", minutes)
print("Seconds:", seconds)
print("Distances:", distances)
print("Directions:", directions)
print('Arc lenght:', arc_length)
print('Delta angle:', DMS_degrees_curves)
print('Delta minutes:', DMS_minutes_curves)
print('Delta seconds', DMS_seconds_curves)

#separating directions for latitude and longitude to be use for bearing DMS to decimal degrees
direction_latitude = []
direction_longitude = []


for i in range(len(directions)):
    if i % 2 == 0:
        direction_latitude.append(directions[i])
    else:
        direction_longitude.append(directions[i])

# converting from bearing DMS to decimal degrees
def calculate_bearing_angle(degrees, minutes, seconds, direction_latitude, direction_longitude):
    # Convert DMS to decimal degrees
    dd = degrees + (minutes / 60) + (seconds / 3600)

    # Determine the bearing angle based on quadrant
    if direction_latitude.lower() == 'n' and direction_longitude.lower() == 'e':
        # North-East quadrant
        bearing_angle = dd
    elif direction_latitude.lower() == 's' and direction_longitude.lower() == 'e':
        # South-East quadrant
        bearing_angle = 180 - dd
    elif direction_latitude.lower() == 's' and direction_longitude.lower() == 'w':
        # South-West quadrant
        bearing_angle = dd + 180
    elif direction_latitude.lower() == 'n' and direction_longitude.lower() == 'w':
        # North-West quadrant
        bearing_angle = 360 - dd

    return bearing_angle


bearing_angle = []
for i in range(len(degrees)):
    bearing = calculate_bearing_angle(degrees[i], minutes[i], seconds[i], direction_latitude[i], direction_longitude[i])
    bearing_angle.append(bearing)

# Finding the new x,y coordinates
def cartesian_converter (bearing_angle, distance):
    angle = (90-bearing_angle)*(mt.pi/180)
    x = distance*mt.cos(angle)
    y = distance*mt.sin(angle)

    return x,y


X = [start_x]
Y = [start_y]
# Accumulate coordinates correctly
for i in range(len(bearing_angle)):
    x_offset, y_offset = cartesian_converter(bearing_angle[i], distances[i])
    new_x = X[-1] + x_offset
    new_y = Y[-1] + y_offset
    X.append(new_x)
    Y.append(new_y)

coordinates = list(zip(X, Y))
print(coordinates)

# Path to geodatabase and feature class
output_gdb = r'C:\Users\ALEXIS.GRACIARODRIGU\Desktop\HCPropertyInventory_Pro.gdb'

# Set spatial reference
spatial_ref = arcpy.SpatialReference(2278)

# Set the workspace
arcpy.env.workspace = r'C:\Users\ALEXIS.GRACIARODRIGU\Desktop\SQLServer-svpitcgisdb01-HCPID_GDB(PID).sde'

# Define the full path to the feature class
# Use double backslashes or raw string format to avoid issues with escape characters
fc = r'\\fs.hc.hctx.net\Shares\ENG\EES and Organizational Effectiveness\GIS Group\7. Other Folders\GIS_Data\ProjectData\RightofWay\RPD Deed Emails\HCPropertyInventory_Pro\PID.sde\HCPID_GDB.PID.Land\HCPID_GDB.PID.RPD_HCOwnedProperty'


# Start an edit session
edit = arcpy.da.Editor(arcpy.env.workspace)

# Define a polygon using the points (make sure the first and last points are the same to close the polygon)
polygon_points = coordinates + [coordinates[0]]  # Closing the loop

try:
    # Start the edit operation
    edit.startEditing(False, True)  # (no undo, allow edits on the layer)

    # Start an edit operation
    edit.startOperation()

    # Define a polygon using the points (make sure the first and last points are the same to close the polygon)
    polygon_points = coordinates + [coordinates[0]]  # Closing the loop

    # Insert the polygon into the feature class (HCPID_GDB.PID.RPD.HCOwnedProperty)
    with arcpy.da.InsertCursor(fc, ['SHAPE@']) as cursor:
        array = arcpy.Array([arcpy.Point(x, y) for x, y in polygon_points])
        polygon = arcpy.Polygon(array, spatial_ref)
        cursor.insertRow([polygon])
    
    print("Parcel drawn successfully.")

    # Complete the edit operation (Locks the file again once the parcel has been plotted)
    edit.stopOperation()
#     edit.stopEditing(True)  # Save changes
except Exception as e:
    print(f"Error occurred: {e}")
    # If an error occurs, abort the edit operation
    edit.abortOperation()
finally:
#     # Stop editing session
    edit.stopEditing(True)  # Save changes
