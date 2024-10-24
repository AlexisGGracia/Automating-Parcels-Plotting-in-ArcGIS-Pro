# Automating Parcel Plotting in ArcGIS Pro with Python Using 'arcpy' Library

# Introduction
This project automates the plotting of property parcels on a 2D map in ArcGIS Pro using a Python script, enabling the company and clients to visually analyze property boundaries more efficiently. The script reads a TXT file containing coordinates in degrees, minutes, seconds, directions (N/S/E/W), and distances. It then converts the coordinates to XY points and uses the arcpy library to access the Traverse Tool and automatically plot each point on the map as polygons.

Who is it for? This project was made for the GIS team during my internship with the Harris County Engineering Department as a geospatial software development intern

# Code Breakdown and Workflow

This section provides a detailed explanation of the logic and steps involved in the code.

1. **Read the input file, splitting the content into complete words**
    - The script starts by reading a `.txt` file that contains the information needed to draw the parcels.
    - The `.txt` files provide the coordinates in a specific format to generate a general pattern that allows the code to work for multiple files.
    - Example: 
        - North 26 degrees 25 minutes 30 seconds East, with a distance of 15.6 ft
        - South 26° 25' 30" West, with a distance of 15.6 ft
        - North 26°25'30" East - 15.6 ft

2. **Extract the information required such as degrees, minutes, seconds, distance, and directions from the `.txt` file.**

3. **Include an if statement that checks if there is any missing information in case the code failed to extract all the required information.**
    - In this section, it checks for the length of degrees, minutes, seconds, distance, and directions.
    - If the code successfully extracts all the information, it continues. Otherwise, it prompts a warning sign with hints to help debug the location of the problem.

4. **Convert the given coordinates and distances such as "North 26°25'30" East - 15.6 ft" to Cartesian XY points.**
    - To do so, we need to find the bearing angles to convert from polar coordinates to XY points.
    
    **Steps to convert from DMS to bearing angles:**
    ```python
    # Find the decimal degree
    decimal_degree = degrees + (minutes / 60) + (seconds / 3600)
    
    # Convert decimal degree to bearing angle:
    if directions are NE:
        bearing_angle = decimal_degrees
    if directions are SE:
        bearing_angle = 180 - decimal_degrees
    if directions are SW:
        bearing_angle = 180 + decimal_degrees
    if directions are NW:
        bearing_angle = 360 - decimal_degrees
    ```

5. **Convert from polar coordinates using the bearing angle to XY points:**

    **Steps:**
    ```python
    angle = 90 - bearing_angle
    X = distance * cos(angle)
    Y = distance * sin(angle)
    ```

6. **Pass the XY points to the `arcpy.da.InsertCursor` function to plot the XY points as polygons.**

    **Steps:**
    - Define a database.
    - Define a feature class (Example: `TraversedLines`).
    - Define a spatial reference (2278 corresponds to South Texas Central and should be changed based on the desired geographic location).
    - Define a polygon using the points (make sure the first and last points are the same to close the polygon).
    - Use `arcpy.da.InsertCursor` to access the traverse tool and insert the XY points for each row.

### Important Notes:
- Your starting point and your last point generated should be the same to close the polygon.
- Additionally, when computing your XY points, you need to use the previous point as your new starting point for the next XY points. Otherwise, your shape will be inaccurate.

  
## Requirements 
To run this project, you will need the following software and tools:

- **Python 3.x**: Ensure Python 3.x is installed. You can download it from [here](https://www.python.org/downloads/).
- **ArcGIS Pro**: You will need ArcGIS Pro to run the script and use its mapping features. You can get it from [ArcGIS Pro](https://www.esri.com/en-us/arcgis/products/arcgis-pro).
- **ArcPy**: This Python library is used for automating GIS workflows in ArcGIS Pro. It comes pre-installed with ArcGIS Pro.
- **Additional Python Libraries**:
  - `numpy`
  - `pandas`
  - `re`
  - `math`
  - `datetime`
  - `os`

You can install the Python libraries using `pip`:

`pip install numpy matplotlib pandas`
# Visual Results
In this section, I have included images that demonstrates the final product of my code. The green figures were made manually which takes about 2-5 minutes to generate. The figure with a distinct color was made using my code automatically which takes less than 3 seconds to generate.

## Green Color Figure: 
    Corresponds to a manually drawn parcel (2-5 minutes to generate)

## Distinct Color Figure: 
    Corresponds to the parcel generated by my code (less than 3 seconds to generate)

![SC1](https://github.com/user-attachments/assets/3c0bfd72-6d8e-4b8f-aa28-35aa16d593ab)
![SC2](https://github.com/user-attachments/assets/c3d17219-bb17-47b0-8314-94063c762bc5)
![SC3](https://github.com/user-attachments/assets/e114a0a3-1333-4b14-ac6f-54377539b38f)
![CS4](https://github.com/user-attachments/assets/2dfefa65-8b77-49a4-9336-92de5c340583)

## Project Usage

This project is used by the following company:

- **Office of the County Engineer**
    - GIS Team

## Contributor

This project was developed and maintained by:

- **Alexis Gracia**  
  [GitHub Profile](https://github.com/AlexisGGracia)  
  [Email](mailto:agg3455@my.utexas.edu)

