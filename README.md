# Automating Parcel Plotting in ArcGIS Pro with Python Using 'arcpy' Library

Description: This project automates the plotting of parcels on a 2D map in ArcGIS Pro using a Python script. The script reads a TXT file containing coordinates in degrees, minutes, seconds, directions (N/S/E/W), and distances. It then converts the coordinates to XY points and uses the arcpy library to access the Traverse Tool and automatically plot each point on the map as polygons.

Who is it for? This project was made for the GIS team during my internship with the Harris County Engineering Department as a geospatial software development intern

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

## Used By

This project is used by the following company:

- Office of the County Engineer
  
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

```bash
pip install numpy matplotlib pandas
  

 
