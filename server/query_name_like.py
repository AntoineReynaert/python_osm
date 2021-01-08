import database as db

def query_name_like(name_like):

	query = "SELECT tags->'name', ST_X(geom), ST_Y(geom) FROM nodes WHERE tags->'name' LIKE '" + name_like + "';"

	cursor = db.execute_query(query)

	for row in cursor: # Pour chaque ligne
		try:
		    name, x, y = row[0], row[1], row[2] 
		    print(name, x, y) 
		except IndexError:
			print("Erreur requête")

	cursor.close()
	db.close_connection()

	return 0

if __name__ == '__main__':

	name_like = "Dom__ne _niversit____" ## la requête ne marche pas avec "%""
	query_name_like(name_like)