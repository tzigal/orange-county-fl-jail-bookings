#enter directory paths in lines 10 and 11 (data home and analysis)
#enter name of crime in line 267

import pickle
import os
import itertools
import matplotlib.pyplot as plt
from collections import Counter as counter
import numpy as np
import re

#directories are for PC -- for a Mac-friendly format, use forwar slashes and start with /Users/
directory = [r'ENTER DIRECTORY PATH HERE']
analysis_directory = [r'ENTER DIRECTORY PATH HERE']
os.chdir(directory)

def list_files_in_directory():
   pkl_list = [file for file in os.listdir(directory)\
   if file.endswith('.pkl')]
   return pkl_list

def combine_files():
    combined_data = []  # Create an empty list
    for file in pkl_list: 
        with open(file, 'rb') as f:
            data_new = pickle.load(f)
            combined_data = combined_data + data_new[0]   # Update contents of file1 to the dictionary
    return combined_data

def make_list_of_crime_types():
    crime_types = []
    for i in range (0, len(combined_data)):
        crime_types.append(combined_data[i][9])
    merged_list = list(itertools.chain(*crime_types)) 
    crime_types = set(merged_list)
    return crime_types

def list_crime_names_for_analysis(): #this is a check to see if subsequent functions are capturing all the crimes
    crime_types_for_analysis = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][9]):
            crime_types_for_analysis.append(combined_data[i][9])#to get full data for each offence, remove [8]
    return crime_types_for_analysis

def analyze_crime_type_by_age():
    crime_age = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][9]):
            crime_age.append(int(combined_data[i][6]))
    plt.figure(1)
    plt.clf()
    num_bins = 20
    n, bins, patches = plt.hist(crime_age, num_bins,range = [0,100],\
                                facecolor='blue', alpha=0.5, rwidth = 0.9, align = 'mid')
    plt.xlabel('Age')
    plt.ylabel('Number of arrests')
    plt.title(('Arrests for '+crime_name_master+' by age'))
    plt.pause(0.01)
    plt.show()
    return crime_age

def analyze_crime_type_by_gender():
    crime_gender = []
    crime_gender_male = []
    crime_gender_female = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][9]):
            crime_gender.append(combined_data[i][4])
            if 'Male' in (combined_data[i][4]):
                crime_gender_male.append(combined_data[i][4])
            elif 'Female' in (combined_data[i][4]):
                crime_gender_female.append(combined_data[i][4])
    
     #calculate percentages
    crime_gender_male_percentage = (len(crime_gender_male)/len(crime_gender))*100
    crime_gender_female_percentage = (len(crime_gender_female)/len(crime_gender))*100
    
    # Data to plot
    labels = 'Male','Female'
    sizes = [len(crime_gender_male), len(crime_gender_female)]
    colors = ['blue', 'red']
     
    # Plot
    plt.figure(2)
    plt.clf()
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(('Arrests for '+crime_name_master+' by gender')) 
    plt.show()
    return crime_gender, crime_gender_male, crime_gender_female,\
     crime_gender_male_percentage, crime_gender_female_percentage

def analyze_crime_type_by_race():
    crime_race = []
    crime_race_black = []
    crime_race_black_hispanic = []
    crime_race_white = []
    crime_race_white_hispanic = []
    crime_race_asian = []
    crime_race_unknown = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][9]):
            crime_race.append(combined_data[i][3])
            if 'Black' in (combined_data[i][3]) and 'Non-Hispanic' in (combined_data[i][5]):
                temp_list = [] #to prevent adding two variables per person
                temp_list.append(combined_data[i][3])
                temp_list.append(combined_data[i][5])
                crime_race_black.append(temp_list)
            elif 'Black' in (combined_data[i][3]) and 'Hispanic' in (combined_data[i][5]):
                temp_list = []
                temp_list.append(combined_data[i][3])
                temp_list.append(combined_data[i][5])
                crime_race_black_hispanic.append(temp_list)
            elif 'White' in (combined_data[i][3]) and 'Non-Hispanic' in (combined_data[i][5]):
                temp_list = []
                temp_list.append(combined_data[i][3])
                temp_list.append(combined_data[i][5])
                crime_race_white.append(temp_list)
            elif 'White' in (combined_data[i][3]) and 'Hispanic' in (combined_data[i][5]):
                temp_list = []
                temp_list.append(combined_data[i][3])
                temp_list.append(combined_data[i][5])
                crime_race_white_hispanic.append(temp_list)
            elif 'Asian' in (combined_data[i][3]):
                temp_list = []
                temp_list.append(combined_data[i][3])
                temp_list.append(combined_data[i][5])
                crime_race_asian.append(temp_list)
            elif 'Unknown' in (combined_data[i][3]):
                crime_race_unknown.append(combined_data[i][3])
                
    #calculate percentages
    crime_race_black_percent = (len(crime_race_black)/len(crime_race))*100
    crime_race_black_hispanic_percent = (len(crime_race_black_hispanic)/len(crime_race))*100
    crime_race_white_percent = (len(crime_race_white)/len(crime_race))*100
    crime_race_white_hispanic_percent = (len(crime_race_white_hispanic)/len(crime_race))*100
    crime_race_asian_percent = (len(crime_race_asian)/len(crime_race))*100
    crime_race_unknown_percent = (len(crime_race_unknown)/len(crime_race))*100
                    
    # Data to plot 
    if len(crime_race_unknown) == 0.0 and len(crime_race_asian) != 0.0:
        sizes = [len(crime_race_black), len(crime_race_black_hispanic), len(crime_race_white),\
        len(crime_race_white_hispanic), len(crime_race_asian)]
        labels = 'Black','Black and Hispanic','White','White and Hispanic','Asian'
        colors = ['darkgreen', 'seagreen','lightseagreen','mediumspringgreen','g']
    elif len(crime_race_asian) == 0.0 and len(crime_race_unknown) != 0.0:
        sizes = [len(crime_race_black), len(crime_race_black_hispanic), len(crime_race_white),\
        len(crime_race_white_hispanic), len(crime_race_unknown)]
        labels = 'Black','Black and Hispanic','White','White and Hispanic','Unknown'
        colors = ['darkgreen', 'seagreen','lightseagreen','mediumspringgreen','g']
    elif len(crime_race_asian) == 0.0 and len(crime_race_unknown) == 0.0:
        sizes = [len(crime_race_black), len(crime_race_black_hispanic), len(crime_race_white),\
        len(crime_race_white_hispanic)]
        labels = 'Black','Black and Hispanic','White','White and Hispanic'
        colors = ['darkgreen', 'seagreen','lightseagreen','mediumspringgreen']
    else:
        sizes = [len(crime_race_black), len(crime_race_black_hispanic), len(crime_race_white),\
        len(crime_race_white_hispanic),len(crime_race_asian),len(crime_race_unknown)]
        labels = 'Black','Black and Hispanic','White','White and Hispanic','Asian','Unknown'
        colors = ['darkgreen', 'seagreen','lightseagreen','mediumspringgreen','g','c']
    
    # Plot
    plt.figure(3)
    plt.clf()
    plt.pie(sizes, labels=labels, colors=colors,
            autopct= '%1.1f%%', shadow=True, startangle=140)
    plt.title(('Arrests for '+crime_name_master+' by race'))
    plt.show()
    return crime_race, crime_race_black, crime_race_black_hispanic, crime_race_white,\
     crime_race_white_hispanic, crime_race_unknown, crime_race_black_percent, \
     crime_race_black_hispanic_percent, crime_race_white_percent ,crime_race_white_hispanic_percent,\
     crime_race_asian_percent, crime_race_unknown_percent
 
def analyze_crime_type_by_agency():
    crime_agency = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][9]):
            crime_agency.append(combined_data[i][7])
    agency_counter = counter(crime_agency)
    agency_names = np.asarray(list(agency_counter.keys()))
    agency_numbers = list(agency_counter.values())
    
    # Plot
    plt.figure(4)
    plt.clf()
    plt.barh(agency_names, width = agency_numbers)
    plt.yticks(agency_names)
    plt.tight_layout()
    plt.title(('Arrests for '+crime_name_master+' by agency'))
    plt.show()
    
    return crime_agency, agency_counter

def build_data_for_analisis():
    data_by_crime = []
    #Go over raw data line by line
    for i in range(len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][9]):
            sublist = []
            #Put into columns of sublist 
            sublist.append(combined_data[i][0])
            sublist.append(combined_data[i][1])
            sublist.append(re.sub('[ ]', '', combined_data[i][2]))
            sublist.append(combined_data[i][3])
            sublist.append(combined_data[i][4])
            sublist.append(combined_data[i][5])
            sublist.append(combined_data[i][6])
            sublist.append(combined_data[i][7])
            sublist.append(combined_data[i][9])
            data_by_crime.append(sublist)
            
    
    return data_by_crime

def print_to_file():
    os.chdir(analysis_directory)
    crime_name_title = crime_name_master
    if "<" in crime_name_title:
        crime_name_title = re.sub('[<]', 'Less Than ', crime_name_title)
    if ">" in crime_name_title:
        crime_name_title = re.sub('[>]', 'More Than ', crime_name_title)
    if "=" in crime_name_title:
        crime_name_title = re.sub('[=]', '', crime_name_title)
    if "/" in crime_name_title:
        crime_name_title = re.sub('[/]', ' or ', crime_name_title)
    if "(" in crime_name_title:
        crime_name_title = re.sub('[(]', '', crime_name_title)
    if ")" in crime_name_title:
        crime_name_title = re.sub('[)]', '', crime_name_title)
    if "#" in crime_name_title:
        crime_name_title = re.sub('[#]', 'Number', crime_name_title)
     
    filename= crime_name_title+' analysis.txt'
    file_text_output=open(filename,'w')
    # print summary of clustering results:
    print(("Total number of arrests for ", crime_name_master,":",len(crime_age)), file=file_text_output)
    print(crime_name_master, " arrests by gender:", file=file_text_output)
    print("Percent male: ",crime_gender_male_percentage, file=file_text_output)
    print("Percent female: ",crime_gender_female_percentage,file=file_text_output)
    print(crime_name_master, " arrests by race:", file=file_text_output)
    print("Percent black: ",crime_race_black_percent, file=file_text_output)
    print("Percent black and Hispanic: ",crime_race_black_hispanic_percent, file=file_text_output)
    print("Percent white: ",crime_race_white_percent, file=file_text_output)
    print("Percent white and Hispanic: ",crime_race_white_hispanic_percent, file=file_text_output)
    print("Percent Asian: ", crime_race_asian_percent, file=file_text_output)
    print("Number of arrests per agency: ", file=file_text_output)
    print(agency_counter, file=file_text_output)
    print(file=file_text_output)
    print(file=file_text_output)
    print('booking_number, ',', last_name,','first_name,', 'date,', 'race,', 'gender,','ethnicity,','age,','department,','crime', file=file_text_output)
    for i in range (len(data_by_crime)):
        print(data_by_crime[i][0],',', data_by_crime[i][1],',', data_by_crime[i][2],',',\
               data_by_crime[i][3],',', data_by_crime[i][4],',', data_by_crime[i][5],',',\
        data_by_crime[i][6],',', data_by_crime[i][7],',', data_by_crime[i][8], file=file_text_output)

    # close output file
    file_text_output.close()
    
    filename= 'allcrimenames.txt'
    file_text_output=open(filename,'w')
    # print summary of clustering results:
    print(sorted(crime_types), file=file_text_output)
    file_text_output.close()


##main program
crime_name_master = "Battery"
pkl_list = list_files_in_directory()
combined_data = combine_files()
crime_types = make_list_of_crime_types()
crime_types_for_analysis = list_crime_names_for_analysis()
crime_age = analyze_crime_type_by_age()
crime_gender, crime_gender_male, crime_gender_female,\
  crime_gender_male_percentage, crime_gender_female_percentage = analyze_crime_type_by_gender()
crime_race, crime_race_black, crime_race_black_hispanic, crime_race_white,\
     crime_race_white_hispanic, crime_race_unknown, crime_race_black_percent, \
     crime_race_black_hispanic_percent, crime_race_white_percent ,crime_race_white_hispanic_percent,\
     crime_race_asian_percent, crime_race_unknown_percent = analyze_crime_type_by_race()
crime_agency, agency_counter = analyze_crime_type_by_agency()
data_by_crime = build_data_for_analisis()
print_to_file()
