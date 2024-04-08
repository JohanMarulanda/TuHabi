import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json
import sys
from pathlib import Path

root_directory = Path(__file__).parent.parent
sys.path.append(str(root_directory))
from utils.utils import validate_filters

def query_properties(filters):
    try:
        filters = validate_filters(filters)
    except ValueError as e:
        return {'error': str(e)}

    try:
        query = """
        SELECT p.address, p.city, p.price, p.description, p.year, s.name AS state
        FROM property p
        JOIN (
            SELECT sh.property_id, sh.status_id, MAX(sh.update_date) AS latest_update
            FROM status_history sh
            GROUP BY sh.property_id
        ) AS latest_sh ON p.id = latest_sh.property_id
        JOIN status s ON latest_sh.status_id = s.id
        WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')
        """
        
        params = []
        if 'year' in filters:
            query += " AND p.year = %s"
            params.append(filters['year'])
        if 'city' in filters:
            query += " AND p.city = %s"
            params.append(filters['city'])
        if 'state' in filters:
            query += " AND s.name = %s"
            params.append(filters['state'])
        
        db = mysql.connector.connect(
            host='3.138.156.32',
            port='3309',
            user='pruebas',
            password='VGbt3Day5R',
            database='habi_db'
        )

        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return results
    except Exception as e:
        # Aquí capturamos cualquier otro error que pueda ocurrir al interactuar con la DB
        return {'error': 'Error al consultar la base de datos', 'details': str(e)}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/properties"):
            self.handle_properties()
        else:
            self.send_error(404, "Not Found")

    def handle_properties(self):
        try:
            query_components = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            # Convertir query_components en un dict simple
            filters = {k: v[0] for k, v in query_components.items()}
            properties = query_properties(filters)
            if 'error' in properties:
                self.send_response(400)  # Bad Request
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(properties).encode())
            else:
                self.send_response(200) # Request Valida
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(properties).encode())
        except Exception as e:
            self.send_response(500)  # Internal Server Error
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Error interno del servidor', 'details': str(e)}).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass  # Aquí se captura la señal de interrupción 
    finally:
        httpd.server_close()  # Se asegura de cerrar el servidor de forma limpia
        print('Stopping server...')

if __name__ == '__main__':
    run()