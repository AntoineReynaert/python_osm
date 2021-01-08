import database as db


query_list_highway = "SELECT DISTINCT tags->'highway' FROM ways WHERE tags?'highway';"

cursor = db.execute_query(query_list_highway)


with open("list_highway.text", "w") as file:
	for row in cursor: # Pour chaque ligne
		file.write(row[0] + "\n")



cursor.close()
db.close_connection()