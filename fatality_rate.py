import sys
import csv
import datetime

def main(argv):
  
  if len(argv) != 3:
        print("Usage: fatalityrate.py <file name> <PHU id>")
        sys.exit(1)
        
  filename = argv[1]
  code_number = argv[2]

  try:
    filename_fh = open(filename,encoding = "utf-8-sig")

  except IOError as err:
    print("Unable to open names file '{}' : {}".format(
                filename, err), file=sys.stderr)
    sys.exit(1)

  cases = list()
  csv_reader = csv.reader(filename_fh)
  
  for row in csv_reader:
    if (row[10] == code_number) and (row[9] == 'Yes') and (row[8] == 'Fatal'):
      cases.append(
        (datetime.datetime.strptime(row[1], '%Y-%m-%d'), row[8])
      )
      

  cases.sort(key=lambda x: x[0])


  print("Date,Outcome,Count")
  fatal_count = 0
  current_date = cases[0][0]

  for case in cases:
    if (case[0] != current_date):

      print("{:%Y-%m-%d},{},{}".format(current_date, 'Fatal', fatal_count))

      fatal_count = 0
      current_date = case[0]

    if (case[1] == 'Fatal'):
      fatal_count += 1
    
main(sys.argv)