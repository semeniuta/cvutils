CVUtils - an OpenCV-based Python utilities library
==================================================

1. The basis computer vision-related functionality is implemented within the **cvfunctions** package. The package is divided into specific modules (calibration, chessboard, geometry, images, output, pyramid, stereovision, transform). It contain only functions and doesn’t rely on classes. This allow the package for potentially being used separately in other applications and being loosely-connected with the higher-level constructs.

2. Higher level functionality, related to specific problems, resides within the **cvapplications** package. The latter contain the modules such as calibration_experiment, confmanager, initenv, statsfuncs, svsparametrize, trueintrinsic, which are aimed at tackling the complex problems and being often reused.

3. The **cvclasses** package contains classes that are used by modules within **cvapplications** and some other simple scripts. The classes such as Camera, StereoVisionSystem and ImageSet simplify handling data related to singe camera (intrinsic parameters), stereo vision system (calibration parameters and rectification transforms) and image set respectively. Also, the classes are useful for serialization/deserialization of data and saving data in human-readable formats (e.g. Microsoft Excel).

4. The **generalfunctions** package is similar in its purpose to the cvfunctions, but encompasses general functionality (not related to computer vision), such as sampling, statistics and Excel files handling. 

5. “Scripts” are relatively simple python files that do not have a strict structure and are aimed at showing some practical aspects, testing the library’s functionality or exploring new features. By convention they have filenames in the form of script_*name*.py. Usually most of the functions within the library are decomposed from such scripts that were started out to explore some feature or implement some functionality from scratch in a single file.

6. “Applications” are the scripts designed to be called from the command line, and serve as user interface tools for the tasks within **cvapplications** package. The filename convention for applications is app_*name*.py.


