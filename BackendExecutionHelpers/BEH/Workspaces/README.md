
# Data Manager

This module is intended to manage data-related things running in the compute environment including:
- namespacing data after it's been loaded
- ontology and schema management
- data dictionaries

and is a common interface for data that's been loaded into Python's memory in this kernel. 
ETL should push here, Pipelines should read and write from here. 
This could be implemented entirely in Python or backed by something like Redis. 

I suppose the DataManager should also interface to databases, but primarily databases owned by this project. 

How to interface with databases and sources NOT owned by this project is I suppose a more complicated question. Would this fall under ETL? or external connections? Don't necessarily want to make a copy of it all into our own databases. 

## Thin Vertical Slices:
Todo:
- be able to easily read and write data from pipeline transformations
- how can we encourage workflows that don't modify data in-place that's in the data manager?
  - impossible to enforce if they want to hack it but have smart defaults! like when reading we can return copies rather than the original?
  - probably still need to turn this off for large large datasets, but I think most cases within our target audience won't care about having multiple copies of a dataframe in memory?
  - actually, if the data is large enough that we can't freely duplicate it then we need to move their workflows to something like Presto, Elasticsearch, or real database operations

- we need persistant workspaces!
  - back data by Redis
  - back data by PostgreSQL
  - back data by Parquet
  - back data by Pickle

Done:





