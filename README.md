# Java-Compiler
This is a simple demonstration of how to make a language compiler using Python's [PLY module](https://ply.readthedocs.io/en/latest/).
The project implements a lexer, parser and interpreter for Java.

## Installation
To install locally, do the following:

1. Ensure that the following things have been installed:

    a. python (Installed based on your distro)

    b. pip (curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py)

    c. virtualenv

2. Open up a terminal.

3. Create a directory somewhere `mkdir java-compiler-env` and `cd` into it.

4. Create a python virtual environment `python -m virtualenv .`

5. Activate the virtual environment `source bin/activate`

6. Navigate to the project's root directory where `setup.py` file is located.

7. Do a ```pip install .``` 

## Java Console
Once the installation is complete, you can test the compiler by running the java console by running the command: `java-console`. Start creating variables and run arithematic commands.
## Functionalities Supported: 
* Variables:
	* Declaration, assignment, access
	* Types: int, double, char, strings, bool
	* Initialisation and declaration of a variable with the name of a pre existing variable would generate error
	* Types of the data and the variable should match while declaring or initialising

* Array:
	* Declaration, assignment, access
	* Types: int, double, char, strings, bool
	* Access outside the array-size would give an error

* Arithematic Expressions:
	* Operators: (+ , - , / , * , % , ++, --, nested parentheses)

* Standard Output:
	* System.out.print()
	* Any variable-type should be displayed

* Error Handling:
	* Mentions the reason for error

