# Import Python packages 
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv

# checking your current working directory
print(os.getcwd())

# Get your current folder and subfolder event data
filepath = os.getcwd() + '/event_data'

# Create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    
# join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root,'*'))
    #print(file_path_list)

# initiating an empty list of rows that will be generated from each file
full_data_rows_list = [] 
    
# for every filepath in the file path list 
for f in file_path_list:

# reading csv file 
####    with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
        # creating a csv reader object 
####        csvreader = csv.reader(csvfile) 
####        next(csvreader)

# We'll try to do this thing in Pandas' way :)
# https://www.kite.com/python/answers/how-to-make-a-single-pandas-dataframe-from-multiple-%60.csv%60-files-in-python

# Be careful of existing Pandas gotchas, especially section "NA type promotions".
# https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html
# https://stackoverflow.com/questions/39666308/pd-read-csv-by-default-treats-integers-like-floats
# https://stackoverflow.com/questions/23348883/how-do-i-prevent-pandas-from-recasting-my-integer-values-to-floats
# https://stackoverflow.com/questions/21287624/convert-pandas-column-containing-nans-to-dtype-int

# Looks like Pandas version starting from 0.24.0 supports column with null values to be integer.
# https://pandas.pydata.org/pandas-docs/stable/user_guide/integer_na.html

# It's a shame that Udacity's project workspaces currently use Pandas 0.23.3, but fortunately there's a workaround.
# Just convert column of int type to str type, and then we can stop Pandas from promoting this column to float64 :)
# https://stackoverflow.com/questions/40251948/stop-pandas-from-converting-int-to-float/40252138
    full_data_rows_list.append(pd.read_csv(f, dtype={"userId": str}))

# extracting each data row one by one and append it        
####        for line in csvreader:
            #print(line)
####            full_data_rows_list.append(line)

combined_df = pd.concat(full_data_rows_list)

# uncomment the code below if you would like to get total number of rows 
#print(len(full_data_rows_list))
# uncomment the code below if you would like to check to see what the list of event data rows will look like
#print(full_data_rows_list)

# creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
# Apache Cassandra tables
####csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

####with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
####    writer = csv.writer(f, dialect='myDialect')
####    writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
####                'level','location','sessionId','song','userId'])
####    for row in full_data_rows_list:
####        if (row[0] == ''):
####            continue
####        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))

combined_df.drop(['auth', 'method', 'page', 'registration', 'status', 'ts'], axis=1, inplace=True)
# https://stackoverflow.com/questions/49291740/delete-rows-if-there-are-null-values-in-a-specific-column-in-pandas-dataframe
# https://stackoverflow.com/questions/46091924/python-how-to-drop-a-row-whose-particular-column-is-empty-nan
combined_df = combined_df.dropna(subset=['artist'])
# https://datatofish.com/export-dataframe-to-csv/
# https://stackoverflow.com/questions/12877189/float64-with-pandas-to-csv
combined_df.to_csv(r'event_datafile_new.csv', index = False, float_format='%.5f')

# check the number of rows in your csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))

# Now that we have a Pandas-generated CSV ready, we can test this file in project template notebook
# Simply skip code cells in "Part I" which would create the CSV file, but remember to execute first cell to import Python packages

# Supplements
# https://discourse.julialang.org/t/csv-read-performance-vs-pandas/21667
# https://www.programiz.com/python-programming/csv
# https://www.shanelynn.ie/python-pandas-read-csv-load-data-from-csv-files/
# https://datatofish.com/import-csv-file-python-using-pandas/
# https://realpython.com/python-csv/