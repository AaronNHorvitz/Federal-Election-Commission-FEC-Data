#Here is the Python code to parse the itemized expenses reported to the FEC (Federal Election Commission) by 
#election committees and group them into 52 separate expense categories. 
#
#Written by Aaron Horvitz
#
#The original data can be downloaded here: https://classic.fec.gov/finance/disclosure/ftpdet.shtml
#
#First create the following directories:
#
#'D:/Election Data/Downloaded FEC Data/New Output/Final Committee Expense Reports/
#'D:/Election Data/Downloaded FEC Data/New Output/Expense Counts/Final Merged Files/
#'D:/Election Data/Downloaded FEC Data/New Output/Expense Totals/
#
#It is recommended that you downlaod and extract each file sperately as provided in the previuos instructions and arrange them 
#by year in the file folders named below going back as many years as you like to 2000.
#
#For example, download 2015-1016 Operating Expenditures data to:
#'D:/Election Data/Downloaded FEC Data/2015 - 2016 Data Files/oppexp16/oppexp.txt'
#'D:/Election Data/Downloaded FEC Data/2015 - 2016 Data Files/oppexp16/oppexp_header_file.csv'
#
#For example, download 2013-1014 Operating Expenditures data to:
#'D:/Election Data/Downloaded FEC Data/2013 - 2014 Data Files/oppexp16/oppexp.txt'
#'D:/Election Data/Downloaded FEC Data/2013 - 2014 Data Files/oppexp16/oppexp_header_file.csv'
#
#Continue for previous years....
#Do the same for the Committee Master File and the Contributions by Individuals
#
#Downlod the 2015-2016 Committee Master File data to:
#'D:/Election Data/Downloaded FEC Data/2015 - 2016 Data Files/cm16/cm.txt'
#'D:/Election Data/Downloaded FEC Data/2015 - 2016 Data Files/cm16/cm_header_file.csv'
#
##Downlod the 2015-2016 Contributions by Individuals to:
#'D:/Election Data/Downloaded FEC Data/2015 - 2016 Data Files/indiv16/itcont.txt'
#'D:/Election Data/Downloaded FEC Data/2015 - 2016 Data Files/indiv16/indiv_header_file.csv'
#

import csv
import pandas as pd
import numpy as np

#Calculate the election number ex. 2000 would be 00' and 2012 would be 12'

def calculate_election_number(election_year,p='no'):
    
    if election_year >= 2010:              #election must be greater than or equal to 2010
        number_year = election_year-2000
        
    elif election_year >= 2000:            #election must be greater than or equal to 2000 but less than 2010
        number_year = '0'+str(election_year-2000)
    
    elif election_year >= 1900:            #election must be greater than or equal to 1900 but less than 2000
        number_year = election_year-1900
    else:
        number_year = 'Unresolved:  Cannot calculate number year'
        
    #Print the results if p = print
    
    if p == 'print':
        print('')
        print('The Election Year is:  '+str(election_year))
        print('') 
    elif p != 'print':    
        return(number_year)
        pass
        
    return number_year

#Calculate the election cycle from the election year ex. 2016 would be a PRESIDENTIAL election cycle, and 2018 is MIDTERM'
def calculate_election_cycle(year,p='no'):
    
    if year%4 == 0:                          #PRESIDENITIAL election years have a remainder of 0 when divided by 4
        election_type = "PRESIDENTIAL"
    else:                                    #All else would be considered a MITERM
        election_type = 'MIDTERM'

    #Print the results if p = print
    
    if p == 'print':
        print('')
        print('The '+str(year)+' General Election is labeled as a '+str(election_type)+' election cycle.')
        print('')
    elif p != 'print':
        return(election_type)
        pass

    return(election_type)

#Definitions for the filepaths

def find_raw_expense_filepaths(year):
    
    prior_year = year-1
    election_year = year
    number_year = calculate_election_number(election_year,p='no')
    
    FEC_raw_expense_data_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/oppexp'+str(number_year)+'/oppexp.txt'
    FEC_raw_expense_header_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/oppexp'+str(number_year)+'/oppexp_header_file.csv'
    FEC_raw_expense_csv_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/oppexp'+str(number_year)+'/oppexp.csv'

    return (FEC_raw_expense_data_filepath,FEC_raw_expense_header_filepath,FEC_raw_expense_csv_filepath)

def find_raw_individual_data_filepaths(year):
    
    prior_year = year-1
    election_year = year
    number_year = calculate_election_number(election_year,p='no')
    
    FEC_raw_individual_data_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/indiv'+str(number_year)+'/itcont.txt'
    FEC_raw_individual_header_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/indiv'+str(number_year)+'/indiv_header_file.csv'
    FEC_raw_individual_csv_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/indiv'+str(number_year)+'/itcont.csv'

    return (FEC_raw_individual_data_filepath,FEC_raw_individual_header_filepath,FEC_raw_individual_csv_filepath)

def find_raw_committee_data_filepaths(year):
    
    prior_year = year-1
    election_year = year
    number_year = calculate_election_number(election_year,p='no')
    
    FEC_raw_committee_data_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/cm'+str(number_year)+'/cm.txt'
    FEC_raw_committee_header_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/cm'+str(number_year)+'/cm_header_file.csv'
    FEC_raw_committee_csv_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/cm'+str(number_year)+'/cm.csv'

    return(FEC_raw_committee_data_filepath,FEC_raw_committee_header_filepath,FEC_raw_committee_csv_filepath)

def find_final_outputs_filepaths(year):
    
    prior_year = year-1
    election_year = year
    number_year = calculate_election_number(election_year,p='no')

    FEC_categorized_expense_csv_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/OUTPUT/parsed_and_categorized_expenses_'+str(election_year)+'.csv'
    FEC_donations_groupedby_committee_csv_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/OUTPUT/total_donations_to_committees_'+str(election_year)+'.csv'
    FEC_expenses_groupedby_committee_csv_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/OUTPUT/total_expenses_by_committee_'+str(election_year)+'.csv'
    Merged_expenses_and_donations_filepath = 'D:/Election Data/Downloaded FEC Data/'+str(prior_year)+' - '+str(election_year)+' Data Files/OUTPUT/merged_total_expenses_and_donations_by_committee_'+str(election_year)+'.csv'

    return(FEC_categorized_expense_csv_filepath,FEC_donations_groupedby_committee_csv_filepath,FEC_expenses_groupedby_committee_csv_filepath,Merged_expenses_and_donations_filepath)
           
    #New Output For Final Merged File
    
def find_New_Output_filepaths(year):
    master_merged_output_file_path = 'D:/Election Data/Downloaded FEC Data/New Output/Final Committee Expense Reports/final_expense_report_'+str(election_year)+'.csv'
    category_count_file_path = 'D:/Election Data/Downloaded FEC Data/New Output/Expense Counts/Final Merged Files/counts_of_each_expense_'+str(election_year)+'.csv'
    category_total_file_path = 'D:/Election Data/Downloaded FEC Data/New Output/Expense Totals/Master_Merged_and_Categorized_Expenses_File_'+str(election_year)+'.csv' 
    
    return(master_merged_output_file_path,category_count_file_path,category_total_file_path)

#Definitions for reading the data in raw

def select_expenses_columns(local_df):

    local_df = local_df[['CMTE_ID','RPT_YR','RPT_TP','NAME','CITY','STATE','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','PURPOSE','ENTITY_TP']]

    return local_df

    
def read_FEC_data(fec_data_filepath, header_filepath):
    print('')
    print('-------- Reading in the raw data --------')
    print('')
   
    header_df=pd.read_csv(header_filepath)  
    local_df = pd.read_csv(fec_data_filepath,encoding = "ISO-8859-1",sep='|',names = header_df,index_col=False)

    #Print dataframe with headers
    local_df.head(600)

    
    return local_df   

#Create categories column to parse expenses into:

def parsing_report(expenses_df):

    local_df = expenses_df
    
    parsing_report_1 = local_df['CATEGORIES'].describe()    
    
    #Print out parsing reports
    print("******")     
    print("Parsing Report------------------------------")
    print("Here are the counts:")
    print(parsing_report_1)
    print("")

def parsing_report_counts(local_df):
    
    local_df = local_df.CATEGORIES.value_counts()[:70] 
    
    return(local_df)
    
    
def create_categories_column(expenses_df):
    
    print("")
    print("--------Creating a column titled CATEGORIES to parse expense items into-------")
    print("")
    
    local_df=expenses_df
    local_df['CATEGORIES']=local_df['PURPOSE']
    
    parsing_report(local_df)      #Print out parsing report
    
    return local_df    



#Parser for Compensation to consultants:

def parse_compensation_consultants(expenses_df):
    
    print("")
    print("--------Parsing Compensation for Consultants from Expense Items--------")
    print("")

    local_df=expenses_df
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CONSULTING'), 'Compensation to Consultants',   
                         np.where(local_df['CATEGORIES'].str.contains('CONSULTANT'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('CONSULT'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('RETAINER'),'Compensation to Consultants', 
                         np.where(local_df['CATEGORIES'].str.contains('ADVICE'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('ADVISING'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('ADVISOR'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('ADVISORS'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('ADVISER'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('ADVISERS'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('GOAL'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('GOALS'), 'Compensation to Consultants',                              
                         np.where(local_df['CATEGORIES'].str.contains('MISSION'), 'Compensation to Consultants', 
                         np.where(local_df['CATEGORIES'].str.contains('POLICY'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('POLICIES'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('STRATEGY'), 'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('STRATEGIC'), 'Compensation to Consultants', local_df['CATEGORIES']
                             )))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    
    return local_df


#Parser for Compensation to Staff:

def parse_compensation_staff(expenses_df):
     
    print("")
    print("--------Parsing Compensation for Staff from Expense Items--------")
    print("")    
    
    local_df=expenses_df
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('STAFF'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('STAFFING'),'Compensation to Staff',   
                         np.where(local_df['CATEGORIES'].str.contains('TEMP'),'Compensation to Staff',                             
                         np.where(local_df['CATEGORIES'].str.contains('RECEPTIONIST'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('SECRETARY'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('ASSISTANT'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('COORDINATOR'),'Compensation to Staff',                               
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE COORDINATOR'),'Compensation to Staff',                                    
                         np.where(local_df['CATEGORIES'].str.contains('SUPPORT'),'Compensation to Staff',                                   
                         np.where(local_df['CATEGORIES'].str.contains('PERSONNEL'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('PERSONEL'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('PERSONAL'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('ADMINISTRATIVE'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('MESSENGER'),'Compensation to Staff',       
                         np.where(local_df['CATEGORIES'].str.contains('ADMINISTRATION'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE COORDINATION'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('CLERICAL'),'Compensation to Staff',  
                         np.where(local_df['CATEGORIES'].str.contains('TEMPORARY'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('MANAGER'),'Compensation to Staff',        
                         np.where(local_df['CATEGORIES'].str.contains('MANAGEMENT'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('MGMT'),'Compensation to Staff',  
                         np.where(local_df['CATEGORIES'].str.contains('MTG'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('FINANCE ASSOCIATE'),'Compensation to Staff',                               
                         np.where(local_df['CATEGORIES'].str.contains('ASSOCIATE'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('DIRECTOR'),'Compensation to Staff',                              
                         np.where(local_df['CATEGORIES'].str.contains('EMPLOYEE'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('TREASURER'),'Compensation to Staff',                             
                         np.where(local_df['CATEGORIES'].str.contains('INTERN'),'Compensation to Staff',      
                         np.where(local_df['CATEGORIES'].str.contains('ANALYST'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('TREASURER'),'Compensation to Staff',     
                         np.where(local_df['CATEGORIES'].str.contains('LABOR'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('LABOR'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('LABORER'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('WORKER'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('FIELD'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('SCHEDULER'),'Compensation to Staff',                              
                         np.where(local_df['CATEGORIES'].str.contains('OPERATIONS'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('FIELD OPERATIONS'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('ORGANIZER'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('SUMMER FELLOWS'),'Compensation to Staff',                                  
                         np.where(local_df['CATEGORIES'].str.contains('VOLUNTEER ORGANIZER'),'Compensation to Staff',  
                         np.where(local_df['CATEGORIES'].str.contains('VOLUNTEER COST'),'Compensation to Staff',   
                         np.where(local_df['CATEGORIES'].str.contains('VOLUNTEER EXPENSE'),'Compensation to Staff',   
                         np.where(local_df['CATEGORIES'].str.contains('VOLUNTEER EXP'),'Compensation to Staff',                                             
                         np.where(local_df['CATEGORIES'].str.contains('COORDINATOR'),'Compensation to Staff',
                         np.where(local_df['CATEGORIES'].str.contains('HELP'),'Compensation to Staff',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))))))))))))))))))

          
    parsing_report(local_df)      #Print out parsing report
    return local_df

                              
def parse_compensation_contractors(expenses_df):
    
    print("")
    print("--------Parsing Compensation for Contractors from Expense Items--------")
    print("")    

    local_df=expenses_df    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CONTRACTOR'), 'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('CONTRACT PAY'), 'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('CONTRACT'), 'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('CONTRACT PAY'), 'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('VENDOR'),'Compensation to Contractors',                              
                         np.where(local_df['CATEGORIES'].str.contains('VENDORS'),'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('SUB VENDOR'),'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('SUB-VENDOR'),'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('SUBVENDOR'),'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('SUBVENDORS'),'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('SUB VENDORS'),'Compensation to Contractors',
                         np.where(local_df['CATEGORIES'].str.contains('SUB-VENDORS'),'Compensation to Contractors',local_df['CATEGORIES']
                         ))))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df



def parse_compensation_hourly_and_salary(expenses_df):
    
    print("")
    print("--------Parsing Compensation for Hourly and Salary Items from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('WAGE'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('WAGES'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('WORK'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('SALARY'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('SALARIES'),'Compensation for Salary and Hourly',                             
                         np.where(local_df['CATEGORIES'].str.contains('WAGE'),'Compensation for Salary and Hourly',  
                         np.where(local_df['CATEGORIES'].str.contains('PAYROLL'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('PAY ROLL'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('PAY ROLE'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('PARYOLL'),'Compensation for Salary and Hourly',                              
                         np.where(local_df['CATEGORIES'].str.contains('WAGES'),'Compensation for Salary and Hourly',  
                         np.where(local_df['CATEGORIES'].str.contains('EPAY'),'Compensation for Salary and Hourly',  
                         np.where(local_df['CATEGORIES'].str.contains('E PAY'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('E-PAY'),'Compensation for Salary and Hourly',       
                         np.where(local_df['CATEGORIES'].str.contains('COMPENSATION'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('PAYCHECK'),'Compensation for Salary and Hourly',       
                         np.where(local_df['CATEGORIES'].str.contains('PAY CHECK'),'Compensation for Salary and Hourly', 
                         np.where(local_df['CATEGORIES'].str.contains('USA EPAY'),'Compensation for Salary and Hourly',                              
                         np.where(local_df['CATEGORIES'].str.contains('HOURS'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('LABOR HOURS'),'Compensation for Salary and Hourly',                                  
                         np.where(local_df['CATEGORIES'].str.contains('PARTIME'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('PARTTIME'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('PART TIME'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('LABOR HOURS'),'Compensation for Salary and Hourly',    
                         np.where(local_df['CATEGORIES'].str.contains('HOURS'),'Compensation for Salary and Hourly',                            
    #Levies on pay would otherwise be paid out as pay
                         np.where(local_df['CATEGORIES'].str.contains('GARNISHMENT'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('GARNISHMENTS'),'Compensation for Salary and Hourly', 
                         np.where(local_df['CATEGORIES'].str.contains('LEVY'),'Compensation for Salary and Hourly',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df

def compensation_bonuses_and_commission(expenses_df):

    print("")
    print("--------Parsing Compensation for Bonuses and Commission Items from Expense Items--------")
    print("")   
    
    local_df=expenses_df    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('BONUS'),'Compensation as Bonuses and Commission',
                         np.where(local_df['CATEGORIES'].str.contains('BONUSES'),'Compensation as Bonuses and Commission',
                         np.where(local_df['CATEGORIES'].str.contains('COMMISSION'),'Compensation as Bonuses and Commission',                              
                         np.where(local_df['CATEGORIES'].str.contains('COMMISSIONS'),'Compensation as Bonuses and Commission',  
                         np.where(local_df['CATEGORIES'].str.contains('COMMISION'),'Compensation as Bonuses and Commission',                              
                         np.where(local_df['CATEGORIES'].str.contains('COMMISIONS'),'Compensation as Bonuses and Commission',  
                         np.where(local_df['CATEGORIES'].str.contains('COMISSION'),'Compensation as Bonuses and Commission',                              
                         np.where(local_df['CATEGORIES'].str.contains('COMISSIONS'),'Compensation as Bonuses and Commission',local_df['CATEGORIES']
                         )))))))) 

    parsing_report(local_df)      #Print out parsing report 
    return local_df



def compensation_benefits(expenses_df):
    
    print("")
    print("--------Parsing Compensation for Benefits from Expense Items--------")
    print("")   
    
    local_df=expenses_df

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('MEDICAL INSURANCE'),'Compensation as Benefits',
                         np.where(local_df['CATEGORIES'].str.contains('MEDICAL INS'),'Compensation as Benefits',                                        
                         np.where(local_df['CATEGORIES'].str.contains('MED INSURANCE'),'Compensation as Benefits',       
                         np.where(local_df['CATEGORIES'].str.contains('MED INS'),'Compensation as Benefits',    
                         np.where(local_df['CATEGORIES'].str.contains('EMPLOYEE INSURANCE'),'Compensation as Benefits', 
                         np.where(local_df['CATEGORIES'].str.contains('INSURANCE'),'Compensation as Benefits', 
                         np.where(local_df['CATEGORIES'].str.contains('HEALTHCARE'),'Compensation as Benefits', 
                         np.where(local_df['CATEGORIES'].str.contains('HEALTH CARE'),'Compensation as Benefits',   
                         np.where(local_df['CATEGORIES'].str.contains('HEALTH'),'Compensation as Benefits', 
                         np.where(local_df['CATEGORIES'].str.contains('HEALTH INS'),'Compensation as Benefits', 
                         np.where(local_df['CATEGORIES'].str.contains('HEALTH PLAN'),'Compensation as Benefits', 
                         np.where(local_df['CATEGORIES'].str.contains('HEALTH'),'Compensation as Benefits',     
                         np.where(local_df['CATEGORIES'].str.contains('WORKERS COMP'),'Compensation as Benefits',    
                         np.where(local_df['CATEGORIES'].str.contains('WORKER COMP'),'Compensation as Benefits',  
                         np.where(local_df['CATEGORIES'].str.contains('RETIREMENT'),'Compensation as Benefits',
                         np.where(local_df['CATEGORIES'].str.contains('SARSEP'),'Compensation as Benefits',  
                         np.where(local_df['CATEGORIES'].str.contains('SIMPLIFIED EMPLOYEE PENSION'),'Compensation as Benefits',  
                         np.where(local_df['CATEGORIES'].str.contains('PENSION'),'Compensation as Benefits',  
                         np.where(local_df['CATEGORIES'].str.contains('SIMPLIFIED EMPLOYEE RETIREMENT PLAN'),'Compensation as Benefits',                              
                         np.where(local_df['CATEGORIES'].str.contains('SUPPORT'),'Compensation as Benefits', 
                         np.where(local_df['CATEGORIES'].str.contains('STIPEND'),'Compensation as Benefits',
                         np.where(local_df['CATEGORIES'].str.contains('FLEX PLAN'),'Compensation as Benefits',
                         np.where(local_df['CATEGORIES'].str.contains('RELOCATION'),'Compensation as Benefits',                                
                         np.where(local_df['CATEGORIES'].str.contains('IRA'),'Compensation as Benefits',
                         np.where(local_df['CATEGORIES'].str.contains('401'),'Compensation as Benefits',
                         np.where(local_df['CATEGORIES'].str.contains('401K'),'Compensation as Benefits',local_df['CATEGORIES'] 
                         ))))))))))))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df




def accounting_expense(expenses_df):
    
    print("")
    print("--------Parsing Accounting Expenses from Expense Items--------")
    print("")   
    
    local_df=expenses_df

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('ACCOUNTING'),'Accounting Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ACOUNTING'),'Accounting Expense',                                         
                         np.where(local_df['CATEGORIES'].str.contains('ACCOUNTANT'),'Accounting Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ACCOUNT ANALYSIS'),'Accounting Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ACCIOUNTING'),'Accounting Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ACCOUNING'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('BOOKKEEPING'),'Accounting Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('BOOKEEPING'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('BOOK-KEEPING'),'Accounting Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('BOOK KEEPING'),'Accounting Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('TREASURY'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('TRESURY'),'Accounting Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('FINANCIAL'),'Accounting Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('AUDITING'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('COMPLIANCE'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('FILING'),'Accounting Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('FILLING'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AX BILL'),'Accounting Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('ACCT'),'Accounting Expense',                                 
                         np.where(local_df['CATEGORIES'].str.contains('QB'),'Accounting Expense',                                          
                         np.where(local_df['CATEGORIES'].str.contains('AMENDMENT'),'Accounting Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('AMENDMENTS'),'Accounting Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('FEC'),'Accounting Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('FEDERAL ELECTION COMMISSION'),'Accounting Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('FEDERAL ELECTION COMISSION'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('FEDERAL ELECTION COMMISION'),'Accounting Expense',                              
                         np.where(local_df['CATEGORIES'].str.contains('REPORT'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('REPORTS'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('REPORTING'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('1099'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('1120 POL'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('1120POL'),'Accounting Expense',                             
                         np.where(local_df['CATEGORIES'].str.contains('1120-POL'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('PREPARATION'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('941'),'Accounting Expense',local_df['CATEGORIES']
                     )))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df


def legal_expense(expenses_df):

    print("")
    print("--------Parsing Legal Expenses from Expense Items--------")
    print("")   
    
    local_df=expenses_df
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('ATTORNEY'),'Legal Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('ATTORNIES'),'Legal Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('LAWYER'),'Legal Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('LAWYERS'),'Legal Expense',
                         np.where(local_df['CATEGORIES'].str.contains('COURT'),'Legal Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('LEGAL'),'Legal Expense',local_df['CATEGORIES']
                         ))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df

def association_dues_subscriptions(expenses_df):

    print("")
    print("--------Parsing Associations Dues and Subscriptions from Expense Items--------")
    print("")   
    
    local_df=expenses_df

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('ASSOCIATION'),'Association Dues and Subscriptions',
                     np.where(local_df['CATEGORIES'].str.contains('ASSOCIATIONS'),'Association Dues and Subscriptions',
                     np.where(local_df['CATEGORIES'].str.contains('SUBSCRIPTION'),'Association Dues and Subscriptions',
                     np.where(local_df['CATEGORIES'].str.contains('SUBSCRIPTIONS'),'Association Dues and Subscriptions',
                     np.where(local_df['CATEGORIES'].str.contains('PROFESSIONAL'),'Association Dues and Subscriptions',
                     np.where(local_df['CATEGORIES'].str.contains('DUES'),'Association Dues and Subscriptions',  
                     np.where(local_df['CATEGORIES'].str.contains('MEMBERSHIP'),'Association Dues and Subscriptions',    
                     np.where(local_df['CATEGORIES'].str.contains('NEWS SERVICE'),'Association Dues and Subscriptions',                                                                    
                     np.where(local_df['CATEGORIES'].str.contains('RENEWAL'),'Association Dues and Subscriptions', 
                     np.where(local_df['CATEGORIES'].str.contains('RENEWALS'),'Association Dues and Subscriptions',local_df['CATEGORIES']
                             ))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df

def marketing_expense_direct_response(expenses_df):

    print("")
    print("--------Parsing Marketing Expense Direct Response from Expense Items--------")
    print("")  

    
    local_df=expenses_df
    
    local_df['CATEGORIES'] = np.where(local_df['CATEGORIES'].str.contains('DIRECT MARKETING'),'Marketing Expense Direct Response', 
                         np.where(local_df['CATEGORIES'].str.contains('DIRECT RESPONSE'),'Marketing Expense Direct Response',                                   
                         np.where(local_df['CATEGORIES'].str.contains('JFC DIRECT MARKETING'),'Marketing Expense Direct Response', 
                         np.where(local_df['CATEGORIES'].str.contains('PAC DIRECT RESPONSE'),'Marketing Expense Direct Response',                                            
                         np.where(local_df['CATEGORIES'].str.contains('DIRECT'),'Marketing Expense Direct Response', 
                         np.where(local_df['CATEGORIES'].str.contains('DIRECT MARKETING'),'Marketing Expense Direct Response', local_df['CATEGORIES']
                                 ))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df  

def marketing_expense_fundraising(expenses_df):
        
    print("")
    print("--------Parsing Marketing Expense Fundraising from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] = np.where(local_df['CATEGORIES'].str.contains('FUNDRAISING'),'Marketing Expense Fundraising',  
                         np.where(local_df['CATEGORIES'].str.contains('FUND RAISING'),'Marketing Expense Fundraising',                               
                         np.where(local_df['CATEGORIES'].str.contains('FUND RAISING'),'Marketing Expense Fundraising', 
                         np.where(local_df['CATEGORIES'].str.contains('FUNRAISING'),'Marketing Expense Fundraising',  
                         np.where(local_df['CATEGORIES'].str.contains('FUNRAISER'),'Marketing Expense Fundraising',                             
                         np.where(local_df['CATEGORIES'].str.contains('FUN RAISER'),'Marketing Expense Fundraising',  
                         np.where(local_df['CATEGORIES'].str.contains('F/R'),'Marketing Expense Fundraising',  
                         np.where(local_df['CATEGORIES'].str.contains('FUNDRAISER'),'Marketing Expense Fundraising',  
                         np.where(local_df['CATEGORIES'].str.contains('FUND RAISER'),'Marketing Expense Fundraising', 
                         np.where(local_df['CATEGORIES'].str.contains('FUND-RAISER'),'Marketing Expense Fundraising', local_df['CATEGORIES']
                                 ))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df   

def marketing_expense_CRM(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense CRM from Expense Items--------")
    print("")   
    
    local_df=expenses_df    

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CRM'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('CUSTOMER RELATIONSHIP MANAGEMENT'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('CUSTOMER RECORD MANAGEMENT'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('CONTACT RECORD MANAGEMENT'), 'Marketing Expense for CRM',    
                         np.where(local_df['CATEGORIES'].str.contains('NATION-BUILDER'),'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('NATION BUILDER'),'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('NATIONBUILDER'),'Marketing Expense for CRM', 
                         np.where(local_df['CATEGORIES'].str.contains('TRAILBLAZER'),'Marketing Expense for CRM',                               
                         np.where(local_df['CATEGORIES'].str.contains('TRAIL BLAZER'),'Marketing Expense for CRM',                                  
                         np.where(local_df['CATEGORIES'].str.contains('TRAIL-BLAZER'),'Marketing Expense for CRM',                                 
                         np.where(local_df['CATEGORIES'].str.contains('SALESFORCE'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('SALES-FORCE'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('SALES FORCE'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('DYNAMICS'), 'Marketing Expense for CRM', 
                         np.where(local_df['CATEGORIES'].str.contains('MICROSOFT DYNAMICS'), 'Marketing Expense for CRM',                              
                         np.where(local_df['CATEGORIES'].str.contains('MICROSOFT-DYNAMICS'), 'Marketing Expense for CRM',   
                         np.where(local_df['CATEGORIES'].str.contains('SEMCASTING'), 'Marketing Expense for CRM',                                                           
                         np.where(local_df['CATEGORIES'].str.contains('SEM-CASTING'), 'Marketing Expense for CRM',                                
                         np.where(local_df['CATEGORIES'].str.contains('SEM CASTING'), 'Marketing (Customer Relationship Management)',                               
                         np.where(local_df['CATEGORIES'].str.contains('NPGVAN'), 'Marketing Expense for CRM',                                                           
                         np.where(local_df['CATEGORIES'].str.contains('NPG VAN'), 'Marketing Expense for CRM',                                
                         np.where(local_df['CATEGORIES'].str.contains('NPG-VAN'), 'Marketing Expense for CRM',     
                         np.where(local_df['CATEGORIES'].str.contains('INTRANET QUORUM'), 'Marketing Expense for CRM',                               
                         np.where(local_df['CATEGORIES'].str.contains('BSD TOOLS'), 'Marketing Expense for CRM',                                                            
                         np.where(local_df['CATEGORIES'].str.contains('TELEFORUM'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('IDONATEPRO'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('PATRIOT'),'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('TRAIL BLAZER'),'Marketing Expense for CRM', 
                         np.where(local_df['CATEGORIES'].str.contains('TRAILBLAZER'),'Marketing Expense for CRM',                               
                         np.where(local_df['CATEGORIES'].str.contains('ARISTOTLE CAMPAIGN'),'Marketing Expense for CRM',                                  
                         np.where(local_df['CATEGORIES'].str.contains('BARNSTORM'),'Marketing Expense for CRM',                                 
                         np.where(local_df['CATEGORIES'].str.contains('BLUE UTOPIA'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('CAMELOT'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN CLOUD'), 'Marketing Expense for CRM',
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN ENGINE'), 'Marketing Expense for CRM',                              
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN OPTIMIZER'), 'Marketing Expense for CRM',   
                         np.where(local_df['CATEGORIES'].str.contains('CAMPIAIGN PARNTER'), 'Marketing Expense for CRM',                                                           
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN PLANNER'), 'Marketing Expense for CRM',                                
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN TOOLBOX'), 'Marketing Expense for CRM',    
                         np.where(local_df['CATEGORIES'].str.contains('VOTEBUILDER'), 'Marketing Expense for CRM',                                                           
                         np.where(local_df['CATEGORIES'].str.contains('VOTE-BUILDER'), 'Marketing Expense for CRM',                                
                         np.where(local_df['CATEGORIES'].str.contains('VOTE BUILDER'), 'Marketing Expense for CRM',                                                                 
                         np.where(local_df['CATEGORIES'].str.contains('CFB STRATEGIES'), 'Marketing Expense for CRM',                                                           
                         np.where(local_df['CATEGORIES'].str.contains('CQRC ENGAGE'), 'Marketing Expense for CRM',      
                         np.where(local_df['CATEGORIES'].str.contains('CRIMSON'),'Marketing Expense for CRM',local_df['CATEGORIES']                                                                
                         )))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df


def marketing_expense_imagery(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense Imagery from Expense Items--------")
    print("")   
    
    local_df=expenses_df   
    
    local_df['CATEGORIES'] =  np.where(local_df['CATEGORIES'].str.contains('PHOTOGRAPHY'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('PHOTOS'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('PHOTO'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('PICTURE'),'Marketing Expense for Imagery',  
                        np.where(local_df['CATEGORIES'].str.contains('PICTURES'),'Marketing Expense for Imagery', 
                        np.where(local_df['CATEGORIES'].str.contains('PHOTO SHOOT'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('CAMERA'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('CAMERAS'),'Marketing Expense for Imagery',                             
                        np.where(local_df['CATEGORIES'].str.contains('IMAGERY'),'Marketing Expense for Imagery',     
                        np.where(local_df['CATEGORIES'].str.contains('IMAGRY'),'Marketing Expense for Imagery',   
                        np.where(local_df['CATEGORIES'].str.contains('IMAGES'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('IMAGE'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('ART'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('ARTWORK'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('ART WORK'),'Marketing Expense for Imagery',  
                        np.where(local_df['CATEGORIES'].str.contains('PHOTO SHOOTS'),'Marketing Expense for Imagery', 
                        np.where(local_df['CATEGORIES'].str.contains('GRAPHIC'),'Marketing Expense for Imagery',  
                        np.where(local_df['CATEGORIES'].str.contains('GRAPHICS'),'Marketing Expense for Imagery',   
                        np.where(local_df['CATEGORIES'].str.contains('DESIGN'),'Marketing Expense for Imagery',                            
                        np.where(local_df['CATEGORIES'].str.contains('DESIGNS'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('VIDEO'),'Marketing Expense for Imagery',
                        np.where(local_df['CATEGORIES'].str.contains('VIDEOS'),'Marketing Expense for Imagery',                            
                        np.where(local_df['CATEGORIES'].str.contains('VIDEOGRAPHY'),'Marketing Expense for Imagery',    
    #Design Software                             
                         np.where(local_df['CATEGORIES'].str.contains('WONDERSHARE'), 'Marketing Expense for Imagery',
                         np.where(local_df['CATEGORIES'].str.contains('ADOBE'), 'Marketing Expense for Imagery',
                         np.where(local_df['CATEGORIES'].str.contains('AUTOCAD'), 'Marketing Expense for Imagery',          
                         np.where(local_df['CATEGORIES'].str.contains('AUTO CAD'), 'Marketing Expense for Imagery', 
                         np.where(local_df['CATEGORIES'].str.contains('AUTO-CAD'), 'Marketing Expense for Imagery', 
                         np.where(local_df['CATEGORIES'].str.contains('COREL'), 'Marketing Expense for Imagery',                               
                         np.where(local_df['CATEGORIES'].str.contains('INDESIGN'), 'Marketing Expense for Imagery', 
                         np.where(local_df['CATEGORIES'].str.contains('IN DESIGN'), 'Marketing Expense for Imagery',     
                         np.where(local_df['CATEGORIES'].str.contains('IN-DESIGN'), 'Marketing Expense for Imagery',  
                         np.where(local_df['CATEGORIES'].str.contains('PHOTOSHOP'), 'Marketing Expense for Imagery',
                         np.where(local_df['CATEGORIES'].str.contains('PHOTO SHOP'), 'Marketing Expense for Imagery',                                                     
                         np.where(local_df['CATEGORIES'].str.contains('PHOTO-SHOP'), 'Marketing Expense for Imagery',                               
                         np.where(local_df['CATEGORIES'].str.contains('SOLIDWORKS'), 'Marketing Expense for Imagery', 
                         np.where(local_df['CATEGORIES'].str.contains('SOLID-WORKS'), 'Marketing Expense for Imagery',     
                         np.where(local_df['CATEGORIES'].str.contains('SOLID WORKS'), 'Marketing Expense for Imagery',                                
                         np.where(local_df['CATEGORIES'].str.contains('COREL'), 'Marketing Expense for Imagery',                                                     
                         np.where(local_df['CATEGORIES'].str.contains('CORREL'), 'Marketing Expense for Imagery',                               
                         np.where(local_df['CATEGORIES'].str.contains('CORELDRAW'), 'Marketing Expense for Imagery', 
                         np.where(local_df['CATEGORIES'].str.contains('COREL-DRAW'), 'Marketing Expense for Imagery',     
                         np.where(local_df['CATEGORIES'].str.contains('COREL DRAW'), 'Marketing Expense for Imagery',   
                         np.where(local_df['CATEGORIES'].str.contains('ILLUSTRATOR'), 'Marketing Expense for Imagery',                                 
                         np.where(local_df['CATEGORIES'].str.contains('ILUSTRATOR'), 'Marketing Expense for Imagery',  
                         np.where(local_df['CATEGORIES'].str.contains('POWERPOINT'), 'Marketing Expense for Imagery',   
                         np.where(local_df['CATEGORIES'].str.contains('POWER POINT'), 'Marketing Expense for Imagery',                                 
                         np.where(local_df['CATEGORIES'].str.contains('POWER-POINT'), 'Marketing Expense for Imagery',  
                         np.where(local_df['CATEGORIES'].str.contains('WORD'), 'Marketing Expense for Imagery',
                         np.where(local_df['CATEGORIES'].str.contains('WORDPERFECT'), 'Marketing Expense for Imagery',
                         np.where(local_df['CATEGORIES'].str.contains('WORD PERFECT'), 'Marketing Expense for Imagery',
                         np.where(local_df['CATEGORIES'].str.contains('GOOGLE DOCS'), 'Marketing Expense for Imagery',
                         np.where(local_df['CATEGORIES'].str.contains('AUTODESK'), 'Marketing Expense for Imagery',                               
                         np.where(local_df['CATEGORIES'].str.contains('AUTO DESK'), 'Marketing Expense for Imagery', 
                         np.where(local_df['CATEGORIES'].str.contains('AUTO-DESK'), 'Marketing Expense for Imagery',local_df['CATEGORIES']                                                                
                         )))))))))))))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df

def marketing_expense_collateral_and_print(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Collateral and Print from Expense Items--------")
    print("")   
    
    local_df=expenses_df 
    
    local_df['CATEGORIES'] =  np.where(local_df['CATEGORIES'].str.contains('COLLATERAL'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('COLATERAL'),'Marketing Expense for Collateral and Print', 
                        np.where(local_df['CATEGORIES'].str.contains('DECAL'),'Marketing Expense for Collateral and Print',                              
                        np.where(local_df['CATEGORIES'].str.contains('DECALS'),'Marketing Expense for Collateral and Print',                              
                        np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN COLLATERAL'),'Marketing Expense for Collateral and Print', 
                        np.where(local_df['CATEGORIES'].str.contains('EMBROIDERY'),'Marketing Expense for Collateral and Print',                     
                        np.where(local_df['CATEGORIES'].str.contains('PRINT'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('PRINTS'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('PRINTING'),'Marketing Expense for Collateral and Print', 
                        np.where(local_df['CATEGORIES'].str.contains('BOOKS'),'Marketing Expense for Collateral and Print', 
                        np.where(local_df['CATEGORIES'].str.contains('FLYER'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('FLYERS'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('FLIER'),'Marketing Expense for Collateral and Print',                             
                        np.where(local_df['CATEGORIES'].str.contains('FLIERS'),'Marketing Expense for Collateral and Print', 
                        np.where(local_df['CATEGORIES'].str.contains('HANDOUTS'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('HAND OUTS'),'Marketing Expense for Collateral and Print',                             
                        np.where(local_df['CATEGORIES'].str.contains('HAND-OUTS'),'Marketing Expense for Collateral and Print',                            
                        np.where(local_df['CATEGORIES'].str.contains('MATERIAL'),'Marketing Expense for Collateral and Print',                            
                        np.where(local_df['CATEGORIES'].str.contains('MATERIALS'),'Marketing Expense for Collateral and Print', 
                        np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN MATERIAL'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN MATERIALS'),'Marketing Expense for Collateral and Print',  
                        np.where(local_df['CATEGORIES'].str.contains('BUMPERSTICKER'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('BUMPER STICKER'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('BUMPER-STICKER'),'Marketing Expense for Collateral and Print',
                        np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN STICKERS'),'Marketing Expense for Collateral and Print',                                    
                        np.where(local_df['CATEGORIES'].str.contains('STICKERS'),'Marketing Expense for Collateral and Print',                               
                        np.where(local_df['CATEGORIES'].str.contains('POSTER'),'Marketing Expense for Collateral and Print',                                   
                        np.where(local_df['CATEGORIES'].str.contains('POSTERS'),'Marketing Expense for Collateral and Print',         
                        np.where(local_df['CATEGORIES'].str.contains('BROCHURE'),'Marketing Expense for Collateral and Print',                          
                        np.where(local_df['CATEGORIES'].str.contains('BROCHURES'),'Marketing Expense for Collateral and Print',local_df['CATEGORIES']                                                                
                         ))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df

def marketing_expense_promotional_items(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Promotional Items from Expense Items--------")
    print("")   
    
    local_df=expenses_df 

    local_df['CATEGORIES'] =  np.where(local_df['CATEGORIES'].str.contains('PROMOTION'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PROMOTIONS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PROMOTIONAL'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PROMOTIONALS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PROMOTIONAL ITEM'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PROMOTIONAL-ITEM'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PROMOTIONAL ITEMS'),'Marketing Expense for Promotional Items',   
                        np.where(local_df['CATEGORIES'].str.contains('PROMOTIONAL-ITEMS'),'Marketing Expense for Promotional Items', 
                        np.where(local_df['CATEGORIES'].str.contains('TCHOTCHKE'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('TCHOTCHKES'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('BUTTON'),'Marketing Expense for Promotional Items',                            
                        np.where(local_df['CATEGORIES'].str.contains('BUTTONS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN PARAPHERNALIA'),'Marketing Expense for Promotional Items',                            
                        np.where(local_df['CATEGORIES'].str.contains('PARAPHERNALIA'),'Marketing Expense for Promotional Items',                                 
                        np.where(local_df['CATEGORIES'].str.contains('MERCHANDISE'),'Marketing Expense for Promotional Items',   
                        np.where(local_df['CATEGORIES'].str.contains('HAT'),'Marketing Expense for Promotional Items',   
                        np.where(local_df['CATEGORIES'].str.contains('HATS'),'Marketing Expense for Promotional Items',   
                        np.where(local_df['CATEGORIES'].str.contains('SHIRT'),'Marketing Expense for Promotional Items',   
                        np.where(local_df['CATEGORIES'].str.contains('SHIRTS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('CLOTHING'),'Marketing Expense for Promotional Items',   
                        np.where(local_df['CATEGORIES'].str.contains('GLASSES'),'Marketing Expense for Promotional Items',   
                        np.where(local_df['CATEGORIES'].str.contains('VCAP VESTS'),'Marketing Expense for Promotional Items',                                 
                        np.where(local_df['CATEGORIES'].str.contains('T-SHIRT'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('T-SHIRTS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('CALENDAR'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('CALENDARS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('TOWEL'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('TOWELS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PEN'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PENS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('BALL'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('BALLS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PIN'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('PINS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('LAPEL'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('LAPELS'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('CANDY'),'Marketing Expense for Promotional Items',
                        np.where(local_df['CATEGORIES'].str.contains('CANDIES'),'Marketing Expense for Promotional Items',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))))))))))


    parsing_report(local_df)      #Print out parsing report
    return local_df

def marketing_expense_events(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Events--------")
    print("")   
    
    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('EVENT'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('EVENTS'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('TELE TOWN HALL'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('TOWN HALL'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('LIVE REMOTE'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('BOOTH'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('BOOTHS'),'Marketing Expense for Events',                              
                         np.where(local_df['CATEGORIES'].str.contains('TABLE'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('TABLES'),'MMarketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('ROOM'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('ROOMS'),'Marketing Expense for Events',                              
                         np.where(local_df['CATEGORIES'].str.contains('EVENT TABLE'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('EVENT TABLES'),'Marketing Expense for Events',                                                  
                         np.where(local_df['CATEGORIES'].str.contains('OUTING'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('OUTINGS'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('GUEST'),'Marketing Expense for Events',    
                         np.where(local_df['CATEGORIES'].str.contains('GUESTS'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('GUEST BOOKING'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('BAND'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('BANDS'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('MUSIC'),'Marketing Expense for Events',    
                         np.where(local_df['CATEGORIES'].str.contains('ENTERTAINMENT'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('VENUE'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('VENU'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('SOUND'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('STAGE'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('LIGHTING'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('RECEPTION'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('DECORATION'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('DECORATIONS'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('TOURNAMENT'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('MEETING'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('SHOW'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('GALA'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('PARTY'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('RAFFLE'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('AUCTION'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('TOURNAMENT'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('PARADE'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('TASTING'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('RNC'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('DNC'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('RETREAT'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('BANQUET'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('CONVENTION'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('CONFERENCE'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('MOVIE'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('GOLF'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('GOLF OUTING'),'Marketing Expense for Events',                         
                         np.where(local_df['CATEGORIES'].str.contains('MEET-N-GREET'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('MEETUP'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('MEET UP'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('MEET-UP'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('MEET AND GREET'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('MEET'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('ORGANIZE'),'Marketing Expense for Events',             
                         np.where(local_df['CATEGORIES'].str.contains('ORGANIZING'),'Marketing Expense for Events',                               
                         np.where(local_df['CATEGORIES'].str.contains('RALLY'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('AUDIO VISUAL'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('AUDIO'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('VISUAL'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('AUDIO/VISUAL SERVICES'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('AUDIO VISUAL SERVICES'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('AUDIO VISUAL SERVICES'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('AUDIO/VISUAL SVC'),'Marketing Expense for Events',                                                 
                         np.where(local_df['CATEGORIES'].str.contains('SPONSOR'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('LOGISTICS'), 'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('FESTIVAL'),'Marketing Expense for Events',                                
                         np.where(local_df['CATEGORIES'].str.contains('WOOD'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('LIVESTOCK'),'Marketing Expense for Events',      
                         np.where(local_df['CATEGORIES'].str.contains('POLITICAL ORGANIZING'),'Marketing Expense for Events',local_df['CATEGORIES']
                         )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df


def marketing_expense_event_items(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Events including Event Items--------")
    print("")   
    
    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('BADGE'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('BADGES'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('BALLOON'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('BALLOONS'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('HELIUM'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('HELLIUM'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('AWARD'),'Marketing Expense for Events',        
                         np.where(local_df['CATEGORIES'].str.contains('AWARDS'),'Marketing Expense for Events',                            
                         np.where(local_df['CATEGORIES'].str.contains('WRIST BANDS'),'Marketing Expense for Events',        
                         np.where(local_df['CATEGORIES'].str.contains('WRISTBANDS'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('LANYARD'),'Marketing Expense for Events',        
                         np.where(local_df['CATEGORIES'].str.contains('LANYARDS'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('NAME TAGS'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('NAMETAGS'),'Marketing Expense for Events',                   
                         np.where(local_df['CATEGORIES'].str.contains('BANNER'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('BANNERS'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('INSERTS'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('FLAG'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('FLAGS'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('DECORATION'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('DECORATIONS'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('RAFFLE'),'Marketing Expense for Events',                              
                         np.where(local_df['CATEGORIES'].str.contains('TICKETS'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('TICKET'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('PRIZE'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('PRIZES'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('WINNER'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('WINNERS'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('TROPHY'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('TROPHIES'),'Marketing Expense for Events',  
                         np.where(local_df['CATEGORIES'].str.contains('PLAQUE'),'Marketing Expense for Events',                            
                         np.where(local_df['CATEGORIES'].str.contains('PLAQUES'),'Marketing Expense for Events',   
                         np.where(local_df['CATEGORIES'].str.contains('PLACARD'),'Marketing Expense for Events',                                
                         np.where(local_df['CATEGORIES'].str.contains('PLACARDS'),'Marketing Expense for Events',                               
                         np.where(local_df['CATEGORIES'].str.contains('PROGRAM'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('PROGRAMS'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('BADGE'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('BADGES'),'Marketing Expense for Events',     
                         np.where(local_df['CATEGORIES'].str.contains('MAP'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('MAPS'),'Marketing Expense for Events',                                                          
                         np.where(local_df['CATEGORIES'].str.contains('ZIP TIES'),'Marketing Expense for Events',
                         np.where(local_df['CATEGORIES'].str.contains('ZIPTIES'),'Marketing Expense for Events',local_df['CATEGORIES']                  
                         ))))))))))))))))))))))))))))))))))))))))))


    parsing_report(local_df)      #Print out parsing report
    return local_df

def marketing_expense_gifts(expenses_df):

    print("")
    print("--------Parsing Marketing Expense for Gifts from Expense Items--------")
    print("")   
    
    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('GIFT'),'Marketing Expense for Gifts',
                         np.where(local_df['CATEGORIES'].str.contains('GIFTS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('LEIS'),'Marketing Expense for Gifts',                               
                         np.where(local_df['CATEGORIES'].str.contains('BASKET'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('GIFT BASKET'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('GIFT BASKETS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('FUNERAL BASKET'),'Marketing Expense for Gifts',                               
                         np.where(local_df['CATEGORIES'].str.contains('SYMPATHY'),'Marketing Expense for Gifts',                               
                         np.where(local_df['CATEGORIES'].str.contains('ARRANGEMENT'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('ARRANGEMENTS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('DONOR MEMENTOS'),'Marketing Expense for Gifts',   
                         np.where(local_df['CATEGORIES'].str.contains('MEMENTOS'),'Marketing Expense for Gifts',                                 
                         np.where(local_df['CATEGORIES'].str.contains('MEMENTO'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('MOMENTOS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('MOMENTO'),'Marketing Expense for Gifts',                                            
                         np.where(local_df['CATEGORIES'].str.contains('BOOK'),'Marketing Expense for Gifts',                               
                         np.where(local_df['CATEGORIES'].str.contains('CIGARS'),'Marketing Expense for Gifts',   
                         np.where(local_df['CATEGORIES'].str.contains('CIGAR'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('BOOK PURCHASE'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('WATCH'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('WATCHES'),'Marketing Expense for Gifts',      
                         np.where(local_df['CATEGORIES'].str.contains('BAG'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('BAGS'),'Marketing Expense for Gifts',                                
                         np.where(local_df['CATEGORIES'].str.contains('COINS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('CHALLENGE COINS'),'Marketing Expense for Gifts',  
                         np.where(local_df['CATEGORIES'].str.contains('ENGRAVING'),'Marketing Expense for Gifts',
                         np.where(local_df['CATEGORIES'].str.contains('ENGRAVINGS'),'Marketing Expense for Gifts',
                         np.where(local_df['CATEGORIES'].str.contains('DONOR ACKNOWLEDGEMENTS'),'Marketing Expense for Gifts',                               
                         np.where(local_df['CATEGORIES'].str.contains('ACKNOWLEDGEMENTS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('DONOR MEMENTOS'),'Marketing Expense for Gifts',   
                         np.where(local_df['CATEGORIES'].str.contains('DONOR MOMENTOS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('FLORAL'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('FLOWER'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('BOUQUET'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('ORNAMENT'),'Marketing Expense for Gifts',   
                         np.where(local_df['CATEGORIES'].str.contains('ORNAMENTS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('CHRISTMAS ORNAMENTS'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('HOLIDAY ORNAMENTS'),'Marketing Expense for Gifts',            
                         np.where(local_df['CATEGORIES'].str.contains('FLOWERS'),'Marketing Expense for Gifts',local_df['CATEGORIES']
                         )))))))))))))))))))))))))))))))))))))))                                                          

    parsing_report(local_df)      #Print out parsing report
    return local_df

def marketing_expense_outdoor_advertising(expenses_df):

    print("")
    print("--------Parsing Marketing Expense for Outdoor Advertising from Expense Items--------")
    print("")   
    
    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('BILLBOARD'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('BILL BOARD'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('BILL-BOARD'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('WRAP'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('WRAPS'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('STREETSIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('STREET SIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('STREET-SIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('YARDSIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('YARD SIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('YARD-SIGN'),'Marketing Expense for Outdoor Advertising',                                
                         np.where(local_df['CATEGORIES'].str.contains('ROADSIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('ROAD SIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('ROAD-SIGN'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('SIGNS'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('SIGN'),'Marketing Expense for Outdoor Advertising',local_df['CATEGORIES']
                         ))))))))))))))))                                                     

    parsing_report(local_df)      #Print out parsing report
    return local_df

def marketing_expense_digital_assets(expenses_df):

    print("")
    print("--------Parsing Marketing Expense for Digital Assets from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('WEBSITE'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('HOSTING'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('DOMAIN'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('APP'), 'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('MOBILE APP'), 'Marketing Expense for Digital Assets',                                
                         np.where(local_df['CATEGORIES'].str.contains('MOBILE APPLICATION'), 'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('APP'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('MOBLIE APP'),'Marketing Expense for Digital Assets',                              
                         np.where(local_df['CATEGORIES'].str.contains('DEVELOPMENT'), 'Marketing Expense for Digital Assets',                                
                         np.where(local_df['CATEGORIES'].str.contains('PROGRAMMING'), 'Marketing Expense for Digital Assets',         
                         np.where(local_df['CATEGORIES'].str.contains('CODING'), 'Marketing Expense for Digital Assets',                                  
                         np.where(local_df['CATEGORIES'].str.contains('WORDPRESS'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('WORD PRESS'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('HOST GATOR'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('HOSTGATOR'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('GO DADDY'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('GODADDY'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('ON-LINE STORE'),'Marketing Expense for Digital Assets',  
                         np.where(local_df['CATEGORIES'].str.contains('ON LINE STORE'),'Marketing Expense for Digital Assets', 
                         np.where(local_df['CATEGORIES'].str.contains('ONLINE STORE'),'Marketing Expense for Digital Assets', 
                         np.where(local_df['CATEGORIES'].str.contains('ON-LINE'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('ON LINE'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('ONLINE'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('WIX'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('WEB DEVELOPMENT'),'Marketing Expense for Digital Assets',
                         np.where(local_df['CATEGORIES'].str.contains('WEB'),'Marketing Expense for Digital Assets',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df    

def marketing_expense_digital_advertising(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Digital Advertising from Expense Items--------")
    print("")   
    
    local_df=expenses_df  

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('GOOGLE'),'Marketing Expense for Digital Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('BING'),'Marketing Expense for Digital Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('DIGITAL ADVERTISING'),'Marketing Expense for Digital Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('INTERNET MARKETING'),'Marketing Expense for Digital Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('SEO'),'Marketing Expense for Digital Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('SEARCH ENGINE OPTIMIZATION'),'Marketing Expense for Digital Advertising',                                 
                         np.where(local_df['CATEGORIES'].str.contains('PAGE BOOSTING'),'Marketing Expense for Digital Advertising',local_df['CATEGORIES']
                         )))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df  

def marketing_expense_bulk_email(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Bulk Email from Expense Items--------")
    print("")   
    
    local_df=expenses_df  

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('EMAIL'),'Marketing Expense for Bulk Email',  
                         np.where(local_df['CATEGORIES'].str.contains('E MAIL'),'Marketing Expense for Bulk Email',  
                         np.where(local_df['CATEGORIES'].str.contains('E-MAIL'),'Marketing Expense for Bulk Email',  
                         np.where(local_df['CATEGORIES'].str.contains('E-MARKETING'),'Marketing Expense for Bulk Email',  
                         np.where(local_df['CATEGORIES'].str.contains('ENEWSLETTER'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('E NEWSLETTER'),'Marketing Expense for Bulk Email', 
                         np.where(local_df['CATEGORIES'].str.contains('E-NEWSLETTER'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('EBLAST'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('EBLAST'),'Marketing Expense for Bulk Email',  
                         np.where(local_df['CATEGORIES'].str.contains('MAILCHIMP'),'Marketing Expense for Bulk Email', 
                         np.where(local_df['CATEGORIES'].str.contains('MAIL CHIMP'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('MAIL-CHIMP'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('STREAMSEND'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('STREAM SEND'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('STREAM-SEND'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('CONSTANTCONTACT'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('CONSTANT CONTACT'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('CONSTANT-CONTACT'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('GETRESPONSE'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('GET-RESPONSE'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('GET RESPONSE'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('VERTICALRESPONSE'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('VERTICAL RESPONSE'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('VERTICAL-RESPONSE'),'Marketing Expense for Bulk Email', 
                         np.where(local_df['CATEGORIES'].str.contains('ACTIVECAMPAIGN'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('ACTIVE CAMPAIGN'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('ACTIVE-CAMPAIGN'),'Marketing Expense for Bulk Email', 
                         np.where(local_df['CATEGORIES'].str.contains('BENCHMARK'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('BENCH MARK'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('BENCH-MARK'),'Marketing Expense for Bulk Email', 
                         np.where(local_df['CATEGORIES'].str.contains('ZOHO'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('ROBLY'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('DRIP'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('AWEBER'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('A WEBER'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('A-WEBER'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('INFUSIONSOFT'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('INFUSION SOFT'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('INFUSION-SOFT'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('DRIFT'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('WISHPOND'),'Marketing Expense for Bulk Email',                            
                         np.where(local_df['CATEGORIES'].str.contains('WISH POND'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('WISH-POND'),'Marketing Expense for Bulk Email',  
                         np.where(local_df['CATEGORIES'].str.contains('INTERCOM'),'Marketing Expense for Bulk Email',                                
                         np.where(local_df['CATEGORIES'].str.contains('INTER COM'),'Marketing Expense for Bulk Email',
                         np.where(local_df['CATEGORIES'].str.contains('INTER-COM'),'Marketing Expense for Bulk Email',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df 

def marketing_expense_social_media(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Social Media from Expense Items--------")
    print("")   
    
    local_df=expenses_df  

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('SOCIAL MEDIA'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('SOCIAL-MEDIA'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('SOCIAL NETWORKING'),'Marketing Expense for Social Media',                              
                         np.where(local_df['CATEGORIES'].str.contains('SOCIAL-NETWORKING'),'Marketing Expense for Social Media',                               
                         np.where(local_df['CATEGORIES'].str.contains('SOCIAL MARKETING'),'Marketing Expense for Social Media',                                                               
                         np.where(local_df['CATEGORIES'].str.contains('POST'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('POSTS'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('POSTING'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('POSTBOOST'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('POST BOOST'),'Marketing Expense for Social Media',                              
                         np.where(local_df['CATEGORIES'].str.contains('POST-BOOST'),'Marketing Expense for Social Media',                                 
                         np.where(local_df['CATEGORIES'].str.contains('FACEBOOK'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('TWITTER'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('LINKEDIN'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('LINKED IN'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('LINKED-IN'),'Marketing Expense for Social Media',                             
                         np.where(local_df['CATEGORIES'].str.contains('INSTAGRAM'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('SNAPCHAT'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('SNAP-CHAT'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('SNAP CHAT'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('PINTEREST'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('PININTEREST'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('PIN INTEREST'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('PIN-INTEREST'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('YOU-TUBE'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('YOU TUBE'),'Marketing Expense for Social Media',
                         np.where(local_df['CATEGORIES'].str.contains('YOUTUBE'),'Marketing Expense for Social Media',local_df['CATEGORIES']
                         )))))))))))))))))))))))))))
 

    parsing_report(local_df)      #Print out parsing report
    return local_df 


def marketing_expense_analytics(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Analytics from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('RESEARCH'),'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('MARKET RESEARCH'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('INTELLIGENCE'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('INTELIGENCE'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('INTEL'),'Marketing Expense for Analytics',  
                         np.where(local_df['CATEGORIES'].str.contains('BUSINESS INTELLIGENCE'),'Marketing Expense for Analytics',  
                         np.where(local_df['CATEGORIES'].str.contains('PREDICT'),'Marketing Expense for Analytics',                              
                         np.where(local_df['CATEGORIES'].str.contains('PREDICTIVE'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER BEHAVIOR'),'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('ANALYTICS'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('ANALYTICAL'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('SURVEY'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('ANALYTICS'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('ANALYTICAL'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('MODELING'),'Marketing Expense for Analytics', 
                         np.where(local_df['CATEGORIES'].str.contains('MODEL'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('ANALYSIS'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('POLLING'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('STATISTICS'),'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('STATISTICAL'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('DATA SCIENCE'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('POLL'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('POLLS'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('POLLING'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('STRATEGIC PLANNING'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('LIST'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('LISTS'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('RECORDS'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER CD'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER RECORDS'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER FILE'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER FILES'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER FILE ACCESS'),'Marketing Expense for Analytics',                                                         
                         np.where(local_df['CATEGORIES'].str.contains('DATABASE'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('DATA'),'Marketing Expense for Analytics',

                         #Analytics Software Listed Below                             

                         np.where(local_df['CATEGORIES'].str.contains('CRYSTAL BALL'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('CRYSTAL-BALL'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('CRYSTALBALL'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('SAS'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('JMP'), 'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('ENTERPRISEMINER'), 'Marketing Expense for Analytics',                              
                         np.where(local_df['CATEGORIES'].str.contains('ENTERPRISE-MINER'), 'Marketing Expense for Analytics',  
                         np.where(local_df['CATEGORIES'].str.contains('ENTERPRISE MINER'), 'Marketing Expense for Analytics',  
                         np.where(local_df['CATEGORIES'].str.contains('SPSS'), 'Marketing Expense for Analytics',                             
                         np.where(local_df['CATEGORIES'].str.contains('MATLAB'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('MAT LAB'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('MAT-LAB'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('STATISTICA'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('RSTUDIO'), 'Marketing Expense for Analytics',      
                         np.where(local_df['CATEGORIES'].str.contains('R STUDIO'), 'Marketing Expense for Analytics',     
                         np.where(local_df['CATEGORIES'].str.contains('R -STUDIO'), 'Marketing Expense for Analytics',    
                         np.where(local_df['CATEGORIES'].str.contains('PYTHON'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('ANACONDA'), 'Marketing Expense for Analytics',  
                         np.where(local_df['CATEGORIES'].str.contains('STATA'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('MINITAB'), 'Marketing Expense for Analytics',                             
                         np.where(local_df['CATEGORIES'].str.contains('EVIEWS'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('E VIEWS'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('E-VIEWS'), 'Marketing Expense for Analytics',       
                         np.where(local_df['CATEGORIES'].str.contains('ARCGIS'), 'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('ARC GIS'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('ARC-GIS'), 'Marketing Expense for Analytics', 
                         np.where(local_df['CATEGORIES'].str.contains('LISREL'), 'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('D3'), 'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('POWERBI'), 'Marketing Expense for Analytics',                              
                         np.where(local_df['CATEGORIES'].str.contains('POWER BI'), 'Marketing Expense for Analytics',                               
                         np.where(local_df['CATEGORIES'].str.contains('POWER-BI'), 'Marketing Expense for Analytics', 
                         np.where(local_df['CATEGORIES'].str.contains('EXCEL'), 'Marketing Expense for Analytics',    
                         np.where(local_df['CATEGORIES'].str.contains('APACHE'), 'Marketing Expense for Analytics', 
                         np.where(local_df['CATEGORIES'].str.contains('SPARK'), 'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('SAP'), 'Marketing Expense for Analytics',                              
                         np.where(local_df['CATEGORIES'].str.contains('RAPID MINER'), 'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('RAPIDMINER'),'Marketing Expense for Analytics',                               
                         np.where(local_df['CATEGORIES'].str.contains('RAPID-MINER'),'Marketing Expense for Analytics',                                
                         np.where(local_df['CATEGORIES'].str.contains('GOOGLE-ANALYTICS'),'Marketing Expense for Analytics', 
                         np.where(local_df['CATEGORIES'].str.contains('GOOGLE ANALYTICS'),'Marketing Expense for Analytics',                               
                         np.where(local_df['CATEGORIES'].str.contains('GOOGLEANALYTICS'),'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('OPENDX'),'Marketing Expense for Analytics',
                         np.where(local_df['CATEGORIES'].str.contains('OPEN DX'),'Marketing Expense for Analytics',  
                         np.where(local_df['CATEGORIES'].str.contains('OPEN-DX'),'Marketing Expense for Analytics',   
                         np.where(local_df['CATEGORIES'].str.contains('COGNOS'),'Marketing Expense for Analytics', 
                         np.where(local_df['CATEGORIES'].str.contains('H2O'), 'Marketing Expense for Analytics',    
                         np.where(local_df['CATEGORIES'].str.contains('H20'), 'Marketing Expense for Analytics',  
                         np.where(local_df['CATEGORIES'].str.contains('KNIME'),'Marketing Expense for Analytics',                                
                         np.where(local_df['CATEGORIES'].str.contains('KINIME'),'Marketing Expense for Analytics',                                  
                         np.where(local_df['CATEGORIES'].str.contains('CHARTS'), 'Marketing Expense for Analytics',local_df['CATEGORIES']   
                         )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
 
    parsing_report(local_df)      #Print out parsing report
    return local_df 

def cell_phone(expenses_df):
    print("")
    print("--------Parsing Expense for Cell Phones from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('BLACKBERRY'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('BLACKBERY'),'Cell Phones', 
                         np.where(local_df['CATEGORIES'].str.contains('BLACKBERRY'),'Cell Phones', 
                         np.where(local_df['CATEGORIES'].str.contains('BLACKBERRIES'),'Cell Phones', 
                         np.where(local_df['CATEGORIES'].str.contains('CELLULAR'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('CELL'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('MOBILE'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('MOBILE PHONE'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('WIRELESS'),'Cell Phones',   
                         np.where(local_df['CATEGORIES'].str.contains('IPHONE'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('I PHONE'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('I-PHONE'),'Cell Phones',                                 
                         np.where(local_df['CATEGORIES'].str.contains('AT&T'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('VERIZON'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('TMOBILE'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('T-MOBILE'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('T MOBILE'),'Cell Phones',
                         np.where(local_df['CATEGORIES'].str.contains('CRICKET'),'Cell Phones',local_df['CATEGORIES'] 
                         ))))))))))))))))))
    parsing_report(local_df)      #Print out parsing report
    return local_df    
                                  
def marketing_expense_phone_banking(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Phone Banking from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('PHONE BANKING'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('PHONE-BANKING'),'Marketing Expense for Phone Banking',                                  
                         np.where(local_df['CATEGORIES'].str.contains('TELEMARKETING'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('TELEMARKET'),'Marketing Expense for Phone Banking',   
                         np.where(local_df['CATEGORIES'].str.contains('TELEPHONE'),'Marketing Expense for Phone Banking',                                     
                         np.where(local_df['CATEGORIES'].str.contains('TELECOM'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('PHONE'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('PHONES'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('PHONING'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('PHONEING'),'Marketing Expense for Phone Banking',                        
                         np.where(local_df['CATEGORIES'].str.contains('DIALER'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('POWERDIALER'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('POWER-DIALER'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('POWER DIALER'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('LONG DISTANCE'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('PREDICTIVE DIALER'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('PREDICTIVE-DIALER'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('SOFT PHONE'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('IP'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('IP PHONE'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('VOIP'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('PHONE SERVICES'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('TELEPONE SERVICES'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('TELEPHONE SERVICES'),'Marketing Expense for Phone Banking',                                
                         np.where(local_df['CATEGORIES'].str.contains('ROBOCALLS'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('ROBO CALLS'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('ROBO-CALLS'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('ROBODIAL'),'Marketing Expense for Phone Banking',                               
                         np.where(local_df['CATEGORIES'].str.contains('ROBO DIAL'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('ROBO-DIAL'),'Marketing Expense for Phone Banking', 
                         np.where(local_df['CATEGORIES'].str.contains('ROBODIALS'),'Marketing Expense for Phone Banking',                               
                         np.where(local_df['CATEGORIES'].str.contains('ROBO DIALS'),'Marketing Expense for Phone Banking',                              
                         np.where(local_df['CATEGORIES'].str.contains('ROBO-DIALS'),'Marketing Expense for Phone Banking',                                       
                         np.where(local_df['CATEGORIES'].str.contains('CALL'),'Marketing Expense for Phone Banking',  
                         np.where(local_df['CATEGORIES'].str.contains('CALLERS'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('CALLS'),'Marketing Expense for Phone Banking',
                         np.where(local_df['CATEGORIES'].str.contains('CALLING'),'Marketing Expense for Phone Banking',local_df['CATEGORIES']
                         )))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df       


def marketing_expense_canvassing(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Phone Banking from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CANVASSING'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('CANVASING'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('DOOR'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('DOOR TO DOOR'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('DOOR-TO-DOOR'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('DOORKNOCKING'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('DOOR KNOCKING'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('DOOR-KNOCKING'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('CANVASS'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('CANVASSER'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('PAID CANVASSER'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('FIELD'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('WALKING'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('WALKERS'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('WALKER'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('WALK THE BLOCK'),'Marketing Expense for Canvassing',
                        #Get out the vote campaign is listed next -- consider a separate category -- Marketing (Get Out The Vote)                            

                         np.where(local_df['CATEGORIES'].str.contains('OUTREACH'),'Marketing Expense for Canvassing', 
                         np.where(local_df['CATEGORIES'].str.contains('OUT REACH'),'Marketing Expense for Canvassing', 
                         np.where(local_df['CATEGORIES'].str.contains('OURREACH'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER ACTIVATION'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER GUIDE'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('ABSENTEE VOTING'),'Marketing Expense for Canvassing',                              
                         np.where(local_df['CATEGORIES'].str.contains('ABSENTEE'),'Marketing Expense for Canvassing',  
                         np.where(local_df['CATEGORIES'].str.contains('VOTING'),'Marketing Expense for Canvassing',   
                         np.where(local_df['CATEGORIES'].str.contains('GRASSROOTS'),'Marketing Expense for Canvassing', 
                         np.where(local_df['CATEGORIES'].str.contains('GRASS ROOTS'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('GRASS-ROOTS'),'Marketing Expense for Canvassing',                
                         np.where(local_df['CATEGORIES'].str.contains('GET OUT THE VOTE'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('GET OUT THE VOTE EFFORTS'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('VOTOR CONTACT'),'Marketing Expense for Canvassing',   
                         np.where(local_df['CATEGORIES'].str.contains('VOTER CONTACT'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('VOTER ACTIVATION ACCESS'),'Marketing Expense for Canvassing',   
                         np.where(local_df['CATEGORIES'].str.contains('REGISTERING'),'Marketing Expense for Canvassing',
                         np.where(local_df['CATEGORIES'].str.contains('REGISTRATION'),'Marketing Expense for Canvassing',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df   

def marketing_expense_for_TV_and_radio(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for TV and Radio from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('COMMERCIAL'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('COMMERCIALS'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('MEDIA'),'Marketing Expense for TV and Radio',                            
                     np.where(local_df['CATEGORIES'].str.contains('TV'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('TELEVISION'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('RADIO'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('SPOT'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('AIRTIME'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('AIR TIME'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('AIR-TIME'),'Marketing Expense for TV and Radio',                              
                     np.where(local_df['CATEGORIES'].str.contains('AD'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('ADS'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('ADV'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('AD-BUY'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('AD BUY'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('ADVERT'),'Marketing Expense for TV and Radio',
                     np.where(local_df['CATEGORIES'].str.contains('ADVERTISING'),'Marketing Expense for TV and Radio',local_df['CATEGORIES']
                     )))))))))))))))))

    
    parsing_report(local_df)      #Print out parsing report
    return local_df   
    
def marketing_expense_public_relations(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Public Relations from Expense Items--------")
    print("")   
    
    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('PR'),'Marketing Expense for Public Relations',
                     np.where(local_df['CATEGORIES'].str.contains('PUBLIC RELATIONS'),'Marketing Expense for Public Relations', 
                     np.where(local_df['CATEGORIES'].str.contains('PUBLIC RELATION'),'Marketing Expense for Public Relations',   
                     np.where(local_df['CATEGORIES'].str.contains('PUBLICATION'),'Marketing Expense for Public Relations',                               
                     np.where(local_df['CATEGORIES'].str.contains('COMMUNICATION'),'Marketing Expense for Public Relations',
                     np.where(local_df['CATEGORIES'].str.contains('COMMUNICATIONS'),'Marketing Expense for Public Relations',
                     np.where(local_df['CATEGORIES'].str.contains('TRANSLATION'),'Marketing Expense for Public Relations',
                     np.where(local_df['CATEGORIES'].str.contains('CANDIDATE STATEMENT'),'Marketing Expense for Public Relations',local_df['CATEGORIES']
                    ))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df  

def marketing_expense_text_blasting(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Text Blasting from Expense Items--------")
    print("")  
    
    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('TEXT BLASTING'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('SMS BLASTING'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('IM BLASTING'),'Marketing Expense for Text Blasting',  
                         np.where(local_df['CATEGORIES'].str.contains('TEXT BLASTS'),'Marketing Expense for Text Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('SMS BLASTS'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('IM BLASTS'),'Marketing Expense for Text Blasting',                                                            
                         np.where(local_df['CATEGORIES'].str.contains('SMS'),'Marketing Expense for Text Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('IM'),'Marketing Expense for Text Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('IMING'),'Marketing Expense for Text Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('INSTANT MESSAGE'),'Marketing Expense for Text Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('INSTANT MESSAGING'),'Marketing Expense for Text Blasting',                                                                   
                         np.where(local_df['CATEGORIES'].str.contains('MSG'),'Marketing Expense for Text Blasting',  
                         np.where(local_df['CATEGORIES'].str.contains('MESSAGE'),'Marketing Expense for Text Blasting',
                         np.where(local_df['CATEGORIES'].str.contains('MESSAGING'),'Marketing Expense for Text Blasting',                                                                   
                         np.where(local_df['CATEGORIES'].str.contains('MESSAGES'),'Marketing Expense for Text Blasting',  
                         np.where(local_df['CATEGORIES'].str.contains('TEXT MESSAGE'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('TEXT MESSAGES'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('TEXT MESSAGING'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('TEXT'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('TEXTING'),'Marketing Expense for Text Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('TEXTING'),'Marketing Expense for Text Blasting',local_df['CATEGORIES']
                         )))))))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df  

def marketing_expense_fax_blasting(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Fax Blasting from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('FAX'),'Marketing Expense for Fax Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('FAXING'),'Marketing Expense for Fax Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('FAXES'),'Marketing Expense for Fax Blasting',  
                         np.where(local_df['CATEGORIES'].str.contains('BLAST FAX'),'Marketing Expense for Fax Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('BLAST FAXING'),'Marketing Expense for Fax Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('BLAST FAXES'),'Marketing Expense for Fax Blasting',                                
                         np.where(local_df['CATEGORIES'].str.contains('BLAST FAX CAMPAIGN'),'Marketing Expense for Fax Blasting',                                 
                         np.where(local_df['CATEGORIES'].str.contains('FAXING SERVICE'),'Marketing Expense for Fax Blasting',  
                         np.where(local_df['CATEGORIES'].str.contains('FAXING SERVICES'),'Marketing Expense for Fax Blasting', 
                         np.where(local_df['CATEGORIES'].str.contains('FAX SERVICES'),'Marketing Expense for Fax Blasting',local_df['CATEGORIES']
                                 ))))))))))

    
    parsing_report(local_df)      #Print out parsing report
    return local_df  

def marketing_expense_mail(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense for Direct Mail from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('MAIL SERVICES'), 'Marketing Expense for Mail',
                         np.where(local_df['CATEGORIES'].str.contains('MAIL'), 'Marketing Expense for Mail',          
                         np.where(local_df['CATEGORIES'].str.contains('ENVELOPES'), 'Marketing Expense for Mail',  
                         np.where(local_df['CATEGORIES'].str.contains('CARDS'), 'Marketing Expense for Mail',     
                         np.where(local_df['CATEGORIES'].str.contains('CARD'), 'Marketing Expense for Mail',     
                         np.where(local_df['CATEGORIES'].str.contains('SHIPPING'),'Marketing Expense for Mail', 
                         np.where(local_df['CATEGORIES'].str.contains('POSTAGE'),'Marketing Expense for Mail',
                         np.where(local_df['CATEGORIES'].str.contains('PACKAGE'),'Marketing Expense for Mail',
                         np.where(local_df['CATEGORIES'].str.contains('DELIVERY'),'Marketing Expense for Mail',
                         np.where(local_df['CATEGORIES'].str.contains('MAIL'),'Marketing Expense for Mail',
                         np.where(local_df['CATEGORIES'].str.contains('STAMP'),'Marketing Expense for Mail',local_df['CATEGORIES']
                         )))))))))))

    
    parsing_report(local_df)      #Print out parsing report
    return local_df  

def marketing_expense_other(expenses_df):
    
    print("")
    print("--------Parsing Marketing Expense Other from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('MARKETING'),'Marketing Expense Other', 
                         np.where(local_df['CATEGORIES'].str.contains('MARKETING'),'Marketing Expense Other',   
                         np.where(local_df['CATEGORIES'].str.contains('ELECTRONIC MARKETING'),'Marketing Expense Other', 
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN'),'Marketing Expense Other',                                               
                         np.where(local_df['CATEGORIES'].str.contains('MARKETING CAMPAIGNS'),'Marketing Expense Other',   
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGNS'),'Marketing Expense Other',  
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN'),'Marketing Expense Other',local_df['CATEGORIES']
                                 )))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df 


def beverages(expenses_df):
    
    print("")
    print("--------Parsing Beverages into Food and Beverages from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('BAR'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('CUP'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('CUPS'),'Food and Beverages',                               
                         np.where(local_df['CATEGORIES'].str.contains('SODA'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('JUICE'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('MILK'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('COFFEE'),'Food and Beverages',    
                         np.where(local_df['CATEGORIES'].str.contains('WATER'),'Food and Beverages',      
                         np.where(local_df['CATEGORIES'].str.contains('ICE'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('CHAMPAIGN'),'Food and Beverages',                        
                         np.where(local_df['CATEGORIES'].str.contains('WINE'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('BEER'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('BAR'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('COMFORT'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('WHISKEY'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('BURBON'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('JACK'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('BOOZE'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('ALCOHOL'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('SHOT'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('COOLER'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('HARD'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('CHAMPAGNE'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('TEQIULA'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('RUM'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('SAKE'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('ALE'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('GIN'),'Food and Beverages',   
                         np.where(local_df['CATEGORIES'].str.contains('GUINNESS'),'Food and Beverages',  
                         np.where(local_df['CATEGORIES'].str.contains('VODKA'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('KEG'),'Food and Beverages',   
                         np.where(local_df['CATEGORIES'].str.contains('DRINK'),'Food and Beverages',                              
                         np.where(local_df['CATEGORIES'].str.contains('DRINKS'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('BEVERAGE'),'Food and Beverages',    
                         np.where(local_df['CATEGORIES'].str.contains('BEVERAGES'),'Food and Beverages',    
                         np.where(local_df['CATEGORIES'].str.contains('REFRESHMENT'),'Food and Beverages',    
                         np.where(local_df['CATEGORIES'].str.contains('REFRESHMENTS'),'Food and Beverages',local_df['CATEGORIES']
                         )))))))))))))))))))))))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report 2
    return local_df  

def food(expenses_df):
    
    print("")
    print("--------Parsing Food into Food and Beverages from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CATERING'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('CATER'),'Food and Beverages',                                       
                         np.where(local_df['CATEGORIES'].str.contains('SNACK'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('SNACKS'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('PIZZA'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('GROCERIES'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('LUNCH'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('LUNCHEON'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('DINNER'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('DINING'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('SUB PURCHASES FOR MEMBERS'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('CATERER'),'Food and Beverages', 
                         np.where(local_df['CATEGORIES'].str.contains('GROCERY'),'Food and Beverages',       
                         np.where(local_df['CATEGORIES'].str.contains('BREAKFAST'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('FOOD'),'Food and Beverages',   
                         np.where(local_df['CATEGORIES'].str.contains('MEAL'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('MEALS'),'Food and Beverages',
                         np.where(local_df['CATEGORIES'].str.contains('BRUNCH'),'Food and Beverages',local_df['CATEGORIES']
                         ))))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report 3
    return local_df  



def air_travel(expenses_df):
    
    print("")
    print("--------Parsing Air Travel into Travel Expense from Expense Items--------")
    print("")  

    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('AIRLINE'),'Travel Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('AIRLINE TICKET'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('AIRLINE TICKETS'),'Travel Expense',     
                         np.where(local_df['CATEGORIES'].str.contains('BAGGAGE'),'Travel Expense',                                   
                         np.where(local_df['CATEGORIES'].str.contains('FLIGHT'),'Travel Expense',                             
                         np.where(local_df['CATEGORIES'].str.contains('FLIGHTS'),'Travel Expense',                                
                         np.where(local_df['CATEGORIES'].str.contains('PILOT'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('PILOT SERVICES'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CHARTER'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CHARTER FLIGHT'),'Travel Expense',                             
                         np.where(local_df['CATEGORIES'].str.contains('AIR TRAVEL'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AIRLINE TICKETS'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AIR'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AIRFARE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AIFARE'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('AIR FARE'),'Travel Expense',     
                         np.where(local_df['CATEGORIES'].str.contains('AIR-FARE'),'Travel Expense',     
                         np.where(local_df['CATEGORIES'].str.contains('PLANE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('PLANE TICKET'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AIRPLANE TICKET'),'Travel Expense',                              
                         np.where(local_df['CATEGORIES'].str.contains('PLANE TICKETS'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AIRPLANE TICKETS'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('AIRPLANE'),'Travel Expense',local_df['CATEGORIES']
                         )))))))))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report 4
    return local_df  

def accomodations(expenses_df):
    
    print("")
    print("--------Parsing Accomodations into Travel Expense from Expense Items--------")
    print("")  

    local_df=expenses_df 
 
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('LODGING'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('LODING'),'Travel Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('HOTEL'),'Travel Expense',    
                         np.where(local_df['CATEGORIES'].str.contains('HOUSING'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('MOTEL'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('MOTELS'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('BED'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ACCOMODAION'),'Travel Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('ACCOMODATION'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ACCOMMODATION'),'Travel Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('ACCOMMODATIONS'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ACCOMODATIONS'),'Travel Expense',local_df['CATEGORIES']
                         ))))))))))))

    parsing_report(local_df)      #Print out parsing report 5
    return local_df


def ground_transportation(expenses_df):
    
    print("")
    print("--------Parsing Ground Transportation into Travel Expense from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('TAXI'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CAB'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CAR'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('DRIVER'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('SHUTTLE'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('OIL CHANGE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('OIL-CHANGE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('OILCHANGE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CAR WASH'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CARWASH'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CABFARE'),'Travel Expense',     
                         np.where(local_df['CATEGORIES'].str.contains('CAB FARE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CAB FARES'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CAR SERVICE'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('CAR PAYMENT'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TOLL'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('TOLLS'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('TOLLWAY'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TOLL WAY'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TOLL-WAY'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('VAN'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TRAIN'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TRAIN TICKET'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TRAIN FARE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('TRAIN SERVICE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('RAIL FARE'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('RAIL'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('TOLLS'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('RIDESHARE'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('RIDE SHARE'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('VEHICLE'),'Travel Expense',     
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN VEHICLE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN VEHICLE: PAYMENT '),'Travel Expense',      
                         np.where(local_df['CATEGORIES'].str.contains('BUS'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('MILEAGE'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('MILEAGE REIMBURSEMENT'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('MILEAGE-REIMBURSEMENT'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('MILAGE'),'Travel Expense',                                   
                         np.where(local_df['CATEGORIES'].str.contains('PARKING'),'Travel Expense',     
                         np.where(local_df['CATEGORIES'].str.contains('AUTO'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('GAS'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('FUEL'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('PARK'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ZIPCAR'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ZIP CAR'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('ZIP-CAR'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('UBER'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('LYFT'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('LIFT'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CAR RENTAL'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CAR-RENTAL'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CAR RENT'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CAR-RENT'),'Travel Expense',           
                         np.where(local_df['CATEGORIES'].str.contains('RENTAL'),'Travel Expense',                            
                         np.where(local_df['CATEGORIES'].str.contains('RENTAL CAR'),'Travel Expense',                                 
                         np.where(local_df['CATEGORIES'].str.contains('RENTAL-CAR'),'Travel Expense',   
                         np.where(local_df['CATEGORIES'].str.contains('TIRE'),'Travel Expense',           
                         np.where(local_df['CATEGORIES'].str.contains('TIRES'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('SUBWAY'),'Travel Expense',           
                         np.where(local_df['CATEGORIES'].str.contains('PETROL'),'Travel Expense',                                   
                         np.where(local_df['CATEGORIES'].str.contains('INTERCHANGE'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('METROFARE'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('PARK'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('PARK'),'Travel Expense',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report 6
    return local_df

def travel_other(expenses_df):
    
    print("")
    print("--------Parsing Other Travel into Travel Expense from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('TRAVEL'),'Travel Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('TRAVL'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('PER DIEM'),'Travel Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('PERDIEM'),'Travel Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('PER-DIEM'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TRANSPORTATION'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('TRANSPORATION'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('TRANSPORTATON'),'Travel Expense',
                         np.where(local_df['CATEGORIES'].str.contains('FARES'),'Travel Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('TRVL'),'Travel Expense',local_df['CATEGORIES']
                         ))))))))))
    
    parsing_report(local_df)      #Print out parsing report 7
    return local_df    

def office_software(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses for Software from Expense Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('SOFTWARE'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('SOFTWARE LICENSE'), 'Office Expense for Software', 
                         np.where(local_df['CATEGORIES'].str.contains('TECHNOLOGY LICENSE'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('LICENSE'), 'Office Expense for Software',                
                         np.where(local_df['CATEGORIES'].str.contains('LICENSING'), 'Office Expense for Software',                              
                         np.where(local_df['CATEGORIES'].str.contains('CLOUD'), 'Office Expense for Software', 
                         np.where(local_df['CATEGORIES'].str.contains('WINDOWS'), 'Office Expense for Software',                              
                         np.where(local_df['CATEGORIES'].str.contains('MICROSOFT'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('WINDOWS'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('LINUX'), 'Office Expense for Software',      
                         np.where(local_df['CATEGORIES'].str.contains('UNIX'), 'Office Expense for Software',  
                         np.where(local_df['CATEGORIES'].str.contains('MICROSOFT'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('WINDOWS'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('SQL'),'Office Expense for Software',  
                         np.where(local_df['CATEGORIES'].str.contains('MYSQL'),'Office Expense for Software', 
                         np.where(local_df['CATEGORIES'].str.contains('MY SQL'),'Office Expense for Software',  
                         np.where(local_df['CATEGORIES'].str.contains('MY-SQL'),'Office Expense for Software',  
                         np.where(local_df['CATEGORIES'].str.contains('IBM'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('AMAZON'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('ORACLE'), 'Office Expense for Software',
                         np.where(local_df['CATEGORIES'].str.contains('LINUX'), 'Office Expense for Software',local_df['CATEGORIES']
                         )))))))))))))))))))))
  
    parsing_report(local_df)      #Print out parsing report 8
    return local_df  

def office_services(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses for Office Services--------")
    print("")  

    local_df=expenses_df    

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('COPYING'),'Office Expense for Office Services',     
                         np.where(local_df['CATEGORIES'].str.contains('COPIES'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('PEST'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE SERVICE'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE SERVICES'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('COPIER SERVICE'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('COPIER SERVICES'),'Office Expense for Office Services',  
                         np.where(local_df['CATEGORIES'].str.contains('DELIVERY'),'Office Expense for Office Services',                               
                         np.where(local_df['CATEGORIES'].str.contains('RECYCLING'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('RECYCLING SVC'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('OUTSIDE SVCS'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('LAUNDRY'),'Office Expense for Office Services',                                                                                                    
                         np.where(local_df['CATEGORIES'].str.contains('FEDEX'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('COURRIER'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('COURIER'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('MAID'),'Office Expense for Office Services',   
                         np.where(local_df['CATEGORIES'].str.contains('MAIDS'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('ADMIN'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('SERVICE'),'Office Expense for Office Services',  
                         np.where(local_df['CATEGORIES'].str.contains('CLEANING'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('CLEANING'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('CLEANING SERVICE'),'Office Expense for Office Services',                                   
                         np.where(local_df['CATEGORIES'].str.contains('MAID SERVICE'),'Office Expense for Office Services',                                
                         np.where(local_df['CATEGORIES'].str.contains('TRASH SERVICE'),'Office Expense for Office Services',                                
                         np.where(local_df['CATEGORIES'].str.contains('REFUSE SERVICE'),'Office Expense for Office Services',    
                         np.where(local_df['CATEGORIES'].str.contains('COPIER SERVICES'),'Office Expense for Office Services',                              
                         np.where(local_df['CATEGORIES'].str.contains('CLEANING SERVICES'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('RECYCLING SERVICE'),'Office Expense for Office Services',                               
                         np.where(local_df['CATEGORIES'].str.contains('MAID SERVICES'),'Office Expense for Office Services',                                
                         np.where(local_df['CATEGORIES'].str.contains('TRASH SERVICES'),'Office Expense for Office Services',    
                         np.where(local_df['CATEGORIES'].str.contains('TRASH'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('WASTE REMOVAL'),'Office Expense for Office Services',                                   
                         np.where(local_df['CATEGORIES'].str.contains('REFUSE SERVICES'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('MOVING SERVICES'),'Office Expense for Office Services',     
                         np.where(local_df['CATEGORIES'].str.contains('MOVING SERVICE'),'Office Expense for Office Services',   
                         np.where(local_df['CATEGORIES'].str.contains('MAINTENANCE'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('DELIVERIES'),'Office Expense for Office Services',                              
                         np.where(local_df['CATEGORIES'].str.contains('RECYCLE REMOVAL'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('GARBAGE AND RECYCLING'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('SHREDDING'),'Office Expense for Office Services',  
                         np.where(local_df['CATEGORIES'].str.contains('CLEANING'),'Office Expense for Office Services',
                         np.where(local_df['CATEGORIES'].str.contains('SNOW REMOVAL'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('REFUSE'),'Office Expense for Office Services',                                
                         np.where(local_df['CATEGORIES'].str.contains('TRASH'),'Office Expense for Office Services',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))))))))))))))))   
    
    parsing_report(local_df)      #Print out parsing report 9
    return local_df      

def office_supplies(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses for Supplies--------")
    print("")  

    local_df=expenses_df    

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('OFFICE SUPPLIES'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE SUPPLY'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE SUPPLES'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('BOX'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('BOXES'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('BOXS'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('SUPPLES'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('SUPPLIES'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('STATIONARY'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('STATIONERY'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('PAPER'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('TONER'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('BATTERIES'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('CHECKS'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('CHECK ORDER'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('CHECKBOOK'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('CHECKBOOKS'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('CHECK BOOK'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('CHECK BOOKS'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('CHECK STOCK'),'Office Expense for Supplies',   
                         np.where(local_df['CATEGORIES'].str.contains('CHECKSTOCK'),'Office Expense for Supplies',   
                         np.where(local_df['CATEGORIES'].str.contains('CLIPBOARD'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('CLIPBOARDS'),'Office Expense for Supplies',                             
                         np.where(local_df['CATEGORIES'].str.contains('DOCUMENT'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('DOCUMENTS'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('PAPER'),'Office Expense for Supplies',                              
                         np.where(local_df['CATEGORIES'].str.contains('FLASH DRIVE'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('FLASH DRIVES'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('FLASHDRIVE'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('FLASHDRIVES'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('FRAMING'),'Office Expense for Supplies',      
                         np.where(local_df['CATEGORIES'].str.contains('HOLE PUNCH'),'Office Expense for Supplies',                           
                         np.where(local_df['CATEGORIES'].str.contains('ENVELOPES'), 'Office Expense for Supplies',                               
                         np.where(local_df['CATEGORIES'].str.contains('KEY'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('KEYS'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('INK'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('CARTRIDGE'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('CARTRIDGES'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('LABEL'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('LABELS'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('FRAME'),'Office Expense for Supplies',                                
                         np.where(local_df['CATEGORIES'].str.contains('FRAMES'),'Office Expense for Supplies',                                
                         np.where(local_df['CATEGORIES'].str.contains('FRAMING'),'Office Expense for Supplies',      
                         np.where(local_df['CATEGORIES'].str.contains('FOLDER'),'Office Expense for Supplies',                                
                         np.where(local_df['CATEGORIES'].str.contains('FOLDERS'),'Office Expense for Supplies',                                  
                         np.where(local_df['CATEGORIES'].str.contains('CLIPBOARD'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('COPIES'),'Office Expense for Supplies',                                      
                         np.where(local_df['CATEGORIES'].str.contains('ENVELOPES'), 'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('PEN'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('PENS'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('PENCIL'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('PENCILS'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('MARKER'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('MARKERS'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('TAPE'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('MAGNETS'),'Office Expense for Supplies',                              
                         np.where(local_df['CATEGORIES'].str.contains('NOTES'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('BOARD'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('STAPLER'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('STAPLERS'),'Office Expense for Supplies',  
                         np.where(local_df['CATEGORIES'].str.contains('STAPLES'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('RUBBER BANDS'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('PAPER CLIP'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('PAPER CLIPS'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE SUPLIES'),'Office Expense for Supplies',
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE SUPPPLIES'),'Office Expense for Supplies',                     
                         np.where(local_df['CATEGORIES'].str.contains('CLIP'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('CLIPS'),'Office Expense for Supplies',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df  

def office_IT(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses for IT Services--------")
    print("")  

    local_df=expenses_df   

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('DISH'),'Office Expense for IT Services',
                         np.where(local_df['CATEGORIES'].str.contains('TECH SUPPORT'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('TECHNICAL SERVICE'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('TECHNICAL SERVICES'),'Office Expense for IT Services',
                         np.where(local_df['CATEGORIES'].str.contains('CONFERENCING SERVICES'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('CONFERENCING'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('CONFERENCING SERVICES'),'Office Expense for IT Services',                          
                         np.where(local_df['CATEGORIES'].str.contains('TELETOWNHALL'),'Office Expense for IT Services',                              
                         np.where(local_df['CATEGORIES'].str.contains('ISP'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('DSL'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('INTERNET SERVICE PROVIDER'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('INTERNET SERVICE PROVIDOR'),'Office Expense for IT Services',                                              
                         np.where(local_df['CATEGORIES'].str.contains('HOTSPOT'),'Office Expense for IT Services',                                      
                         np.where(local_df['CATEGORIES'].str.contains('NETWORK SERVICES'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('INFORMATION'),'Office Expense for IT Services',                     
                         np.where(local_df['CATEGORIES'].str.contains('TELECOMMUNCATIONS'),'Office Expense for IT Services',  
                         np.where(local_df['CATEGORIES'].str.contains('INFORMATION TECHNOLOGY'),'Office Expense for IT Services',                       
                         np.where(local_df['CATEGORIES'].str.contains('TELECONFERENCE'),'Office Expense for IT Services',                                
                         np.where(local_df['CATEGORIES'].str.contains('TELECONFERENCING'),'Office Expense for IT Services',                             
                         np.where(local_df['CATEGORIES'].str.contains('TELECOMMUNCATIONS'),'Office Expense for IT Services',  
                         np.where(local_df['CATEGORIES'].str.contains('INFORMATION TECHNOLOGY'),'Office Expense for IT Services',                              
                         np.where(local_df['CATEGORIES'].str.contains('TECH'),'Office Expense for IT Services',                              
                         np.where(local_df['CATEGORIES'].str.contains('CIRECTV'),'Office Expense for IT Services',                              
                         np.where(local_df['CATEGORIES'].str.contains('CIREC TV'),'Office Expense for IT Services',      
                         np.where(local_df['CATEGORIES'].str.contains('CIRECT TV'),'Office Expense for IT Services',
                         np.where(local_df['CATEGORIES'].str.contains('UVERSE'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('UVERSE'),'Office Expense for IT Services',   
                         np.where(local_df['CATEGORIES'].str.contains('U-VERSE'),'Office Expense for IT Services',    
                         np.where(local_df['CATEGORIES'].str.contains('U VERSE'),'Office Expense for IT Services',
                         np.where(local_df['CATEGORIES'].str.contains('IT'),'Office Expense for IT Services',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df  


def office_network_computer_equipment(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses for Network and Computer Equipment--------")
    print("")  

    local_df=expenses_df   

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('INFRASTRUCTURE'),'Office Expense for Network and Computer Equipment',
                         np.where(local_df['CATEGORIES'].str.contains('WIFI'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('CABLE'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('CABLES'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('FIBER'),'Office Expense for Network and Computer Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('COMPUTERS'),'Office Expense for Network and Computer Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('COMPUTER'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('CHROMECAST'),'Office Expense for Network and Computer Equipment',                               
                         np.where(local_df['CATEGORIES'].str.contains('CPU'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('PRINTER'),'Office Expense for Network and Computer Equipment',
                         np.where(local_df['CATEGORIES'].str.contains('PRINTERS'),'Office Expense for Network and Computer Equipment',
                         np.where(local_df['CATEGORIES'].str.contains('ROUTER'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('ROUTERS'),'Office Expense for Network and Computer Equipment',           
                         np.where(local_df['CATEGORIES'].str.contains('MODEM'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('MODEMS'),'Office Expense for Network and Computer Equipment',                              
                         np.where(local_df['CATEGORIES'].str.contains('MONITOR'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('MONITORS'),'Office Expense for Network and Computer Equipment',                              
                         np.where(local_df['CATEGORIES'].str.contains('LAPTOP'),'Office Expense for Network and Computer Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('LAP TOP'),'Office Expense for Network and Computer Equipment',                      
                         np.where(local_df['CATEGORIES'].str.contains('SERVERS & TECH INFRASTRUCTURE'),'Office Expense for Network and Computer Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('SERVERS'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('SERVER'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('GATEWAY'),'Office Expense for Network and Computer Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('EQUIPMENT'),'Office Expense for Network and Computer Equipment',local_df['CATEGORIES']
                         ))))))))))))))))))))))))       

    parsing_report(local_df)      #Print out parsing report
    return local_df  



def office_furniture_equipment(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses for Furniture and Equipment--------")
    print("")  

    local_df=expenses_df   

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('FURNITURE'),'Office Expense For Furniture and Equipment',
                         np.where(local_df['CATEGORIES'].str.contains('CHAIR'),'Office Expense For Furniture and Equipment',      
                         np.where(local_df['CATEGORIES'].str.contains('CHAIRS'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('TABLE'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('TABLES'),'Office Expense For Furniture and Equipment',                                
                         np.where(local_df['CATEGORIES'].str.contains('DESK'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('DESKS'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('SOFA'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('SOFAS'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('COUCH'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('COUCHES'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('STAND'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('STANDS'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('BOARD'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('BOARDS'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('STOOL'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('STOOLS'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('BENCH'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('BENCHES'),'Office Expense For Furniture and Equipment',                               
                         np.where(local_df['CATEGORIES'].str.contains('WATER COOLER'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('WATER COOLERS'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('COFFEE MAKER'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('COFEEE MAKERS'),'Office Expense For Furniture and Equipment',                               
                         np.where(local_df['CATEGORIES'].str.contains('TELEVISION'),'Office Expense For Furniture and Equipment',  
                         np.where(local_df['CATEGORIES'].str.contains('TELEVISIONS'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('COPIER'),'Office Expense For Furniture and Equipment',
                         np.where(local_df['CATEGORIES'].str.contains('COPIERS'),'Office Expense For Furniture and Equipment',      
                         np.where(local_df['CATEGORIES'].str.contains('COPIER'),'Office Expense For Furniture and Equipment',
                         np.where(local_df['CATEGORIES'].str.contains('ALARM'),'Office Expense For Furniture and Equipment',                               
                         np.where(local_df['CATEGORIES'].str.contains('ALARMS'),'Office Expense For Furniture and Equipment',local_df['CATEGORIES']
                         ))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df  

def office_rent_and_utilities(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses for Rent and Utilities--------")
    print("")  

    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('RENT'),'Office Expense for Rent and Utilities', 
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE CONSTRUCTION'),'Office Expense for Rent and Utilities',                               
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE SPACE'),'Office Expense for Rent and Utilities',                              
                         np.where(local_df['CATEGORIES'].str.contains('MORTGAGE'),'Office Expense for Rent and Utilities', 
                         np.where(local_df['CATEGORIES'].str.contains('BUILDING'),'Office Expense for Rent and Utilities',                                                            
                         np.where(local_df['CATEGORIES'].str.contains('LEASE'),'Office Expense for Rent and Utilities', 
                         np.where(local_df['CATEGORIES'].str.contains('STORAGE'),'Office Expense for Rent and Utilities',                              
                         np.where(local_df['CATEGORIES'].str.contains('MEETING ROOM'),'Office Expense for Rent and Utilities',                              
                         np.where(local_df['CATEGORIES'].str.contains('WAREHOUSE'),'Office Expense for Rent and Utilities',             
                         np.where(local_df['CATEGORIES'].str.contains('SEWAGE'),'Office Expense for Rent and Utilities', 
                         np.where(local_df['CATEGORIES'].str.contains('UTILITIES'),'Office Expense for Rent and Utilities',
                         np.where(local_df['CATEGORIES'].str.contains('UTILTIES'),'Office Expense for Rent and Utilities',                              
                         np.where(local_df['CATEGORIES'].str.contains('ELECTRIC'),'Office Expense for Rent and Utilities',
                         np.where(local_df['CATEGORIES'].str.contains('ELECTRICITY'),'Office Expense for Rent and Utilities',
                         np.where(local_df['CATEGORIES'].str.contains('ELECTRIC BILL'),'Office Expense for Rent and Utilities', 
                         np.where(local_df['CATEGORIES'].str.contains('ENERGY BILL'),'Office Expense for Rent and Utilities', 
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE UTILTIES'),'Office Expense for Rent and Utilities',
                         np.where(local_df['CATEGORIES'].str.contains('WATER'),'Office Expense for Rent and Utilities',local_df['CATEGORIES']
                         ))))))))))))))))))


    parsing_report(local_df)      #Print out parsing report
    return local_df  

def office_other(expenses_df):
    
    print("")
    print("--------Parsing Office Expenses Other--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('OFFICE YOGA'),'Office Expense General', 
                         np.where(local_df['CATEGORIES'].str.contains('MOVING'),'Office Expense General',
                         np.where(local_df['CATEGORIES'].str.contains('FREIGHT'),'Office Expense General', 
                         np.where(local_df['CATEGORIES'].str.contains('OFFICE COSTS'),'Office Expense General', 
                         np.where(local_df['CATEGORIES'].str.contains('OPERATING EXPENSE'),'Office Expense General', 
                         np.where(local_df['CATEGORIES'].str.contains('OPERATING EXPENSES'),'Office Expense General',local_df['CATEGORIES'] 
                         ))))))
 
    parsing_report(local_df)      #Print out parsing report
    return local_df  

def tax_expense(expenses_df):
    
    print("")
    print("--------Parsing Tax Expenses from Expense Items--------")
    print("")   
    
    local_df=expenses_df

    local_df['CATEGORIES'] = np.where(local_df['CATEGORIES'].str.contains('UNEMPLOYMENT'),'Tax Expense', 
                       np.where(local_df['CATEGORIES'].str.contains('FICA'),'Tax Expense',
                       np.where(local_df['CATEGORIES'].str.contains('FUTA'),'Tax Expense',
                       np.where(local_df['CATEGORIES'].str.contains('FEDERAL INCOME TAX'),'Tax Expense',                             
                       np.where(local_df['CATEGORIES'].str.contains('TAX'),'Tax Expense',                
                       np.where(local_df['CATEGORIES'].str.contains('TAXES'),'Tax Expense',     
                       np.where(local_df['CATEGORIES'].str.contains('INTERNAL REVENUE SERVICE'),'Tax Expense', 
                       np.where(local_df['CATEGORIES'].str.contains('INTERNAL REVENUE SERVICES'),'Tax Expense', 
                       np.where(local_df['CATEGORIES'].str.contains('IRS'),'Tax Expense', 
                       np.where(local_df['CATEGORIES'].str.contains('TREASURY'),'Tax Expense', 
                       np.where(local_df['CATEGORIES'].str.contains('UNITED STATES TREASURY'),'Tax Expense', 
                       np.where(local_df['CATEGORIES'].str.contains('US TREASURY'),'Tax Expense',
                       np.where(local_df['CATEGORIES'].str.contains('TREASURY DEPARTMENT'),'Tax Expense',
                       np.where(local_df['CATEGORIES'].str.contains('STATE W/H'),'Tax Expense', 
                       np.where(local_df['CATEGORIES'].str.contains('FEDERAL W/H'),'Tax Expense',     
                       np.where(local_df['CATEGORIES'].str.contains('W/H'),'Tax Expense',                                      
                       np.where(local_df['CATEGORIES'].str.contains('DEPARTMENT OF THE TREASURY'),'Tax Expense',local_df['CATEGORIES']
                       )))))))))))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df


def in_kind_contributions(expenses_df):
    
    print("")
    print("--------Parsing In Kind Contributions--------")
    print("")  

    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('IN-KIND'),'In Kind Contributions', 
                         np.where(local_df['CATEGORIES'].str.contains('INKIND'),'In Kind Contributions',  
                         np.where(local_df['CATEGORIES'].str.contains('IN KIND'),'In Kind Contributions',   
                         np.where(local_df['CATEGORIES'].str.contains('KIND'),'In Kind Contributions',local_df['CATEGORIES']
                         )))) 

    parsing_report(local_df)      #Print out parsing report
    return local_df  

def reimbursements(expenses_df):
    
    print("")
    print("--------Parsing Reimbursements--------")
    print("")  

    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('REIMBURSEMENT'),'Reimbursements',
                         np.where(local_df['CATEGORIES'].str.contains('REFUND'),'Reimbursements',   
                         np.where(local_df['CATEGORIES'].str.contains('REFUNDS'),'Reimbursements', 
                         np.where(local_df['CATEGORIES'].str.contains('DISGORGEMENT'),'Reimbursements',   
                         np.where(local_df['CATEGORIES'].str.contains('FRAUD'),'Reimbursements',                               
                         np.where(local_df['CATEGORIES'].str.contains('REMUNERATION'),'Reimbursements',local_df['CATEGORIES']              
                                 ))))))
  
    parsing_report(local_df)      #Print out parsing report
    return local_df  


def donation_expense(expenses_df):
    
    print("")
    print("--------Parsing Donation Expenses from Expense Items--------")
    print("")   
    
    local_df=expenses_df    

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CONTRIBUTION'),'Donation Expense',
                         np.where(local_df['CATEGORIES'].str.contains('CONTRIBUTION'),'Donation Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('CONTRIBTION'),'Donation Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('CONTRIBTIONS'),'Donation Expense', 
                         np.where(local_df['CATEGORIES'].str.contains('DONATION'),'Donation Expense',
                         np.where(local_df['CATEGORIES'].str.contains('DONATIONS'),'Donation Expense',local_df['CATEGORIES']
                         ))))))        

    parsing_report(local_df)      #Print out parsing report
    return local_df

def transaction_fees(expenses_df):
    
    print("")
    print("--------Parsing Transaction Fees from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CREDIT CARD FEES'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT CARD FEE'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT CARD PROCESSING FEES'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT CARD PROCESSING FEE  '),'Credit Card PayPal and Transaction Fees',            
                         np.where(local_df['CATEGORIES'].str.contains('MERCHANT FEE'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('MERCHANT FEES'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('SERVICE FEE'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('SERVICE FEES'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT FEE'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT FEES'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('FRST BK MRCH SVC DISCT'),'Other Fees and Interest',  
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT CARD CHARGE'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT CARD CHARGES'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('CREDIT CHARGE'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('TRANSACTION FEE'),'Credit Card PayPal and Transaction Fees',
                         np.where(local_df['CATEGORIES'].str.contains('TRANSACTION FEES'),'Credit Card PayPal and Transaction Fees', local_df['CATEGORIES']
                                 ))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df



def bank_fees(expenses_df):
    
    print("")
    print("--------Parsing Bank Fees from Expense Items--------")
    print("")   
    
    local_df=expenses_df  

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('BANK FEES'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('WIRE FEE'),'Bank Fees',   
                         np.where(local_df['CATEGORIES'].str.contains('WIRE SERVICE'),'Bank Fees',                               
                         np.where(local_df['CATEGORIES'].str.contains('WIRE SERVICES FEE'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('WIRE SERVICES'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('WIRE SERVICES FEE'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('WIRE TRANSFER SERVICE'),'Bank Fees',                              
                         np.where(local_df['CATEGORIES'].str.contains('WIRE TRANSFER FEE'),'Bank Fees',                              
                         np.where(local_df['CATEGORIES'].str.contains('WIRE TRANSFER FEES'),'Bank Fees',                              
                         np.where(local_df['CATEGORIES'].str.contains('WIRE SERVICE'),'Bank Fees',                              
                         np.where(local_df['CATEGORIES'].str.contains('BANK SERVICE FEE'),'Bank Fees',                                     
                         np.where(local_df['CATEGORIES'].str.contains('BANK SERVICES FEE'),'Bank Fees',                                 
                         np.where(local_df['CATEGORIES'].str.contains('BANK SERVICES'),'Bank Fees',                                          
                         np.where(local_df['CATEGORIES'].str.contains('BANK FEE'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('BANKING FEE'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('BANKING FEES'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('BANK CHARGE'),'Bank Fees',   
                         np.where(local_df['CATEGORIES'].str.contains('BANK CHARGES'),'Bank Fees',
                         np.where(local_df['CATEGORIES'].str.contains('BANK SERVICES CHARGE'),'Bank Fees',   
                         np.where(local_df['CATEGORIES'].str.contains('BANK SERVICE CHARGE'),'Bank Fees', 
                         np.where(local_df['CATEGORIES'].str.contains('BANK SERVICE CHARGES'),'Bank Fees',  
                         np.where(local_df['CATEGORIES'].str.contains('BANK'),'Bank Fees',local_df['CATEGORIES']
                                 ))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df

def petty_cash(expenses_df):
    
    print("")
    print("--------Parsing Petty Cash from Expense Items--------")
    print("")   
    
    local_df=expenses_df  
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('PETTY CASH'),'Petty Cash',
                         np.where(local_df['CATEGORIES'].str.contains('REPLENISH PETTY CASH'),'Petty Cash',                                            
                         np.where(local_df['CATEGORIES'].str.contains('PETTY CASH'),'Petty Cash',local_df['CATEGORIES'] 
                                 )))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df   


    
def other_fees(expenses_df):
    
    print("")
    print("--------Parsing Other Fees and Interest from Expense Items--------")
    print("")   
    
    local_df=expenses_df     
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('CHARGE'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('CHARGES'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('CHECK VOIDED'),'Other Fees and Interest',   
                         np.where(local_df['CATEGORIES'].str.contains('LOST CHECK'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('CASH BACK REWARDS'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('MERCHANDISE FULFILLMENT'),'Other Fees and Interest', 
                         np.where(local_df['CATEGORIES'].str.contains('FULFILLMENT'),'Other Fees and Interest',   
                         np.where(local_df['CATEGORIES'].str.contains('MERCHANT DISCOUNT'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('MERCHANT SERVICES'),'Other Fees and Interest', 
                         np.where(local_df['CATEGORIES'].str.contains('FULFILLMENT'),'Other Fees and Interest',                            
                         np.where(local_df['CATEGORIES'].str.contains('SERVICE CHARGE'),'Other Fees and Interest', 
                         np.where(local_df['CATEGORIES'].str.contains('SERVICE CHARGES'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('REGISTRATION FEE'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('REGISTRATION FEES'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('RETURNED CHECK'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('LOST CHECK'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('MERCHANT INTERCHANGE'),'Other Fees and Interest',                             
                         np.where(local_df['CATEGORIES'].str.contains('VOID CHECK'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('VOIDED CHECK'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('REBATE'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('REBATES'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('RETURN'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('ESCROW SERVICES'),'Other Fees and Interest',   
                         np.where(local_df['CATEGORIES'].str.contains('RETURN'),'Other Fees and Interest',                              
                         np.where(local_df['CATEGORIES'].str.contains('ACH'),'Other Fees and Interest',                                
                         np.where(local_df['CATEGORIES'].str.contains('UNCASHED CHECK'),'Other Fees and Interest',  
                         np.where(local_df['CATEGORIES'].str.contains('PAYMENT'),'Other Fees and Interest',    
                         np.where(local_df['CATEGORIES'].str.contains('CC DAILY'),'Other Fees and Interest',                        
                         np.where(local_df['CATEGORIES'].str.contains('ESCROW'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('COLLECTIONS'),'Other Fees and Interest',                              
                         np.where(local_df['CATEGORIES'].str.contains('POINTS REBATE'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('INTEREST'),'Other Fees and Interest',                                           
                         np.where(local_df['CATEGORIES'].str.contains('FILING FEE'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('FILING FEES'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('TRANSFER'),'Other Fees and Interest',   
                         np.where(local_df['CATEGORIES'].str.contains('GATEWAY BILLING'),'Other Fees and Interest',
                         np.where(local_df['CATEGORIES'].str.contains('DEBT FORGIVEN'),'Other Fees and Interest',                            
                         np.where(local_df['CATEGORIES'].str.contains('DEBT REDUCTION'),'Other Fees and Interest',  
                         np.where(local_df['CATEGORIES'].str.contains('FEE'),'Other Fees and Interest',        
                         np.where(local_df['CATEGORIES'].str.contains('FEES'),'Other Fees and Interest',                                               
                         np.where(local_df['CATEGORIES'].str.contains('Other Fees'),'Other Fees and Interest',local_df['CATEGORIES'] 
                                 )))))))))))))))))))))))))))))))))))))))))   
    
    parsing_report(local_df)      #Print out parsing report
    return local_df        
    

def obscurely_marked(expenses_df):
    
    print("")
    print("--------Parsing Obscurely Marked Items--------")
    print("")  

    local_df=expenses_df 

    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('MEMO'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('001'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('004'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('006'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('15'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('15z'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('15Z'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('20c'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('20C'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('SC'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('REFERENCE'),'Obscurely Marked Items',                                   
                         np.where(local_df['CATEGORIES'].str.contains('APT. A'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('CHECK'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('DEBT'),'Obscurely Marked Items',                             
                         np.where(local_df['CATEGORIES'].str.contains('EARMARK'),'Obscurely Marked Items',                              
                         np.where(local_df['CATEGORIES'].str.contains('EARMARKS'),'Obscurely Marked Items',                                  
                         np.where(local_df['CATEGORIES'].str.contains('SEE DETAIL'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('SCHEDULING'),'Obscurely Marked Items',                              
                         np.where(local_df['CATEGORIES'].str.contains('UNKNOWN'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('VARIOUS'),'Obscurely Marked Items',                                                              
                         np.where(local_df['CATEGORIES'].str.contains('MEMOS'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('MEMMO'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('SEE BELOW'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('SEE SCHEDULE'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('SEE LIST'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('SEE MEMO'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('SEE CODE'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('CODE'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('ISSUED IN ERROR'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('INVESTMENT LOSS'),'Obscurely Marked Items',                                                             
                         np.where(local_df['CATEGORIES'].str.contains('OPERATING COST'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('MONTHLY BILL'),'Obscurely Marked Items',                              
                         np.where(local_df['CATEGORIES'].str.contains('RECEIVABLE'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('LOAN PAYMENT'),'Obscurely Marked Items',                               
                         np.where(local_df['CATEGORIES'].str.contains('VSG619VVKV3'),'Obscurely Marked Items',                             
                         np.where(local_df['CATEGORIES'].str.contains('DISCOUNT'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('LOAN PAYMENT'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('DISCOUNT'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('GENERAL'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('OPERATING'),'Obscurely Marked Items',  
                         np.where(local_df['CATEGORIES'].str.contains('REV SHARE DEDUCTION'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('CAMPAIGN FUNDS'),'Obscurely Marked Items',                                                                           
                         np.where(local_df['CATEGORIES'].str.contains('FINE'),'Obscurely Marked Items',                       
                         np.where(local_df['CATEGORIES'].str.contains('RECEIVABLE'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('RECEIVABLES'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('LOAN PAYMENT'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('DISCOUNT'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('OUT-OF-POCKET'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('GENERAL FUND'),'Obscurely Marked Items',   
                         np.where(local_df['CATEGORIES'].str.contains('UNCATEGORIZED'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('REPLENISHMENT'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('MISC EXP'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('REPLENISH'),'Obscurely Marked Items',                               
                         np.where(local_df['CATEGORIES'].str.contains('SETTLEMENT'),'Obscurely Marked Items',                                
                         np.where(local_df['CATEGORIES'].str.contains('ALLOCATED TO LN 24'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('ALLOCATED TO LN 24'),'Obscurely Marked Items',       
                         np.where(local_df['CATEGORIES'].str.contains('ALLOCATE TO LN 24'),'Obscurely Marked Items',                               
                         np.where(local_df['CATEGORIES'].str.contains('LN 24'),'Obscurely Marked Items',    
                         np.where(local_df['CATEGORIES'].str.contains('LINE 24'),'Obscurely Marked Items',                                   
                         np.where(local_df['CATEGORIES'].str.contains('OTHER'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('CHANGE IN INVESTMENT'),'Obscurely Marked Items',          
                         np.where(local_df['CATEGORIES'].str.contains('VOID OF 11/16 DISBURSEMENT'),'Obscurely Marked Items',                                   
                         np.where(local_df['CATEGORIES'].str.contains('LINE 17'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('MONTHLY'),'Obscurely Marked Items',                                                        
                         np.where(local_df['CATEGORIES'].str.contains('OFFSET'),'Obscurely Marked Items',  
                         np.where(local_df['CATEGORIES'].str.contains('VOID'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('RENEW'),'Obscurely Marked Items',  
                         np.where(local_df['CATEGORIES'].str.contains('RENEWAL'),'Obscurely Marked Items',     
                         np.where(local_df['CATEGORIES'].str.contains('CC PAYMENT'),'Obscurely Marked Items',  
                         np.where(local_df['CATEGORIES'].str.contains('CC'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('VISA'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('MASTERCARD'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('MASTER CARD'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('MASTER-CARD'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('DISCOVER'),'Obscurely Marked Items',  
                         np.where(local_df['CATEGORIES'].str.contains('PAYPAL'),'Obscurely Marked Items',
                         np.where(local_df['CATEGORIES'].str.contains('MEMMOS'),'Obscurely Marked Items',local_df['CATEGORIES']
                                 )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df        

def overlooked(expenses_df):
    
    print("")
    print("--------Parsing Overlooked Items--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('PAY'),'Compensation for Salary and Hourly',
                         np.where(local_df['CATEGORIES'].str.contains('JUL PAY'),'Compensation for Salary and Hourly',                            
                         np.where(local_df['CATEGORIES'].str.contains('ASSESSMENT'),'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('STAFF'),'Compensation to Staff',                           
                         np.where(local_df['CATEGORIES'].str.contains('ASSESSMENT'),'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('STAFF'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('NEWSLETTER'),'Marketing Expense for Collateral and Print', 
                         np.where(local_df['CATEGORIES'].str.contains('STAFFING'),'Compensation to Staff',local_df['CATEGORIES'] 
                                 ))))))))
    
    parsing_report(local_df)      #Print out parsing report
    return local_df  

def categorize_expenses(expenses_df):

    print("")
    print("--------Putting the expenses in final categories--------")
    print("")  

    local_df=expenses_df 
    
    local_df['CATEGORIES'] =   np.where(local_df['CATEGORIES'].str.contains('Compensation to Consultants'),'Compensation to Consultants',
                         np.where(local_df['CATEGORIES'].str.contains('Compensation to Staff'),'Compensation to Staff', 
                         np.where(local_df['CATEGORIES'].str.contains('Compensation to Contractors'),'Compensation to Contractors',   
                         np.where(local_df['CATEGORIES'].str.contains('Compensation for Salary and Hourly'),'Compensation for Salary and Hourly', 
                         np.where(local_df['CATEGORIES'].str.contains('Compensation as Bonuses and Commission'),'Compensation as Bonuses and Commission',
                         np.where(local_df['CATEGORIES'].str.contains('Compensation as Benefits'),'Compensation as Benefits',

                         np.where(local_df['CATEGORIES'].str.contains('Accounting Expense'),'Accounting Expense',
                         np.where(local_df['CATEGORIES'].str.contains('Legal Expense'),'Legal Expense',  
                         np.where(local_df['CATEGORIES'].str.contains('Donation Expense'),'Donation Expense',

                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense Direct Response'),'Marketing Expense Direct Response', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense Fundraising'),'Marketing Expense Fundraising',                               
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for CRM'),'Marketing Expense for CRM', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Imagery'),'Marketing Expense for Imagery',                               
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Collateral and Print'),'Marketing Expense for Collateral and Print', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Events'),'Marketing Expense for Events', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Gifts'),'Marketing Expense for Gifts', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Outdoor Advertising'),'Marketing Expense for Outdoor Advertising',
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Promotional Items'),'Marketing Expense for Promotional Items', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Digital Assets'),'Marketing Expense for Digital Assets',                              
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Digital Advertising'),'Marketing Expense for Digital Advertising', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Bulk Email'),'Marketing Expense for Bulk Email',                              
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Social Media'),'Marketing Expense for Social Media', 
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Analytics'),'Marketing Expense for Analytics',      
                         
                         np.where(local_df['CATEGORIES'].str.contains('Cell Phones'),'Cell Phones',    
                                  
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Phone Banking'),'Marketing Expense for Phone Banking',                               
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Canvassing'),'Marketing Expense for Canvassing',                                                          
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for TV and Radio'),'Marketing Expense for TV and Radio',                                                                            
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Public Relations'),'Marketing Expense for Public Relations',                              
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Text Blasting'),'Marketing Expense for Text Blasting',                              
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Fax Blasting'),'Marketing Expense for Fax Blasting',                             
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense for Mail'),'Marketing Expense for Mail',                              
                         np.where(local_df['CATEGORIES'].str.contains('Marketing Expense Other'),'Marketing Expense Other',

                         np.where(local_df['CATEGORIES'].str.contains('Food and Beverages'),'Food and Beverages',    

                         np.where(local_df['CATEGORIES'].str.contains('Travel Expense'),'Travel Expense', 

                         np.where(local_df['CATEGORIES'].str.contains('Office Expense for Software'),'Office Expense for Software',                              
                         np.where(local_df['CATEGORIES'].str.contains('Office Expense for Office Services'),'Office Expense for Office Services', 
                         np.where(local_df['CATEGORIES'].str.contains('Office Expense for Supplies'),'Office Expense for Supplies', 
                         np.where(local_df['CATEGORIES'].str.contains('Office Expense for IT Services'),'Office Expense for IT Services', 
                         np.where(local_df['CATEGORIES'].str.contains('Office Expense for Network and Computer Equipment'),'Office Expense for Network and Computer Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('Office Expense For Furniture and Equipment'),'Office Expense For Furniture and Equipment', 
                         np.where(local_df['CATEGORIES'].str.contains('Office Expense for Rent and Utilities'),'Office Expense for Rent and Utilities', 
                         np.where(local_df['CATEGORIES'].str.contains('Office Expense General'),'Office Expense General',    

                         np.where(local_df['CATEGORIES'].str.contains('Reimbursements'),'Reimbursements',                                            
                         np.where(local_df['CATEGORIES'].str.contains('Association Dues and Subscriptions'),'Association Dues and Subscriptions', 
                         np.where(local_df['CATEGORIES'].str.contains('Credit Card PayPal and Transaction Fees'),'Credit Card PayPal and Transaction Fees',                               
                         np.where(local_df['CATEGORIES'].str.contains('Bank Fees'),'Bank Fees',                                            
                         np.where(local_df['CATEGORIES'].str.contains('Petty Cash'),'Petty Cash', 
                         np.where(local_df['CATEGORIES'].str.contains('Obscurely Marked Items'),'Obscurely Marked Items', 
                         np.where(local_df['CATEGORIES'].str.contains('Tax Expense'),'Tax Expense',
                         np.where(local_df['CATEGORIES'].str.contains('In Kind Contributions'),'In Kind Contributions', 
                                   
                         np.where(local_df['CATEGORIES'].str.contains('Other Fees and Interest'),'Other Fees and Interest','Uncategorized Expenses'
                                 )))))))))))))))))))))))))))))))))))))))))))))))))))

    parsing_report(local_df)      #Print out parsing report
    return local_df 



#Definitions for the parser's execution

def parse_expenses(FEC_raw_expense_data_filepath , FEC_raw_expense_header_filepath):

    print("")
    print("--------This will parse the expense items, print a preview, and write them to a new CSV file--------")
    print("")
  
    #Read in the dataframe in raw format and convert to a dataframe.
    expenses_df = read_FEC_data(FEC_raw_expense_data_filepath , FEC_raw_expense_header_filepath)     #Read in raw data FEC data.  
    expenses_df = select_expenses_columns(expenses_df)                     #Select column features for the dataframe
    expenses_df = create_categories_column(expenses_df)                    #Create CATEGORIES column to parse expenses into.
    
    #Parse out compensation...
    expenses_df = parse_compensation_consultants(expenses_df)              #Parse Compensation for Consultants.
    expenses_df = parse_compensation_staff(expenses_df)                    #Parse Compensation for Staff.
    expenses_df = parse_compensation_contractors(expenses_df)              #Parse Compensation for Contractors.
    expenses_df = parse_compensation_hourly_and_salary(expenses_df)        #Parse Compensation for Hourly and Salary.
    expenses_df = compensation_bonuses_and_commission(expenses_df)         #Parse Compensation for Bonuses and Commission.
    expenses_df = compensation_benefits(expenses_df)                       #Parse Compensation for Benefits.
    
    #Parse out professional services...
    expenses_df = accounting_expense(expenses_df)                          #Parse Accounting Expenses. 
    expenses_df = legal_expense(expenses_df)                               #Parse Legal Expenses. 
    expenses_df = association_dues_subscriptions(expenses_df)              #Parse Association Dues and Subscriptions.     

    #Parse out marketing expenses...
    expenses_df = marketing_expense_direct_response(expenses_df)           #Parse Marketing Expense for Direct Response.
    expenses_df = marketing_expense_fundraising(expenses_df)               #Parse Marketing Expense for Fundraising.    
    expenses_df = marketing_expense_CRM(expenses_df)                       #Parse Marketing Expense for CRM.
    expenses_df = marketing_expense_imagery(expenses_df)                   #Parse Marketing Expense for Imagery.
    expenses_df = marketing_expense_collateral_and_print(expenses_df)      #Parse Marketing Expense for Collateral and Print.
    expenses_df = marketing_expense_promotional_items(expenses_df)         #Parse Marketing Expense for Promotional Items.
    expenses_df = marketing_expense_events(expenses_df)                    #Parse Marketing Expense for Events.    
    expenses_df = marketing_expense_event_items(expenses_df)               #Parse Marketing Expense for Events - Event Items.  
    expenses_df = marketing_expense_gifts(expenses_df)                     #Parse Marketing Expense for Gifts.
    expenses_df = marketing_expense_outdoor_advertising(expenses_df)       #Parse Marketing Expense for Outdoor Advertising.
    expenses_df = marketing_expense_digital_assets(expenses_df)            #Parse Marketing Expense for Digital Assets.
    expenses_df = marketing_expense_digital_advertising(expenses_df)       #Parse Marketing Expense for Digital Advertising.
    expenses_df = marketing_expense_bulk_email(expenses_df)                #Parse Marketing Expense for Bulk Email.
    expenses_df = marketing_expense_social_media(expenses_df)              #Parse Marketing Expense for Social Media.    
    expenses_df = marketing_expense_analytics(expenses_df)                 #Parse Marketing Expense for Analytics.
    
    expenses_df = cell_phone(expenses_df)                                  #Parse Expense for Cell Phones.   

    expenses_df = marketing_expense_phone_banking(expenses_df)             #Parse Marketing Expense for Phone Banking.
    expenses_df = marketing_expense_canvassing(expenses_df)                #Parse Marketing Expense for Canvassing.     
    expenses_df = marketing_expense_for_TV_and_radio(expenses_df)          #Parse Marketing Expense for TV and Radio.  
    expenses_df = marketing_expense_public_relations(expenses_df)          #Parse Marketing Expense for Public Relations. 
    expenses_df = marketing_expense_text_blasting(expenses_df)             #Parse Marketing Expense for Text Blasting.   
    expenses_df = marketing_expense_fax_blasting(expenses_df)              #Parse Marketing Expense for Fax Blasting.   
    expenses_df = marketing_expense_mail(expenses_df)                      #Parse Marketing Expense for Mail.     
    expenses_df = marketing_expense_other(expenses_df)                     #Parse Marketing Expense for Other


    #Parse out food and beverages...
    expenses_df = beverages(expenses_df)                                   #Parse Beverages into Food and Beverages.   
    expenses_df = food(expenses_df)                                        #Parse Food into Food and Beverages.    

    #Parse out travel expenses...
    expenses_df = air_travel(expenses_df)                                  #Parse Air Travel into Travel Expense.   
    expenses_df = accomodations(expenses_df)                               #Parse Accomodations into Travel Expense.        
    expenses_df = ground_transportation(expenses_df)                       #Parse Ground Transportation into Travel Expense. 
    expenses_df = travel_other(expenses_df)                                #Parse Other Travel into Travel Expense.

    #Parse out office expenses...                                
    expenses_df = office_software(expenses_df)                             #Parse Office Expense for Software.                                
    expenses_df = office_services(expenses_df)                             #Parse Office Expense for Office Services.                                 
    expenses_df = office_supplies(expenses_df)                             #Parse Office Expense for Office Supplies.
    expenses_df = office_IT(expenses_df)                                   #Parse Office Expense for IT Services.
    expenses_df = office_network_computer_equipment(expenses_df)           #Parse Office Expense for Network and Computer Equipment.  
    expenses_df = office_furniture_equipment(expenses_df)                  #Parse Office Expense for Office Furniture and Equipment.
    expenses_df = office_rent_and_utilities(expenses_df)                   #Parse Office Expense for Rent and Utilities.      
    expenses_df = office_other(expenses_df)                                #Parse Office Expense for Other.                                  

    #Parse out financial expenses...                                  
    expenses_df = tax_expense(expenses_df)                                 #Parse Tax Expenses.   
    expenses_df = in_kind_contributions(expenses_df)                       #Parse In Kind Contributions. 
    expenses_df = reimbursements(expenses_df)                              #Parse Reimbursements.    
    expenses_df = donation_expense(expenses_df)                            #Parse Donation Expenses. 
    expenses_df = transaction_fees(expenses_df)                            #Parse Credit Card PayPal and Transaction Fees. 
    expenses_df = bank_fees(expenses_df)                                   #Parse Bank Fees.                                 
    expenses_df = petty_cash(expenses_df)                                  #Parse Petty Cash.
    expenses_df = other_fees(expenses_df)                                  #Parse Other Fees and Interest.     
                                                          
    #Parse out missed and obscurely marked items...                                
    expenses_df = obscurely_marked(expenses_df)                            #Parse Obscurely Marked Items.  

    expenses_df = overlooked(expenses_df)                                  #Parse Overlooked Items.  
                                
    #Print a count of all finally parsed categories...                            
    parsing_report_2 = expenses_df.CATEGORIES.value_counts()[:60]          #Look at final categories
    print(parsing_report_2)
    
    
    return expenses_df

#Definitions to merge files and write them to CSV format

def group_individual_donations_by_committee(individuals_file_path,headers_file_path,individuals_output_file_path):

    #Read in individual donations.
    local_df = read_FEC_data(individuals_file_path,headers_file_path) 
    
    #Rename the individual donations column to accurately refelct the upcomming change.  
    local_df['TOTAL_INDIVIDUAL_DONATIONS'] = local_df['TRANSACTION_AMT'] 
    local_df = local_df[['CMTE_ID','TOTAL_INDIVIDUAL_DONATIONS']]   
    
    #Sum all individual donations to each group in the total individual dontations column.
    grouped_df = local_df.groupby('CMTE_ID').sum()                                       
    
    #Write the new dataframe to a CSV file. 
    grouped_df.to_csv(individuals_output_file_path)         
    
    #Read the CSV file back into the datframe.
    local_df = pd.read_csv(individuals_output_file_path)                               
    
    return(local_df)

    
def pivot_expenses_by_category(committee_expenses_file_path,pivoted_output_file_path):
    
    #Read in committee expenses that have already been grouped
    local_df = pd.read_csv(committee_expenses_file_path,encoding = "ISO-8859-1")
    
    #Pivot table to consolodate all expenses into columns.  Pivot table to put expenses in columns, indexed by election committee
    local_df = local_df.pivot_table('TRANSACTION_AMT',index='CMTE_ID',columns='CATEGORIES',aggfunc='sum') 

    #Drop all NAN Values and replace them with 0 
    local_df = local_df.fillna(value=0)   

    #Create a total expenses column    
    local_df['TOTAL_EXPENSES'] = local_df.sum(axis=1)
 
    #Write the new dataframe to a CSV file.
    local_df.to_csv(pivoted_output_file_path) 
    
    #Read the CSV file back in.
    local_df = pd.read_csv(pivoted_output_file_path)
    
    return(local_df)

def merge_donations_to_expenses(expensed_columns_df,grouped_df,merged_output_file_path):

    #Join the Expense Data to the Individual Donations, so we preserve the names of the master file where expenses are not listed. 
    merged_df = pd.merge(expensed_columns_df,grouped_df,on=['CMTE_ID'],how='left')
    
    #Write the new dataframe to a CSV file.
    merged_df.to_csv(merged_output_file_path) 
    
    #Read the CSV file back in. 
    merged_df = pd.read_csv(merged_output_file_path)
    
    local_df=merged_df
    
    return(local_df)

def merge_committee_master_file(committee_master_file_path,headers_file_path,master_merged_output_file_path,merged_df):

    #Read in committee master file.
    local_df = read_FEC_data(committee_master_file_path,headers_file_path)
    
    #Merge committee master file with the merged data frame
    local_df = pd.merge(local_df,merged_df,on=['CMTE_ID'],how='left')
    
    #Drop all NAN Values and replace them with 0 
    local_df = local_df.fillna(value=0)   
    
    #Save newly merged data file to a CSV file
    local_df.to_csv(master_merged_output_file_path)
    
    return(local_df)
   
def presidential_or_midterm_year(local_df,election_cycle,election_year,master_merged_output_file_path):

    #Add a column with pre-selected election cycle ('MIDTERM' or 'PRESIDENTIAL')
    local_df['ELECTION_CYCLE']=election_cycle
    
    #Add a column for the election year
    local_df['ELECTION_YEAR']=election_year
    
    #Save newly merged data file to a CSV file
    local_df.to_csv(master_merged_output_file_path)
    
    return(local_df)



#Execute Parser and File Writer

#For loop to cycle through the election cycle from 2004 to 2016

for year in range(2008,2017,2):
    
    election_year    =  year
    prior_year       =  year - 1
    election_number  =  calculate_election_number(election_year,p='no')
    election_cycle   =  calculate_election_cycle(election_year,'no')
    
    #Print opening
    print('             \\\\\\\\\\\\\\\\\\\\ ----- Parsing the '+str(prior_year)+' - '+str(election_year)+' FEC Data Files ----- ////////////////////')
    
    #Find filepaths for raw committee operations expense data
    FEC_raw_expense_data_filepath,FEC_raw_expense_header_filepath,FEC_raw_expense_csv_filepath          = find_raw_expense_filepaths(election_year)

    #Find filepaths for individual donation data
    FEC_raw_individual_data_filepath,FEC_raw_individual_header_filepath,FEC_raw_individual_csv_filepath = find_raw_individual_data_filepaths(year)
 
    #Find filepaths for raw individual donation data
    FEC_raw_committee_data_filepath,FEC_raw_committee_header_filepath,FEC_raw_committee_csv_filepath    = find_raw_committee_data_filepaths(year)
    
    #Assign output filepaths for final grouped and parsed data
    FEC_categorized_expense_csv_filepath,FEC_donations_groupedby_committee_csv_filepath,FEC_expenses_groupedby_committee_csv_filepath,Merged_expenses_and_donations_filepath = find_final_outputs_filepaths(year)
    
    #Assign output filepaths for New Output File Folder
    master_merged_output_file_path,category_count_file_path,category_total_file_path = find_New_Output_filepaths(election_year)
    
    #Execute parser
    parsed_expenses_df=parse_expenses(FEC_raw_expense_data_filepath , FEC_raw_expense_header_filepath)

    #Save partsing results to New Output Count Files
    #counts = parsing_report_counts(parsed_expenses_df)
    #counts.to_csv(category_count_file_path)
    
    #Display parsing results
    parsed_expenses_df.CATEGORIES.value_counts()[:80] 

    #Final categorization of expenses
    categorized_expenses_df=categorize_expenses(parsed_expenses_df)

    #Write final results to a file
    categorized_expenses_df.to_csv(FEC_categorized_expense_csv_filepath)
    #FEC_expenses_groupedby_committee_csv_filepath
    
    #Group individual donations by committee
    grouped_df = group_individual_donations_by_committee(FEC_raw_individual_data_filepath,FEC_raw_individual_header_filepath,FEC_raw_individual_csv_filepath)

    #Pivot expenses into categories
    expensed_columns_df = pivot_expenses_by_category(FEC_categorized_expense_csv_filepath,FEC_expenses_groupedby_committee_csv_filepath)

    #Merge donations to expenses
    merged_df = merge_donations_to_expenses(expensed_columns_df,grouped_df,Merged_expenses_and_donations_filepath)

    #Merge committee master file with donations to expenses
    master_merged_file = merge_committee_master_file(FEC_raw_committee_data_filepath,FEC_raw_committee_header_filepath,FEC_raw_committee_csv_filepath,merged_df)

    #Add presidential or midterm to the last column
    Final_master_merged_file = presidential_or_midterm_year(master_merged_file,election_cycle,election_year,master_merged_output_file_path)

    Final_master_merged_file.head(600)
    
