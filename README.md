## IntercomDinnerParty

### The Problem
We have some customer records in a text file (customers.txt) -- one customer per line, JSON lines formatted.
We want to invite any customer within 100km of our Dublin office for some food and drinks on us. 
Write a program that will read the full list of customers and output the names and user ids of matching customers (within 100km), sorted by User ID (ascending).

### The Solution
I have built a configurable solution. Here by simply changing the values in the [config.json](link) file, we can modify the behaviour of the code.
Instead of hard-coding the parameters, the `main.py` script initializes the `Invite` object with instance attributes from the config file and the `Invite` object takes it from there.

This structure be amazingly helpful, flexible and extensible if we need to run multiple programs.
For example, we can configure two programs, one where we invite customers within 100km and the other where we invite a different set of customers within a distance of 50km.  

#### Project Structure Overview
##### Root
In the root of the project there are the following files
* [main.py](link) - This is the main python script used to run the program.
* [customer.py](link) - This file contains the customer model.
* [invite.py](link) - This file contains a class called Invite which contains the bulk of running knowledge.
* [readers.py](link) - This file contains the Reader interface and implementations: HttpReader and FileReader. 
* [utils.py](link) - This file contains utility functions Eg: writing to file, calculating distance. 
* [config.json](link) - This is the configuration file. It contains properties of the invite class like the intercom coordinates, distance threshold and i/o file paths.

##### Test
The test folder contains python scripts performing tests on the various components of the program.
<br>`unittest` has been used to perform these tests.    

##### Resources
This folder contains the input file [customers.txt](link) along with some files for the tests and output files.

##### Output File
We can find the output file [inviteList.txt](link) in the `resources/out` folder. 

#### Software and requirements
This problem has been solved using the language Python. If you are using a Mac or Linux, it should already be 
pre-installed. You can check this by entering:

```
python --version
```

on the command line. This code was written using Python 3, so please make sure the version runnning on your computer is 
3 or above if you intend to test it. There is a good article [here](https://wsvincent.com/install-python3-mac/) on how
to do so. 

There are no additional packages required to run this script. 

#### Running the code
To run the program :
```shell script
python main.py config.json
```

#### Running the tests
To run tests on the program:
```shell script
python -m unittest discover test
```