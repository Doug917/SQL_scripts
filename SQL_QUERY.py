
#--------------------------------------------------------MAIN----------------------------------------------------------------------

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

if len(sys.argv) != 2:
	sys.exit("Usage: python SQL_QUERY.txt inputdatabase.db")
else:
	inputfilename = sys.argv[1]


conn = sqlite3.connect(inputfilename)
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

f = open('query_results.txt', 'a', newline="")
is_query = "y"
while is_query.lower() == "y":
	query = input("Enter query: ")
	if query == "example_query_1":
		query = example_query_1
	elif query == "example_query_2":
		query = example_query_2
	result = cur.execute(query)
	output = result.fetchall()
	#Write results to query log.
	f.write(20 * '-'+"\n")
	f.write(query + "\n")
	for line in output:
		f.write(',  '.join([str(item) for item in line]))
		f.write("\n")
	is_query = input("Run new query? (y/n): ")
conn.close()
f.close()



