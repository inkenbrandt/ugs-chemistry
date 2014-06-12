# installing [oracle client](http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html)

1. [Instant Client Package](http://download.oracle.com/otn/nt/instantclient/121010/instantclient-basic-windows.x64-12.1.0.1.0.zip)
1. Create a folder on disk and extract to that location
1. Add location to windows path
1. Install [cx_Oracle](https://pypi.python.org/pypi/cx_Oracle/5.1.3)

this package will take ugs csv data and import it into a gdb.  

`dbseeder.py --seed` will create the **gdb**, the **stations** point feature class and the **results** table.

The seed will look for `data\Results` and `data\Stations` and import all the child *.csv's. 

Once that is done you can create the relationship feature class by running

`dbseeder --relate`

`dbseeder --update` is still a work in progress but all the plumbing is there. We just need to figure out how to get the query to the program and what that query should be.

## Tests

`setup.py test`

To run specific tests cd to the `scripts` folder and run 
`nosetests dbseeder.tests.file:class.testname

## Installation

`setup.py install`