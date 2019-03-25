# piedpiper-pycoverage-faas

Getting Started
----------------
First download and install the following:
```
Docker
Flask
Open-FAAS
```

PyCoverage FAAS 
----------------
To run open a new terminal window and cd into the PyCoverage FAAS folder

Run the following commands:
```
  sudo faas build
  faas deploy
```

Now the service is running. You can verify by running the command **- docker ps**.
Additionally to verify the coverage tool is running, one can run the following command:
```
  curl -F 'files=@TEST.zip' http://172.17.0.1:8080/function/piedpiper-pycoverage-function
```

Configuration
---------------
PyCoverage FAAS is a dockerized container of the PyTest and Coverage tools for test coverage analysis of python code. There are two files of interest for configuring the tool; *setup.cfg* and *.coveragerc*. 

Setup.cfg tells the tools which package to analyze by specifying the package name after the command line switch **--cov=**

The .coveragerc file is the configuration file used by coverage.py. Most options are shown and documented in the test.zip, however for full documentation reference the website https://coverage.readthedocs.io/en/latest/config.html

