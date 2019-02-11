from bs4 import BeautifulSoup as bs
from selenium import webdriver

#Function declarations
def stringTimeToDecimal(string):
    time_array = []
    timeMinutes = 0
    if len(string) < 10:
        #convert MM:SS.MS
        time_array = string.split(':')
        time_array[0] = int(time_array[0])
        time_array[1] = round(float(time_array[1])/60,2)
        return sum(time_array)
    else:
        #convert H:MM:SS.MS
        time_array = string.split(':')
        time_array[0] = int(time_array[0])*60
        time_array[1] = int(time_array[1])
        time_array[2] = round(float(time_array[2])/60,2)
        return sum(time_array)     
    
def makeLine(num):
    line = ''
    for i in range(num):
        line += '='
    return line

def makeDict(array):
    my_dict = {}
    for e in array:
        if e not in my_dict:
            my_dict[e] = 0
        
        my_dict[e] += 1
    return my_dict

def decimalToTime(num):
    time_string = ''
    time_array = []
    hh, mm, ss = 0,0,0
    if num >= 60.00:
        hh = num/60
        mm = (hh%1)*60
        ss = (mm%1)*60
        time_string = "%2s:%2s:%2s" % (str(int(hh)).zfill(2),str(int(mm)).zfill(2),str(int(ss)).zfill(2))
    else:
        mm = int(num)
        ss = round((num%1)*60)
        time_string = "%2s:%2s" % (str(mm).zfill(2),str(ss).zfill(2))
    return time_string


#url to scrape
url = 'https://runsignup.com/Race/Results/?raceId=42350#resultSetId-81813;perpage:5000'

dist = 3.72823 #For 6k scraping
#dist = 7.45645 #For 12k scraping

time_strings = []
paces = []

#Open page, get HTML, traverse and get td's
driver = webdriver.Firefox(executable_path='/home/chad/Desktop/webscrape/geckodriver')
driver.implicitly_wait(30)
driver.get(url)
soup = bs(driver.page_source,'html.parser')
driver.close()
times = soup.findAll('td',{'class':'time'})

#Scrap lines containing appropriate times
for i in range(1,len(times),3):
    time_strings.append(str(times[i]))
    
#Strip HTMl from time strings
for i in range(len(time_strings)):
    time_strings[i] = time_strings[i].strip('<td class="time" style="text-align: right;">')
    time_strings[i] = time_strings[i].strip('</td>')
    time_strings[i] = stringTimeToDecimal(time_strings[i])

#Create array of paces from array of decimal times
for e in time_strings:
    paces.append(e//dist)

#Calculate average pace, median pace and create dictionary of paces
averagePace = sum(time_strings)/len(time_strings)/dist
medianPace = time_strings[len(time_strings)//2]/dist
pace_dict = makeDict(paces)

#Print statemets for mean, median and histogram of paces
print("Average Pace: %s" % decimalToTime(averagePace))
print("Median Pace: %s" % decimalToTime(medianPace))

for key in pace_dict:
    print("%2d: %s" % (key, makeLine(pace_dict[key])))
