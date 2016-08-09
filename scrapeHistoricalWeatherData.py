__author__ = 'seanhendryx'

# This script finds daily mean temperatures from wunderground within specified date range and saves to csv:
# 1st column is date stamp in yearmonthday, 2nd column is temp in degrees F

 # Example: pip install [env name] [package name]
 # This will either install inside an environment, or create one
 # Let's install requests inside a virtualenv called *venv*
  #pip install -E python 2.7 beautifulsoup4

from urllib.request import urlopen

# from ^  import urlopen
from bs4 import BeautifulSoup

# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = open('wunder-data.txt', 'w')

# Iterate through year, month, and day
for y in range(2011, 2014):
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

      # Open wunderground.com url
      #http://www.wunderground.com/history/us/az/mount-lemmon
      url = "https://www.wunderground.com/history/airport/KTUS/"+str(y) + "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
      page = urlopen(url)

      # Get temperature from page
      soup = BeautifulSoup(page)
      #dayTemp = soup.body.nobr.b.string
      #my edit here using soup.findAll
      wx = soup.findAll(attrs={"class":"wx-value"})
      dayTemp = wx[0].string
      # Format month for timestamp
      if len(str(m)) < 2:
        mStamp = '0' + str(m)
      else:
        mStamp = str(m)

      # Format day for timestamp
      if len(str(d)) < 2:
        dStamp = '0' + str(d)
      else:
        dStamp = str(d)

      # Build timestamp
      timestamp = str(y) + mStamp + dStamp

      # Write timestamp and temperature to file
      f.write(timestamp + ',' + dayTemp + '\n')

# Done getting data! Close file.
f.close()
