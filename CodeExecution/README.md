
# Code Execution

Manage our environments for actually executing code. For most cases (initially) code will be executed in short-lived IPython Kernals in separate process from this backend process. 

**Note to devs:** this python backend service is more of a *manager*, if we're making specialty wrapper classes or functionality we'll need to get those compiled and imported into the IPython execution environments. 

Though by default the ipython kernels seem to start using the same python interpreter or venv / conda env that this backend service is running. 

## Thin Vertical Slices:
- import common but non-default libraries (eg Pandas) into our IPython execution environment
- import custom libraries (eg ETL) into our IPyhton execution environment
- Execute a SQL statement against a database table
- Execute a SQL statement against an in-memory dataframe/table?
- Namespaces / Workspaces, multiple interpreters open at once
- Save the state of a workspace and recreate it at next startup
  - variables only?
  - defined functions too?





