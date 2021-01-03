import database as db

name_like = 'Dom__ne _niversit____'

cursor = db.execute_query("SELECT tags->'name', ST_X(geom), ST_Y(geom) FROM nodes WHERE tags->'name' LIKE '" + name_like + "';")

for row in cursor: # Pour chaque ligne
	try:
	    name, x, y = row[0], row[1], row[2] 
	    print(name, x, y) 
	except IndexError:
		print("Erreur requête")

cursor.close()
db.close_connection()