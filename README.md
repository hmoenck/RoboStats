# RoboStats

### Imports: 

    PyQt5
    sip
    pandas
    numpy
    matplotlib 
    seaborn
    json
    datetime
    os, sys
    
### Start via: 
    python3 mainWindow.py

### Input: 
    - csv File containing (at least) columns for: Frame index, Timestamp (ms, s, or datetime), x-position, y-position, angle (in deg or    rad) for each agent
    - possible problems: headers or commented lines may cause problems. In that case try again with a file that contains only data.
    
### Procedure: 
    - Click 'Browse' to select a file for file selection (any filetype other than csv wil cause error)
    - Adjust settings of the chosen file (deliminator, skiplines)
    - Click 'Load' to open a Table view of selected data
    
    
### Outputs: 
