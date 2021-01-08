import drawer as d
import database as db

def map(bbox,height=1000,width=1000):

	couleurSVGA = {
	"secondary" : (0.0, 0.0, 0.0, 1.0),
	"unclassified" : (0.0, 0.0, 0.0, 1.0),
	"primary" : (0.0, 0.0, 0.0, 1.0),
	"footway":(0.0, 0.0, 0.0, 1.0),
	"track":(1.0, 0.0, 0.0, 1.0),
	"motorway":(0.0, 1.0, 0.0, 1.0),
	"proposed":(0.0, 0.0, 0.0, 1.0),
	"trunk":(0.0, 0.0, 0.0, 1.0),
	"tertiary":(0.0, 0.0, 0.0, 1.0),
	"bus_stop":(0.0, 0.0, 0.0, 1.0),
	"tertiary_link":(0.0, 0.0, 0.0, 1.0),
	"raceway":(0.0, 0.0, 0.0, 1.0),
	"motorway_link":(0.0, 0.0, 0.0, 1.0),
	"steps":(0.0, 0.0, 0.0, 1.0),
	"pedestrian":(0.0, 0.0, 1.0, 1.0),
	"secondary_link":(0.0, 0.0, 0.0, 1.0),
	"primary_link":(0.0, 0.0, 0.0, 1.0),
	"construction":(0.0, 0.0, 0.0, 1.0),
	"platform":(0.0, 0.0, 0.0, 1.0),
	"services":(0.0, 0.0, 0.0, 1.0),
	"trunk_link":(0.0, 0.0, 0.0, 1.0),
	"service":(0.0, 0.0, 0.0, 1.0),
	"cycleway":(1.0, 0.0, 1.0, 1.0),
	"living_street":(0.5, 0.5, 0.5, 1.0),
	"path":(1.0, 1.0, 0.0, 1.0),
	"residential":(0.0, 0.0, 0.0, 1.0),
	"road":(0.0, 1.0, 1.0, 1.0)
	}

	image = d.Image(height,width)

	x1, y1, x2, y2 = bbox.split(",")
	x1, y1, x2, y2 = float(x1),float(y1),float(x2),float(y2)

	if __name__ == "__main__":
		query_main = "SELECT linestring, tags->'highway' FROM ways WHERE tags?'highway'"
		query_box = "AND ST_Xmin(bbox)>"+str(x1)+"AND ST_Xmax(bbox)<"+str(x2)+" AND ST_Ymin(bbox)>"+str(y1)+" AND ST_Ymax(bbox)<"+str(y2)+";"
	
	else:
		query_main = "SELECT ST_Transform(linestring,3857), tags->'highway' FROM ways WHERE tags?'highway' "
		query_box = " AND ST_Xmin(ST_Transform(bbox,3857))>"+str(x1)+" AND ST_Xmax(ST_Transform(bbox,3857))<"+str(x2)+" AND ST_Ymin(ST_Transform(bbox,3857))>"+str(y1)+" AND ST_Ymax(ST_Transform(bbox,3857))<"+str(y2)+";"

	cursor = db.execute_query(query_main + query_box)

	for row in cursor:
		highway=row[1]
		listSommets=[((point.x-x1)/(x2-x1)*height, (y2-point.y)/(y2-y1)*width) for point in row[0]]
		try:
			image.draw_linestring(listSommets,couleurSVGA[highway])
		except KeyError:
			image.draw_linestring(listSommets,(0.0, 0.0, 0.0, 1.0)) # Par defaut le linstring est noir

	image.save("cache_tuile/"+bbox+".png")

	cursor.close()
	db.close_connection()

if __name__ == "__main__":
	map("5.6,45.2,5.7,45.3")

