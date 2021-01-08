import database as db


query_list_waterway = "SELECT DISTINCT tags->'waterway' FROM ways WHERE tags?'waterway';"

cursor = db.execute_query(query_list_waterway)


with open("list_waterway.text", "w") as file:
	for row in cursor: # Pour chaque ligne
		file.write(row[0] + "\n")



cursor.close()
db.close_connection()