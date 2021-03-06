#This program uses PDF2TXT. Download it here: https://www.pdf2txt.com/ and save in the same directory as this file.
from ftplib import FTP
import os
import re
import pickle
import csv
import smtplib, ssl

def ftp_get_pdf():
    ftp = FTP('ftp.ocfl.net')     # connect to host, default port
    ftp.login()                     # user anonymous, passwd anonymous@
    ftp.cwd('divisions/corrections/pub')               # change into "debian" directory
    ftp.retrbinary('RETR bookings.pdf', open('bookings.pdf', 'wb').write)
    ftp.quit()

def extract_text_from_pdf():
    os.system('java -jar pdfbox-app-2.0.12.jar ExtractText bookings.pdf bookings.txt') 

def extract_date_from_text_file():
    #read file
    with open('bookings.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    #Find top row with date, which starts with "BEGINNING AT MIDNIGHT"
    for line in range(len(content)):
        if "BEGINNING AT MIDNIGHT" in content[line]:
            date = content[line]
            if date.startswith("BEGINNING AT MIDNIGHT"):
                return date[23:] #delete unnecessary wording in string
                date = re.sub('[ ]', '', date)
    return date
    
def process_text_file():    
    with open('bookings.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    
    #Loop over all elements of content, which contain all arrests
    data_raw = []        
    current_arrestee = []
    first_arrestee_flag = 1
    for line in range(0, len(content)):
    
        #If line contains certain markers, it is the first line for a new arrestee:
        if " BRC" in content[line] or " --" in content[line]\
        or "FDC" in content[line] or "MAIN-" in content[line]:
            if first_arrestee_flag == 0:
                #Add previous arrestee to data_raw
                data_raw.append(current_arrestee)
            first_arrestee_flag = 0
            #Start a new sublist for a new arrestee 
            current_arrestee = []
            #Add current line to new arrestee
            current_arrestee.append(content[line])
            
        else:
            #If this is not the first line: Add to the record of the current arrestee
            current_arrestee.append(content[line])
    
    #Sve the last arrestee to data_raw
    data_raw.append(current_arrestee)        
    
    return data_raw    

def label_booking_number(line):
    if " / M" in ' '.join(data_raw[line]):
        str_male = " / M"
        index = ' '.join(data_raw[line]).index(str_male)
        booking_number = re.sub('[ / M]', '', data_raw[line][0][index:][:12])
    elif " / F" in ' '.join(data_raw[line]):
        str_female = " / F"
        index = ' '.join(data_raw[line]).index(str_female)
        booking_number = re.sub('[ / F]', '', data_raw[line][0][index:][:12])
    else:
        booking_number = "Booking number not found"
        print('Booking number not found for line ', line)
         
    if len(booking_number) == 8:
        return booking_number
    else:
        print ("Check booking number for line ", line)
    
#Create name column by taking the first item in the list and cutting it off 
#at the end of the name, which is the cell location
def label_name(line):
    #Index location of the items at the end of the name, always "BRC", "FDC", "MAIN" or "--"
    str_brc = " BRC"
    str_dashes = " --"
    str_fdc = " FDC"
    str_main = "MAIN-"
    if "BRC" in ' '.join(data_raw[line]):
        index = data_raw[line][0].index(str_brc)
    elif "FDC" in ' '.join(data_raw[line]):
        index = data_raw[line][0].index(str_fdc)
    elif "MAIN-" in ' '.join(data_raw[line]):
        index = data_raw[line][0].index(str_main)
    elif "--" in ' '.join(data_raw[line]):
        index = data_raw[line][0].index(str_dashes)
    else:
        name = "Name not found"
        print("Could not find end of name in line", line)
    
    try:
        name
    except:
        name = data_raw[line][0][0:index]    
    
    return name.title()

#Create race and gender columns
def label_race_gender(line):
    race = []
    gender = []
    if "W / M" in ' '.join(data_raw[line]):
        race = "White"
        gender = "Male"
    elif "W / F" in ' '.join(data_raw[line]):
        race = "White"
        gender = "Female"
    elif "B / M" in ' '.join(data_raw[line]):
        race = "Black"
        gender = "Male"
    elif "B / F" in ' '.join(data_raw[line]):
        race = "Black"
        gender = "Female"
    elif "A / M" in ' '.join(data_raw[line]):
        race = "Asian"
        gender = "Male"
    elif "A / F" in ' '.join(data_raw[line]):
        race = "Asian"
        gender = "Female"
    elif "I / M" in ' '.join(data_raw[line]):
        race = "Native"
        gender = "Male"
    elif "I / F" in ' '.join(data_raw[line]):
        race = "Native"
        gender = "Female"
    elif "U / M" in ' '.join(data_raw[line]):
        race = "Unknown"
        gender = "Male"
    elif "U / F" in ' '.join(data_raw[line]):
        race = "Unknown"
        gender = "Female"
    else:
        print("Did not find race/gender for line", line)
    return race, gender

#Create ethnicity (Hispanic/non-Hispanic columns)
def label_hispanic_or_non(line):
    if "NON-HISPANIC" in ' '.join(data_raw[line]):
        ethnicity = "Non-Hispanic"
    elif "HISPANIC" in ' '.join(data_raw[line]):
        ethnicity = "Hispanic"
    elif "UNKNOWN" in ' '.join(data_raw[line]):
        ethnicity = "Unknown"
    else:
        ethnicity = "None"
        print("Did not find ethnicity for line", line)
        
    return ethnicity

#create age column by finding the preceeding box, which is ethnicity, and working backwards
def label_age(line):
    iage = 0
    if "NON-HISPANIC" in ' '.join(data_raw[line]):
           i = (data_raw[line].index("NON-HISPANIC"))-1
           iage = data_raw[line][i]
    if iage == 0:
        if "HISPANIC" in ' '.join(data_raw[line]):
            i = (data_raw[line].index("HISPANIC"))-1
            iage = data_raw[line][i]
    if iage == 0:
        if "UNKNOWN" in ' '.join(data_raw[line]):
            i = (data_raw[line].index("UNKNOWN"))-1
            iage = data_raw[line][i]
    if iage == 0:
        print("Did not find age", "line", line)
    try:
        age = int(iage)
    except ValueError:
        #iage = -99
        str = data_raw[line][0]
        age = int(str[-2:])
        #print("Non-numeric data found in the file")
   
    if age not in range(15,120):
        print("Did not find age in range for line", line)
    return age
    
#Create law enforcement agency column
def label_law_enforcement_agency(line):
    agency = []
    if "APOPKA  PD" in ' '.join(data_raw[line]):
        agency = "Apopka Police Department"
    elif "BELLE ISLE POLICE DEPARTMENT" in ' '.join(data_raw[line]):
        agency = "Belle Isle Police Department"
    elif "BONDING AGENCY" in ' '.join(data_raw[line]):
        agency = "Bonding agency"
    elif "DIV OF STATE FIRE MARSHALL" in ' '.join(data_raw[line]):
        agency = "State Fire Marshall"
    elif "DRUG ENFORCEMENT AGENCY" in ' '.join(data_raw[line]):
        agency = "DEA"
    elif "EATONVILLE PD" in ' '.join(data_raw[line]):
        agency = "Eatonville Police Department"
    elif "EDGEWOOD PD" in ' '.join(data_raw[line]):
        agency = "Edgewood Police Department"
    elif "FDLE" in ' '.join(data_raw[line]):
        agency = "FDLE"
    elif "FLORIDA HIGHWAY PATROL" in ' '.join(data_raw[line]):
        agency = "Florida Highway Patrol"    
    elif "MAITLAND PD" in ' '.join(data_raw[line]):
        agency = "Maitland Police Department"
    elif "CONTEMPT OF COURT" in ' '.join(data_raw[line])\
    or "RETURN PER COURT ORDER" in ' '.join(data_raw[line]):
        agency = "Ninth Judicial Circuit"
    elif "OCOEE PD" in ' '.join(data_raw[line]):
        agency = "Ocoee Police Department"
    elif "ORANGE COUNTY CLERK OF COURT" in ' '.join(data_raw[line]):
        agency = "Orange County Clerk of Courts"
    elif "OAKLAND PD" in ' '.join(data_raw[line]):
        agency = "Oakland Police Department"
    elif "ORANGE COUNTY SHERIFF OFFICE" in ' '.join(data_raw[line]):
        agency = "Orange County Sheriff"
    elif "ORLANDO PD" in ' '.join(data_raw[line]):
        agency = "Orlando Police Department"
    elif "UCF PD" in ' '.join(data_raw[line]):
        agency = "UCF Police Department"
    elif "VIOLATION OF PROBATION" in ' '.join(data_raw[line]):
        agency = "Probation violation"
    elif "WINDERMERE PD" in ' '.join(data_raw[line]):
        agency = "Windermere Police Department" 
    elif "WINTER GARDEN PD" in ' '.join(data_raw[line]):
        agency = "Winter Garden Police Department"
    elif "WINTER PARK PD" in ' '.join(data_raw[line]):
        agency = "Winter Park Police Department"  
    else: 
        agency = "Agency not found"
        print("Did not find agency for line", line)
    return agency

#create misdemeanor or felony column        
def label_misdemeanor_or_felony(line):
    if "FELONY" in ' '.join(data_raw[line]) and "MISDEMEANOR" in ' '.join(data_raw[line]):
        crime_designation = "Misdemeanor and Felony"
    elif "FELONY" in ' '.join(data_raw[line]):
        crime_designation = "Felony"
    elif "MISDEMEANOR" in ' '.join(data_raw[line]):
        crime_designation = "Misdemeanor"
    else:
        crime_designation = "Crime designation not found"
        print("Did not find crime designation for line", line)
    
    return crime_designation

#Create column(s) for crime(s)
def label_crime(line):
    str_degree = "DEGREE"
    #find indices of all items in sublist containing the word "DEGREE"
    regex = re.compile(".*DEGREE.*")
    data_a = data_raw[line]
    icrime = [i for i, item in enumerate(data_a) if re.search(regex, item)]
    #Loop over all of these items; extract offence type
    crime = []
    for i in icrime:
        index = data_raw[line][i].index(str_degree)
        crime_title = ((data_raw[line][i][index:]).split(' '))[1:]
        crime_title = (' '.join(crime_title)).title()
        #Remove commas from crime title 
        if "," in crime_title:
            crime_title = re.sub('[,]', '', crime_title)

        crime.append(crime_title)

    return crime


#put it all together
def build_data():
    data = []
    #Go over raw data line by line
    for line in range(len(data_raw)): 
        sublist = []
        #Extract date, gender, race, ethnicity, crime designation
        booking_number = label_booking_number(line)
        name = label_name(line)
        date = extract_date_from_text_file()
        race, gender = label_race_gender(line)
        ethnicity = label_hispanic_or_non(line)
        age = label_age(line)
        agency = label_law_enforcement_agency(line)
        crime_designation = label_misdemeanor_or_felony(line)
        crime = label_crime(line)
        #Put into columns of sublist 
        sublist.append(booking_number)
        sublist.append(name)
        sublist.append(date)
        sublist.append(race)
        sublist.append(gender)
        sublist.append(ethnicity)
        sublist.append(age)
        sublist.append(agency)
        sublist.append(crime_designation)
        sublist.append(crime)
        data.append(sublist)
        
    
    return data
  
def save_data():
    with open('data.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([data], f)

#Rename file with date
def rename_file():
    date_file_name = re.sub('[/]', '.', date)
    command_string = '/bin/mv -f bookings.pdf output/bookings_' + date_file_name +'.pdf' 
    os.system(command_string)
    command_string = '/bin/mv -f bookings.txt output/bookings_' + date_file_name +'.txt' 
    os.system(command_string)
    command_string = '/bin/mv -f data.pkl output/bookings_' + date_file_name +'.pkl'
    os.system(command_string)  
    

########################################################################
# Main program:
########################################################################
ftp_get_pdf()
extract_text_from_pdf()
date = extract_date_from_text_file()
data_raw = process_text_file()
data = build_data()
save_data()
rename_file()
