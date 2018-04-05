#Having an impossible time reading FEC data?
#
#Here is an example converting Itemized Individual Donations in 2016 to CSV format. This will allow you to look at every itemized 
#individual contribution to a campaign by individuals who donated at least $200 to a single election committee.  This methodology should
#also work with all FEC files dating back to the year 2000. 
#
#Please keep in mind that most of the files you download will be too large to read in Excel in a CSV format however you can look at them 
# in JMP or by using Pandas.

#The FEC gives the column names of the data in a different file titled "Comma Delimitted Header File" in CSV format.  
#This can be confusing because you need to add names to the columns of data or the data will not make any sense. 

#The Contributions by Individuals file and all the other associated and downloadable files are txt files, delimited in ASCII-28 format, 
#separated by a '|'. Therefore it's only possible to read the data into a Pandas dataframe by using the line: 
#encoding = "ISO-8859-1",sep='|' while reading the file. 

#Dont' worry - the full line of code is provided below. After you follow the steps below, you can run the Python code provided in any 
#IDE or a Jupyter Notebook. 

#To add to the confusion, the FEC does not change the name of the file to align it with the election year, after it's unzipped.
#In other words, the file names for election data found in 2016 will be the same as the file names in 2014 or 2012. 
#Therefore it's important to download them into a file directory with the election year clearly marked. 

#STEP 1 -------------------------------------------------------
#
#Create a directory on your C drive titled 'Election Year 2016'
#WARNING:  This file has over 22 million rows of data. So if you don't have enough space on your C drive, 
#it may be necessary to use an external drive instead of your C drive. 

#STEP 2 -------------------------------------------------------
#
#Start by downloading the "Comma Delimited Header File" into the directory marked 'Election Year 2016' 
#Here is a link to the "Comma Delimited Header File" it's file name is 'indiv_header_file.csv'
#Link ---->   https://classic.fec.gov/finance/disclosure/metadata/indiv_header_file.csv
#
#Download the Comma Delimited Header File to the 'C:/Election Year 2016/' directory.
#If the file name is followed by (2), that means you downloaded it twice. Remove the last part so it reads, 'indiv_header_file'
#
#STEP 3 -------------------------------------------------------
#
#Next download the "Contributions by Individuals" zip file into the directory marked 'Election Year 2016' 
#Here is a link to the "Contributions by Individuals" zip file. It's named indiv16.zip
#Link ---->   https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2016/indiv16.zip
#
#STEP 4 -------------------------------------------------------
#
#Download the Contributions by Individuals to the 'C:/Election Year 2016/' directory. 
#If the file name is followed by (2), that means you downloaded it twice. Remove the last part so it reads, 'indiv16.zip'
#
#This will download a zipped file folder title, 'indiv16.zip'  Navigate to that folder, left click on it and highlight it.  
#Then right click on it, scroll up and then left click on 'Extract All'
#A new folder titled 'indiv16' will appear. Navigate to that and open it. You should find the txt file named 'itcont.txt'.  
#
#STEP 5 -------------------------------------------------------
#
#Then use this Python code to combine this file into a readable CSV file. 
#WARNING: This step could take a long time, because it has to convert 22 million rows of data to a CSV format. 
#
#When it's done, it will also allow you to to browse the individual donations in a pandas datframe. 
#You will see their name, employer, occupation, state, city, zip code, the amount donated, the date of donation, and to where it was donated to.
#
#The CSV file will be named 'individual_contributions_2016.csv' and it will be found in the 'C:/Election Year 2016/' directory.
#
#Python Code --------------------------------------------------
#

import pandas as pd
import numpy as np

#Establish the file paths
header_filepath = 'C:/Election Year 2016/indiv_header_file.csv'
contributions_filepath = 'C:/Election Year 2016/indiv16/itcont.txt'
contributions_csv_filepath = 'C:/Election Year 2016/individual_contributions_2016.csv'

#Read in the header file path
header_df = pd.read_csv(header_filepath)    

#Convert the TXT file to a readable Pandas dataframe while combining it with the column names in the header file.
contributions_df = pd.read_csv(contributions_filepath,encoding = "ISO-8859-1",sep='|',names=header_df,index_col=False)

#Write the converted file to CSV format. 
contributions_df.to_csv(contributions_csv_filepath)   

#Displays some of the contents of the dataframe. 
contributions_df.head(100)  






