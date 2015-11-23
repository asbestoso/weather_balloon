# weather balloon

These scripts emulate gathering and processing metrics from a weather balloon.
Raw log data is assumed to be collected in plaintext on the filesystem. Running *consumer.py* to normalize the data and store it on the filesytem in a sqlite datafile. *print_data.py* and *query_metrics.py* can be used to retrieve information from the datafile. 

**Generate fake data**
- run fake_data.py with *output path* and *number of lines to generate* as arguments, eg:

  ```./fake_data.py data.log 50000```


**Import data**
- run consumer.py with *input path*, *datastore path* as arguments, eg:

  ```./consumer.py data.log data.db```
  
**Print data**
- run print_data.py with *datafile*, *temperature output unit* and *distance output unit* as arguments, eg:

  ```./print_data.py data.db C M```
  - available temperture units 'C', 'F', or 'K'; (celsius, fahrenheit, and kelvin)
  - available distance units 'M', 'KM', or 'Mi'; (meter, kilometer, mile)
  - outputs to console, use pipe to write to file

**Query metrics**
- run query.py with [options] and *datafile*. Use the -h option for details. eg:

  ```./query.py --distance --mean --observations --max --min data.db```
  
  
*Didn't get a chance to implement random inconsistencies to the fake log generator, added the original idea as a comment in the file.

*Assumes we are only reading from the log once, the consumer drops the table each time it runs. Could easily make it append new data; wasn't done because I was originally to precompute the query options [in this commit](https://github.com/asbestoso/weather_balloon/commit/ca729ba09678d726cf8c71b977308bac80eff54f), but ultimately decided against it and didn't get around to updating the consumer.

*Ideally, all the sqlite interfacing code should live in its own module and exposed as a service so it can be easily swapped out for a timeseries database like whisper or a non-relational one like cassandra; depending on the kind of use cases might have for this data. As it is, the code is very tightly coupled to the sqlite db.  
