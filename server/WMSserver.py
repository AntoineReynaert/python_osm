#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import draw

PORT_NUMBER = 4242


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

    def send_plain_text(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

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

    def send_html_file(self, filename):
        self.send_response(200)
        self.end_headers()
        self.serveFile(filename)


if __name__ == "__main__":
    try:
        # Ici on crée un serveur web HTTP, et on affecte le traitement
        # des requêtes à notre releaseHandler ci-dessus.
        server = HTTPServer(('', PORT_NUMBER), WMSHandler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)

        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()
