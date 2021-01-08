import database as db

name_like = 'Dom__ne _niversit____'
## la requête ne marche pas avec "%""


query_coord = "SELECT tags->'name', ST_X(geom), ST_Y(geom) FROM nodes WHERE tags->'name' LIKE '" + name_like + "';"

query_list_highway = "SELECT DISTINCT tags->'highway' FROM ways WHERE tags?'highway';"

cursor = db.execute_query(query_main + query_box)

for row in cursor: # Pour chaque ligne
	try:
	    name, x, y = row[0], row[1], row[2] 
	    print(name, x, y) 
	except IndexError:
		print("Erreur requête")

cursor.close()
db.close_connection()