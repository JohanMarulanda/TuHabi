import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json

def query_properties(filters):
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
    print("Estos son los resultados obtenidos: ")
    print(results)
    cursor.close()
    db.close()
    return results


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        if path == "/properties":
            query_components = dict(urlparse.parse_qsl(parsed_path.query))
            properties = query_properties(query_components)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(properties).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()