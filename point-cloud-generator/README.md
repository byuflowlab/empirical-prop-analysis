# PropellerPointCloudGenerator

This code is designed to take in an xy coordinate of an airfoil, then generate propeller blades based on chord, thickness, pitch functions
It adds a simple hub and exports, I used meshlab to generate a mesh from the point cloud and export a STL for 3D printing.  

The code takes the original airfoil and rotates and scales it, then adds z values for an offset, then repeats until it populates the entire
blade with profiles.  To do a point cloud, I made the profiles close enough for the mesh to work.  You can save out individual files of each profile
