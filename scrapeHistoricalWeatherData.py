__author__ = 'seanhendryx'

# This script extracts Solar Radiation in watts/square meter from wunderground within specified date range and saves to csv:
# 1st column is date stamp in yearmonthdayhourminute, 2nd column is solar radiation in watts per square meter

#Example url to query API: http://api.wunderground.com/api/######################/history_20120101/q/AZ/Tucson.json
# Mt. Bigelow station ID: MQSLA3

import json
import requests
import time

def main():
    # Create/open a file called wunder.txt (which will be a comma-delimited file)
    f = open('Solar_Radiation_Wunderground_Data.txt', 'w')

    # Iterate through year, month, and day
    # Changed for-loop over years to pull one year of data per run of script to avoid errors due to connectivity issues
    for y in range(2014, 2015):
        for m in range(1, 13):
            for d in range(1, 32):
            #for h in range(1, 25):
                # Check if leap year
                if y%400 == 0:
                    leap = True
                elif y%100 == 0:
                    leap = False
                elif y%4 == 0:
                    leap = True
                else:
                    leap = False

                # Check if already gone through month
                if (m == 2 and leap and d > 29):
                    continue
                elif (m == 2 and d > 28):
                    continue
                elif (m in [4, 6, 9, 10] and d > 30):
                    continue

                # Format month and day with zero buffer:
                if len(str(m)) < 2:
                    m = '0' + str(m)
                else:
                    m = str(m)
                if len(str(d)) < 2:
                    d = '0' + str(d)
                else:
                    d = str(d)

                # Open wunderground.com url

                #Inside each day page: (for loop)
                #Place your API key in ################
                url = 'http://api.wunderground.com/api/################/history_'+ str(y) + m + d + '/q/pws:MQSLA3.json'
                response = requests.get(url)
                #Wait 1 second to help ensure url is loaded:
                time.sleep(1)
                print(response.raise_for_status())

                string = response.text

                decodedData = json.loads(string)

                #Check that data is loaded and if not wait with waiter function
                decodedData = waiter(decodedData, url)

                #Inside each observation:
                for i in range(0, len(decodedData['history']['observations'])):
                    tzname = decodedData['history']['observations'][i]['date']['tzname']
                    minStamp = decodedData['history']['observations'][i]['date']['min']
                    hStamp = decodedData['history']['observations'][i]['date']['hour']
                    dStamp = decodedData['history']['observations'][i]['date']['mday']
                    mStamp = decodedData['history']['observations'][i]['date']['mon']
                    yStamp = decodedData['history']['observations'][i]['date']['year']

                    #Ensure month and days are properly formatted with zero buffer:
                    if len(str(mStamp)) < 2:
                        mStamp = '0' + str(mStamp)
                    else:
                        mStamp = str(mStamp)

                    # Format day for timestamp
                    if len(str(dStamp)) < 2:
                        dStamp = '0' + str(dStamp)
                    else:
                        dStamp = str(dStamp)

                    #Put together string timestamp:
                    timeStamp = str(yStamp) + str(mStamp) + str(dStamp) + str(hStamp) + str(minStamp)

                    solarRadiation = decodedData['history']['observations'][i]['solarradiation']

                    solarRadiation = str(solarRadiation)

                    f.write(timeStamp + ',' + solarRadiation + '\n')


    f.close()

def waiter(decodedData, url):
    """
    Checks to ensure that json has loaded by checking to make sure data of interest exists.  Helpful for slow internet connections.
    :param decodedData: dictionary from json.loads(string)
    :param url: url to request from again if data has not loaded
    :return:
    """
    if 'history' in decodedData and 'observations' in decodedData['history']:
        return decodedData
    else:
        response = requests.get(url)
        #Wait 10 seconds
        time.sleep(10)
        print(response.raise_for_status(), " after 10 seconds.")
        string = response.text
        reloadedDecodedData = json.loads(string)
        if 'history' in reloadedDecodedData and 'observations' in reloadedDecodedData['history']:
            return reloadedDecodedData
        else:
            time.sleep(30)
            response = requests.get(url)
            #Wait 30 seconds
            time.sleep(10)
            print(response.raise_for_status(), " after 40 seconds.")
            string = response.text
            reloadedDecodedData = json.loads(string)
            if 'history' in reloadedDecodedData and 'observations' in reloadedDecodedData['history']:
                return reloadedDecodedData
            else:
                print("Still no keys after 50 seconds.")



# Main Function
if __name__ == '__main__':
    main()