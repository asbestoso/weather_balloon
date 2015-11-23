# weather

**Generate fake data**
- run fake_data.py with *output path* and *number of lines to generate* as arguments, eg:

  ```./fake_data.py out.log 50000```
- TODOs:
  - scramble the lines around and corrupt some data

**Import data**
- run consumer.py with *input path*, *datastore path* as arguments, eg:

  ```./consumer.py out.log weather.db```
  
**Print data**
- run print_data.py with *temperature output unit* and *distance output unit* as arguments, eg:

  ```./print_data.py C M```
  - available temperture units 'C', 'F', or 'K'; (celsius, fahrenheit, and kelvin)
  - available distance units 'M', 'KM', or 'Mi'; (meter, kilometer, mile)
  - outputs to console, use pipe to write to file

**Query metrics**
- TODO, ran out of time. Original unfinished implementations commented out. Will finish tomorrow.
  
