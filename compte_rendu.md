# Compte rendu Antoine Reynaert


### Question 10

Pour1 récupérer tous les noms et coordonnées géographiques des points dont le nom ressemble  (au sens du LIKE SQL) à un argument nommé name_like, on effectue via la fonction python execute_query la reque SQL suivante : SELECT tags->'name', ST_X(geom), ST_Y(geom) FROM nodes WHERE tags->'name' LIKE '" + name_like + "';

Ainsi on propose le code suivant : 

```python
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
  
```

Qui, à l'éxécution, renvoie :

```bash
tonio@localhost:server$ python query_name_like.py 
<connection object at 0x7f2df85c4040; dsn: 'user=reynaera password=xxx dbname=osm host=postgresql.ensimag.fr', closed: 0> SELECT tags->'name', ST_X(geom), ST_Y(geom) FROM nodes WHERE tags->'name' LIKE 'Dom__ne _niversit____';
Domaine Universitaire 5.7695911 45.1881104
Domaine Universitaire 5.7611708 45.1898362
Domaine Universitaire 5.7588187 45.1935807
Domaine Universitaire 5.758102 45.1874865
Domaine Universitaire 5.7569834 45.1870508

```

### Question 11 : 

De la même maniére que dans la question précédente on effectue une requête qui récupére dans une bbox tous les linestring avec un tag highway ainsi que ce tag.
Une fois les linestring récupérés, on normalise les coordonnées de ses points afin de pouvoir dessiner ces linestring avec la fonction draw_linestring.
Un dictionnaire est également utilisé afin d'associer une couleur à certains types de highway.

On propose le code suivant (qui a été adapté pour les question suivante) : 

```python
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
  ```
Qui génére la figure_1 (en annexe)

### Question 12, 13, 14

Pour vérifier les paramètres entrés par la reque GET on léve les exceptions assosiés afin de renvoyer un message d'erreur expliquant l'erreur de paramètre.
Si il n'y a pas d'erreurs, tuile par tuile, le code vérifie si la tuile a déja été généré, si ce n'est pas le cas, grâce à la fonction présenté précédement ,elle est généré dans un dossier cache_tuile et nommé selon la bbox associé à la tuile.
Suite à cela la tuile est envoyé sur le serveur.

On propose pour cela les modifications suivantes du fichier WMSserver.py :


```python
class WMSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/wms"):
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            try :
                if params["request"]!=['GetMap']:
                    self.send_error(404, "request n'est pas GetMap")
                elif params["srs"]!=['EPSG:3857']:
                    self.send_error(404, "srs n'est pas EPSG:3857")
                else :
                    bbox = params["bbox"][0]
                    height, width = int(params["height"][0]), int(params["width"][0])
                    self.send_png_image(bbox, height, width)
                return 0

            except KeyError:
                self.send_error(404, "Erreur : Argument manquant")
        else:
            self.send_error(404, 'Erreur URL : %s' % self.path)

```
  
 ```python
 def send_png_image(self, bbox, height, width):
    self.send_response(200)
    self.send_header('Content-type', 'image/png')
    self.end_headers()
    filename = "cache_tuile/"+bbox+".png"
    try:
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())
    except FileNotFoundError:
        draw.map(bbox, height, width)
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

 ```
 
 Ainsi l'exécution du fichier index.html donne le résulat présenté figure 2 en annexe 
 
 On peut également lancer la requête html suivante qui renvoie le résultat présenté figure 3 en annexe :
 
 
  





