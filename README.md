**Asana Time Export Script**

This script uses the Asana API in order to find and return time entry data from within a set time period. The default setting is for one month, but this can be adjusted as required.

Unfortunately Asana doesn't offer an endpoint for time entry data, so this is a workaround until they do.

It's highly specific to the organisation I work for, which is why there are a number of custom fields that are being pulled.

The steps it follows are:

1. Load workspace and personal access token from a config.json file on a local machine
2. Fetch all live projects
3. Create a list of project identifiers
4. Loop through the projects and use the /tasks (get multiple tasks) endpoint to get all the tasks updated in the last month
5. Filter those tasks to those which actually have time on them
6. Loop through the resulting list of tasks and query the time entries for those
7. Filter out the time entries that aren’t in the last month

Next I'll be adding export functionality, either to a CSV or to an SQL database. 
