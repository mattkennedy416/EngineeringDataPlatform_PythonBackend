
# Extract-Transform-Load

ETL should focus on external connections and sources, whether that's getting data from the local system, other services, or remote servers. Get it connected and accessible to pipelines in a relatively nice and consistent format. 


## Architecture

So back to the issue that ETL needs to run in a separate kernel in a separate thread, and should NOT be running in the main thread. 
This also actually solves the problem of processing limitations of polling too many ETL operations from a single thread slowing everything down. 

I think we have two main use-cases here that need to easily translate back and forth:
- **dev/test:** few-shot ETL into my current execution environment
- **prod:** continuous ETL into database infrastructure

and by translate back and forth, I mean the user needs to be able to select a **dev/test** ETL and "push to production",
likewise take a continuous production ETL and load some samples into my current environment. 

### ETL Manager
The concept of an ETL manager will help us translate the same operations back and forth between dev/test and production environments. 
It will also help define and execute repeating operations over time. 

The ETL Manager class shall wrap around and execute ETL Item objects that
define individual operations. 


## Thin Vertical Slices:
Todo:
- create an ETL action to continuously poll a folder for new CSVs to load
- multi-threaded ETL? I suppose have one kernel initially parse, pass instructions back to the main thread which then disperses to multiple kernels to load simulataneously?


Done:
- load a CSV from local disk, using some kind of endpoint that defines a new ETL action
- create an ETL action to load a small sample of CSVs from a folder of many CSVs
- 



