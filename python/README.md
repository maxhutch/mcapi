API for MaterialsCommons.org
============================

This is the python version of an API to MaterialsCommons.org. 
The source code is available at 
https://github.com/materials-commons/mcapi/tree/master/python.

It consists of four packages/modules
* **mcapi** - the main interface to the API
* **mcapi.cli** - a command line interface (see scripts/mc)
* **casm_mcapi** - a special set of API extensions for its application
 in CASM, including a command line interface
* **demo_project** - a module for building a demo project in a designated 
 Materials Commons server, for a given user, using the API
 
In addition there is a distribution package (which includes 
the demo_project and mcapi moduels): **mcapi_dist**.

For testing: see test.RunTests.md