# dataplotter
This is a tool created for quickly and efficiently visualizing data from several different data files. It uses Python's Tkinter module for creating the GUI, and Numpy and Matplotlib modules to handle the data visualization. There is a powerpoint file that discusses how to install and use this tool in detail. 

NOTE: This tool was created for work, and the data is saved in a very specific format. Therefore, the code in this project is written specifically to be able to analyze these data files. 

# How to run locally
This project is meant to be distributed as a package. Therefore, there is a .tar.gz file that should be installed. First, download the .tar file, then open a command line prompt in that location and run the command "python -m pip install dataplotter-1.0.2.tar.gz". Running this command will install the dataplotter package and create a batch file that, when clicked, will automatically run the dataplotter module. Alternatively, the dataplotter module can be run by typing the command "python -m dataplotter" in the command line.

Another option to install the package locally is to clone the repo locally and run the `setup`:
  
  python setup.py install

