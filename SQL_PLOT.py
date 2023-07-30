example_query_1 = \
'''
select MATERIAL,CONF_Q FROM ORDERS_YTD
WHERE ACTUAL_FINISH_DATE='2023-02-06 00:00:00'
LIMIT 10;
'''

example_query_2 = \
'''
select Z.MATERIAL_GROUP,SUM(O.CONF_Q) as AMOUNT
FROM ORDERS_YTD O JOIN ZINVDLOD_UNIQUE Z
ON O.MATERIAL = Z.MATERIAL
GROUP BY Z.MATERIAL_GROUP
ORDER BY AMOUNT DESC
LIMIT 10;
'''



import sqlite3
import sys
import matplotlib.pyplot as plt


#--------------------------OPEN DATABASE--------------------------

try:
	outputfilename = sys.argv[1]
except:
	sys.exit("Usage: python SQL_PLOT.txt databasename.db")

conn = sqlite3.connect(outputfilename)
cur = conn.cursor()
print("Opened database successfully")

#-----------------------List available tables---------------------------

print("Tables:")
tables = cur.execute("select name from sqlite_master where type = 'table';")
table_list = tables.fetchall()
print(table_list)

#-----------------------List available columns for each table---------------------------

print("Schema:")
for table in table_list:
	print(table[0])
	table_info = cur.execute("pragma table_info({});".format(table[0]))
	print(table_info.fetchall())

#-------------------------Request user query-------------------------------

query = input("Enter query to plot: ")
if query=="example_query_1":
	query = example_query_1
elif query=="example_query_2":
	query = example_query_2
result = cur.execute(query)
output = result.fetchall()

#--------------------------CREATE PLOT OF DATA--------------------------

chart_type = input("Chart type: Choose from scatter, bar, or line: ")
n = len(output)
x_data = [item[0] for item in output]
y_data = [item[1] for item in output]

fig, ax = plt.subplots()
match chart_type:
	case 'scatter':
		ax.scatter(x_data, y_data)
	case 'bar':
		ax.bar(x_data, y_data)
	case 'line':
		ax.plot(x_data, y_data)
plt.show()

conn.close()

