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
    - csv File containing (at least) columns for: 
    Frame index, Timestamp (ms, s, or datetime), x-position, y-position, angle (deg/rad) for each agent
    - possible problems: headers or commented lines may cause problems. In that case try again with a file that contains only data.
    
### Procedure: 

    ----- > see also: HowTo.pdf (detailed description of procedure with screenshots)

    #### Before loading data: 
    
    - Click 'Browse' to select a file for file selection (any filetype other than csv wil cause error)
    - Adjust settings of the chosen file (deliminator, skiplines)
    - Click 'Load' to open a Table view of selected data
    
    #### In Table Window: 
    
    - Match each variable with the corresponding column in the original file, settings will be saved for later user
        -- minimum number of variables: 5, i.e. columns for frame number, time, agents x and y position and angle
    
    - 'Add/Remove Agents'-Button: opens a subwindow where you can change the number of agents and give them individual names
    - 'Add Parameters'-Button: opens a subwindow where you can set the time format (s, ms or datetime), the angle format (deg, rad)
       and add additional Categorie such as RoboMode and Region (not yet used for statistics)
       
    #### After loading data: 
    
    - after leaving the Table View the data in from the selected columns are used to display start and stop time as well as the min and max values of position. Both time and space boundaries can be adjusted via the respective 'Change'- Buttons and analysis will only be performed for the selected range. 
    
    - to eliminate measurement errors the trajectory can be smoothed, with a selected fileter (currently only median filter with k = 5) and the filter is applied via the 'Apply Smoothing Button'
    
    - clicking the 'Plot' Button will plot the trajectory and a black rectangle indicating the selected borders. The plot can be manipulated and saved via matplotlibs navigation toolbar. 
    
    - clicking the stats and save button will create a folder labelled with the current day's date within which folders are created every time the application is called (labelled 000, 001, 002, etc). This subfolder contains 2 csv files descirbed below. In the future it will also contain any plots created during the analysis. 
    
    
### Outputs: 
    1. timelines.csv with columns: 

	frames, 
	time (in selected format), 
	distance between pairs of agents 
	for each agent: 
		x-position, 
		y-position, 
		angle, 
		x-velocity, 
		y-velocity, 
		absolute speed 
		
		
    2. info.csv
    
    -source: original datafile
    -x_min: selected border value
    -x_max: selected border value
    -y_min: selected border value
    -y_max: selected border value
    -Start: selected start time
    -Stop: selected stop time
    -Filtered: true or false dependeing on wheter or not smoothing was applied 

    For each agent:
	    -trajectory_length: total lengh of agents trajectory
	    -mean_speed
	    -var_speed
	    -min_speed
	    -25%_speed: i.e 25 percentile
	    -median_speed
	    -75%_speed
	    -max_speed
	    
    For each pair of agents: 
	    -mean_dist
	    -var_dist
	    -min_dist
	    -25%_dist
	    -median_dist
	    -75%_dist
	    -max_dist


	
