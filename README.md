# University-Transcripts
This repository contains a Python script to run a data analysis on the university transcript data contained in the /data folder. 

## Features

The transform_transcripts.py file contains the code. There are three global variables (DIRECTORY, COLUMNS and QUERIES) set at the top of the file. These define, respectively, the directory containing the data we'd like analysed, the columns we're interested in and the queries we'd like answered about the data. 

The script then creates an instance of the UniversityTranscriptsAnalysis class with the global variables as instance variables. This class has the methods necessary to run the analysis. In my approach I rely heavily on the modules pandas and pandasql. I use pandas to create a dataframe containing all the data from the directory and then answer the business questions by using pandasql to run sql queries over this dataframe.

The validate_input_files method runs some sanity checks on the files before adding them to the dataframe. It checks whether the file is in the correct format (.csv or .json) and whether the file is non-empty. The execute_queries function will catch SQL syntax errors, using a try-except and catching pandasql.PandaSQLException. 

The output of the script is two-fold - The dataframes resulting from the sql queries are printed in the command line and saved as csv with the business questions as their file names.

The transform_transcripts_test.py file contains the necessary unit tests, the fixtures folder contains files used in the unit tests and task_description.txt contains the task description. 

## Design Decisions

Using pandas and pandasql made it very easy to read the files and create something that we could run a query over. 

Setting the directory, columns and queries as global variables that are passed into the class allows some flexibility for future ad-hoc analysis. We will be able to write different businesss questions as SQL scripts for different datasets. All that's necessary is to amend the global variables at the top of the file.

## Potential Future Improvements

There's a lot of potential to expand on this approach. Depending on what future datasets look like, extra data cleaning might need to be added, as well as compatibility for other file extensions (for example, XML). 
