import sqlite3
import datetime
import re
from selenium import webdriver
import time

#requirements on local machine:  install selenium and sqlite3.

#--------------------------------------------------------Create/update SQL table--------------------------------------------------------

outputfilename = 'DATA.db'

conn = sqlite3.connect(outputfilename)
cur = conn.cursor()
print("Opened database successfully")
cur.execute("DROP TABLE IF EXISTS SPOILAGEREPORTS;")
cur.execute("CREATE TABLE SPOILAGEREPORTS (ORDERNUM TEXT,MATERIAL TEXT,CARDTYPE TEXT,ORDERQTY INTEGER,CODE4 TEXT,PIECES_SCRAPPED INTEGER,REPORTDATE DATE,PRESS TEXT,CAUSE TEXT,PROCESSES TEXT);")
print("Table created successfully")

#--------------------------------------------------------Pull Data from HTML Source----------------------------------------------

browser = webdriver.Chrome()
browser.get(#URL#)	#company's data log of spoilage reports (not shown for privacy)
dataPage = browser.page_source
time.sleep(5)
browser.close()

s = ""
for line in dataPage:
	s += line

s_len = len(s)

#Find starting point of code for creating the table with 10 columns.
begin = s.find("<tr")
end = s.find("/tr>")
sprime = s[begin:end+4]
c = sprime.count("<td")
while (c != 10):
	begin = end + 4
	end = s.find("/tr>", begin)
	sprime = s[begin:end+4]
	c = sprime.count("<td")

#Now, fill a list with all data.
data = []
while True:
	begin = s.find("<td", begin)
	end = s.find("/td>",begin)
	if (begin == -1 or end == -1):
		break
	item = s[begin:end]
	item = re.sub('<[^<>]*>', '', item)
	item = re.sub('&nbsp;<','', item)
	item = re.sub('<', '', item)
	data.append(item)
	begin = end + 4

#Now, create table as list[list[]].
rows = []
numdata = len(data)
i = 0
while (i < numdata):
	rows.append(data[i:i+10])
	i += 10

#-------------------------------------------------------Populate SQL table-------------------------------------------------------

print("loading data...")
placeholder = "?"+ 9 * ",?"
m = len(rows)
problem_rows = []
for i in range(0,m):
	try:
		#Convert date_strings to dates
		date_str = rows[i][6]
		month, day, year = date_str.split("/")
		reformatted_date = datetime.datetime(int(year), int(month), int(day))
		rows[i][6] = reformatted_date

		#Convert number strings to integers
		num_str = rows[i][3].replace(',','')
		num_str = re.sub('[^0-9]','', num_str)
		num_str2 = rows[i][5].replace(',','')
		num_str2 = re.sub('[^0-9]','', num_str2)
		rows[i][3] = int(num_str)
		rows[i][5] = int(num_str2)
	except:
		problem_rows.append(i)

#Remove rows with invalid number(s) or date records or without all entries.
for i in problem_rows:
	try:
		rows.remove(rows[i])
	except:
		rows.pop()
	

sql = "INSERT INTO SPOILAGEREPORTS (ORDERNUM,MATERIAL,CARDTYPE,ORDERQTY,CODE4,PIECES_SCRAPPED,REPORTDATE,PRESS,CAUSE,PROCESSES) VALUES ({});".format(placeholder)
cur.executemany(sql, rows)
conn.commit()

conn.close()






















	
