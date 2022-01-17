#!/usr/bin/env python
import sys
import csv
import datetime

def main(argv):
  
  if len(argv) != 4:
        print("Usage: total_school_covid_cases.py <file name> <start reported date><end reported date>")
        sys.exit(1)
        
  filename = argv[1]

  try:
    filename_fh = open(filename,encoding = "utf-8-sig")

  except IOError as err:
    print("Unable to open names file '{}' : {}".format(
                filename, err), file=sys.stderr)
    sys.exit(1)

  start_dt = None
  end_dt = None

  for format in ['%Y-%m-%dT%H:%M:%S']:
    try:
      start_dt = datetime.datetime.strptime(argv[2], format)
      end_dt = datetime.datetime.strptime(argv[3], format)
    except:
      pass

  #error check for valid format of date and time
  if (start_dt is None or end_dt is None):
    print ("Error: Not valid date and time format. Please try again")
    sys.exit(1)

  #check if start date doesn't come after the end date
  if ((datetime.datetime.strptime(argv[2], '%Y-%m-%dT%H:%M:%S')) > (datetime.datetime.strptime(argv[3], '%Y-%m-%dT%H:%M:%S'))):
    print ("Error: Start date should be less than end date")
    sys.exit(1)

  cases = list()
  
  csv_reader = csv.reader(filename_fh)
  next(csv_reader,None)

  for row in csv_reader:
    
    #Only store data which is between the reporting period
    
    if ((datetime.datetime.strptime(row[2], '%Y-%m-%dT%H:%M:%S')) >= start_dt and (datetime.datetime.strptime(row[2], '%Y-%m-%dT%H:%M:%S')) <= end_dt):
    
      #Faulty dataset corrected: Some school names have unnecessary commas which increases the number of columns. Eg: "St," instead of St
      row[5] = row[5].replace(',','')
      cases.append((datetime.datetime.strptime(row[2], '%Y-%m-%dT%H:%M:%S'), row[4], row[10], row[5], row[3]))

  cases.sort(key=lambda x: x[0])

  #check the availability of data between the selected period
  if not cases:
    print("No data available between the selected period")
    sys.exit(1)

  list1 = []
  list2 = []
  list3 = []

  #Variable declared to prevent double count of the same data
  Check = True

  total_cases = 0

  new_list = cases

  print("School_id,School,School_board,Total_Cases")
  
  for count in new_list:
    total_cases = 0

    #loop to prevent double counting of same elements
    #if no same element is found the check is True
    for i in range(0, len(list1),1):
      if(count[1] == list1[i]):
        if(count[3] == list2[i]):
          if (count[4] == list3[i]):
            Check = False
            break
          else:
            Check = True
        else:
          Check = True
      else:
        Check = True
        
    if (Check == True):
      for case in cases:
        
        #Check if School id, school names and school boards are same
        if (count[1] == case[1] and count[3] == case[3] and count[4] == case[4]):
          total_cases = total_cases + int(case[2])

      print("{},{},{},{}".format(count[1], count[3], count[4], total_cases))

    #elements which have been used from the data are stored in the lists
    list1.append(count[1])  #School ids are stored
    list2.append(count[3])  #School names are stored
    list3.append(count[4])  #School boards are stored

##
## Call our main function, passing the system argv as the parameter
##

main(sys.argv)

#
#   End of Script
#
