# /*
# Name: Diya Parmar
# Student ID: 1168469
# */


import sys 
import MolDisplay 
from http.server import HTTPServer, BaseHTTPRequestHandler
from molsql import Database
import urllib
import cgi
import io
import json

# Initialize the database
db = Database(reset=True)
db.create_tables()

# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = ['/index.html', '/addRemove.html','/upload.html', '/select.html', '/display.html','/style.css', '/script.js', '/display.js']
class MyHandler(BaseHTTPRequestHandler):

    # do_GET method t presents a web-form when the path, “ /” is requested
    # and generates a 404 error otherwise
    def do_GET(self):
        print(self.path)
        if self.path in public_files:
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")

            fp = open( self.path[1:] ); 
            page = fp.read()
            fp.close()

            self.send_header("Content-length", len(page))

            self.end_headers()
            self.wfile.write(bytes(page, "utf-8"))

        elif (self.path == '/getMolecules'):
            # get molecules data
            molecules = db.getMolecules()
            if len(molecules) == 0:
                # database empty
                self.send_response(204) # No Content
                self.send_header("Content-type", "application/json")
                self.end_headers()
                return
            
            self.send_response(200) # OK
            self.send_header("Content-type", "application/json")
            self.end_headers()
            molecules_json = json.dumps(molecules)

            self.wfile.write(bytes(molecules_json, "utf-8"))

        # 404 error page
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))



    # do_POST method that sends an svg file to the client when the path “/molecule” is
    # requested and generates a 404 error otherwise. 
    def do_POST(self):

        if self.path == '/addElement':

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

            #print("here 82")

            print( postvars )

            elNum = postvars['elementNumber'][0]
            elCode = postvars['elementCode'][0]
            elName = postvars['elementName'][0]
            color_1 = postvars['color1'][0]
            color_2 = postvars['color2'][0]
            color_3 = postvars['color3'][0]
            radiusVal = postvars['radius'][0]

            db['Elements'] = (elNum, elCode, elName, color_1[1:], color_2[1:], color_3[1:], radiusVal)
            print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

            # message = "data received"
            self.send_response(200)
            self.path = "/addRemove.html"
            self.do_GET()
            # self.send_header('Content-type', 'text/plain')
            # self.send_header('Content-length', len(message))
            # self.end_headers()
            # self.wfile.write(bytes(message, "utf-8"))

        elif self.path == '/removeElement':

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

            print(postvars)

            elementDelete = str(postvars['remove_element_code'][0])
            print(elementDelete)

            db.test(elementDelete)

            print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() )

            message = "data received"

            self.send_response(200)
            self.path = "/addRemove.html";
            self.do_GET();
            # self.send_header('Content-type', 'text/plain')
            # self.send_header('Content-length', len(message))
            # self.end_headers()
            # self.wfile.write(bytes(message, "utf-8"))

        elif self.path == '/upload.html':
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            moleculeName = form['molName'].value
            SDFfile = form['sdfFile'].value

            print(moleculeName)
            print(SDFfile)

            # Validate SDF extention
            contentDispo = form['sdfFile'].headers['Content-Disposition']
            filename = cgi.parse_header(contentDispo)[1]['filename']
            ext = filename.split('.')[-1]
            
            if ext != 'sdf':
                # Handle invalid SDF file error
                response_body = "Error! SDF file is Invalid"
                response_length = len(response_body.encode('utf-8'))
                self.send_response(400)
                self.send_header("Content-type", "text/plain")
                self.send_header("Content-length", response_length)
                self.end_headers()
                self.wfile.write(response_body.encode('utf-8'))

                self.path = "/upload.html"
                self.do_GET()
                return

            # Create Molecule
            tFile = io.BytesIO(SDFfile)
            file = io.TextIOWrapper(tFile)

            # Add molecule into database
            db.add_molecule(moleculeName, file)

            self.path = "/upload.html"
            self.do_GET()

        elif self.path == "/viewMol":

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

            name = str(postvars['moleculeName'][0])

            # save molecule name globally
            MyHandler.molName = name
            print(name)

            message = "molecule was added";
            # response_length = len(response_body.encode('utf-8'))
            self.send_response(200);
            self.send_header("Content-type", "text/plain");
            self.send_header("Content-length", len(message));
            self.end_headers();
            self.wfile.write(message.encode('utf-8'))

         # 404 error page
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))


# # Web form 
# home_page = """
# <html>
#     <head>
#         <title> File Upload </title>
# </head>
# <body>
#      <h1> File Upload </h1>
#     <form action="molecule" enctype="multipart/form-data" method="post">
#         <p>
#             <input type="file" id="SDFfile" name="filename"/>
#         </p>
#         <p>
#             <input type="submit" value="Upload"/>
#         </p>
#     </form>
#     </body>
# </html>
# """

db = Database(reset=True)
db.create_tables()

MolDisplay.radius = db.radius();
MolDisplay.element_name = db.element_name();
MolDisplay.header += db.radial_gradients();

httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
httpd.serve_forever()
