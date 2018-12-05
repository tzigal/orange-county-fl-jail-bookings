import pickle
import os
import itertools
import matplotlib.pyplot as plt
from collections import Counter as counter
import numpy as np


os.chdir('/Users/Gal/Dropbox/Crime-clusters/scraping/output/')

def list_files_in_directory():
    #os.chdir('/Users/Gal/Dropbox/Crime-clusters/scraping/output/')
    #for file in os.listdir('.'):
   pkl_list = [file for file in os.listdir('/Users/Gal/Dropbox/Crime-clusters/scraping/output/')\
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
        crime_types.append(combined_data[i][8])
    merged_list = list(itertools.chain(*crime_types)) 
    crime_types = set(merged_list)
    return crime_types

def list_crime_names_for_analysis(): #this is a check to see if subsequent functions are capturing all the crimes
    crime_types_for_analysis = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][8]):
            crime_types_for_analysis.append(combined_data[i][8])#to get full data for each offence, remove [8]
    return crime_types_for_analysis

def analyze_crime_type_by_age():
    crime_age = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][8]):
            crime_age.append(combined_data[i][5])
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
        if crime_name_master in ' '.join(combined_data[i][8]):
            crime_gender.append(combined_data[i][3])
            if 'Male' in (combined_data[i][3]):
                crime_gender_male.append(combined_data[i][3])
            elif 'Female' in (combined_data[i][3]):
                crime_gender_female.append(combined_data[i][3])
    
     #calculate percentages
    crime_gender_male_percentage = (len(crime_gender_male)/len(crime_gender))*100
    crime_gender_female_percentage = (len(crime_gender_female)/len(crime_gender))*100
    
    # Data to plot
    labels = 'Male','Female'
    sizes = [len(crime_gender_male), len(crime_gender_female)]
    colors = ['red', 'blue']
     
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
    crime_race_unknown = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][8]):
            crime_race.append(combined_data[i][2])
            if 'Black' in (combined_data[i][2]) and 'Non-Hispanic' in (combined_data[i][4]):
                temp_list = [] #to prevent adding two variables per person
                temp_list.append(combined_data[i][2])
                temp_list.append(combined_data[i][4])
                crime_race_black.append(temp_list)
            elif 'Black' in (combined_data[i][2]) and 'Hispanic' in (combined_data[i][4]):
                temp_list = []
                temp_list.append(combined_data[i][2])
                temp_list.append(combined_data[i][4])
                crime_race_black_hispanic.append(temp_list)
            elif 'White' in (combined_data[i][2]) and 'Non-Hispanic' in (combined_data[i][4]):
                temp_list = []
                temp_list.append(combined_data[i][2])
                temp_list.append(combined_data[i][4])
                crime_race_white.append(temp_list)
            elif 'White' in (combined_data[i][2]) and 'Hispanic' in (combined_data[i][4]):
                temp_list = []
                temp_list.append(combined_data[i][2])
                temp_list.append(combined_data[i][4])
                crime_race_white_hispanic.append(temp_list)
            elif 'Unknown' in (combined_data[i][2]):
                crime_race_unknown.append(combined_data[i][2])
                
    #calculate percentages
    crime_race_black_percent = (len(crime_race_black)/len(crime_race))*100
    crime_race_black_hispanic_percent = (len(crime_race_black_hispanic)/len(crime_race))*100
    crime_race_white_percent = (len(crime_race_white)/len(crime_race))*100
    crime_race_white_hispanic_percent = (len(crime_race_white_hispanic)/len(crime_race))*100
    crime_race_unknown_percent = (len(crime_race_unknown)/len(crime_race))*100
                    
    # Data to plot 
    if len(crime_race_unknown) == 0.0:
        sizes = [len(crime_race_black), len(crime_race_black_hispanic), len(crime_race_white),\
        len(crime_race_white_hispanic)]
        labels = 'Black','Black and Hispanic','White','White and Hispanic'
        colors = ['darkgreen', 'seagreen','lightseagreen','mediumspringgreen']
    else:
        sizes = [len(crime_race_black), len(crime_race_black_hispanic), len(crime_race_white),\
        len(crime_race_white_hispanic),len(crime_race_unknown)]
        labels = 'Black','Black and Hispanic','White','White and Hispanic','Unknown'
        colors = ['darkgreen', 'seagreen','lightseagreen','mediumspringgreen','c']
    
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
     crime_race_unknown_percent
 
def analyze_crime_type_by_agency():
    crime_agency = []
    for i in range (0, len(combined_data)):
        if crime_name_master in ' '.join(combined_data[i][8]):
            crime_agency.append(combined_data[i][6])
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

def print_to_file():
    # open output text file 
    os.chdir('/Users/Gal/Dropbox/Crime-clusters/scraping/analysis/')
    filename= crime_name_master+' analysis.txt'
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
    print("Number of arrests per agency: ", file=file_text_output)
    print(agency_counter, file=file_text_output)
    # close output file
    file_text_output.close()

##main program
crime_name_master = 'Theft'
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
     crime_race_unknown_percent = analyze_crime_type_by_race()
crime_agency, agency_counter = analyze_crime_type_by_agency()
print_to_file()