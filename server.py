# /*
# Name: Diya Parmar
# Student ID: 1168469
# */

#imports

import sys 
import MolDisplay 
from http.server import HTTPServer, BaseHTTPRequestHandler
from molsql import Database
import urllib
import cgi
import io
import json
import molecule

# Initialize the database
db = Database(reset=True)
db.create_tables()
# db['Elements'] = (1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25)
# db['Elements'] = (6, 'C', 'Carbon', '808080', '010101', '000000', 40)
# db['Elements'] = (7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40)
# db['Elements'] = (8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40)

# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = ['/index.html', '/addRemove.html','/upload.html', '/select.html', '/display.html','/style.css', '/script.js', '/display.js']
class MyHandler(BaseHTTPRequestHandler):

    currDisplayMol = ""
    xRot = 0
    yRot = 0
    zRot = 0

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

        #path that gets the molecules from the uploaded ones
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

        #path for generating the molecule picture
        elif(self.path == "/moleculeFormation"):

            self.send_response( 200 ) 
            self.send_header("Content-type", "image/svg+xml") 
            self.end_headers() 
            length = int(self.headers.get('Content-Length', 0)) 

            #generate svg
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()

            #load the database
            name = MyHandler.currDisplayMol
            mol = db.load_mol(name)
            print(mol)
            
            #checking which side is being rotated, once identified,
            #rotate that molecule on its respective axis
            #xRotation
            if (MyHandler.xRot != 0):
                print(MyHandler.xRot)
                mx = molecule.mx_wrapper(int(MyHandler.xRot), 0, 0)
                mol.xform( mx.xform_matrix )
                print(mol)

            #yRotation
            if (MyHandler.yRot != 0):
                mx = molecule.mx_wrapper(0, int(MyHandler.yRot), 0)
                mol.xform( mx.xform_matrix )
                print(mol)

            #zRotation
            if (MyHandler.zRot != 0):
                mx = molecule.mx_wrapper(0, 0, int(MyHandler.zRot))
                mol.xform( mx.xform_matrix )
                print(mol)

            #sort the molecule and write it out
            mol.sort()
            self.wfile.write( bytes( mol.svg(), "utf-8" ) )

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

        #path to remove an element in the databse
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

        #path to upload a file 
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

            #SDF extention validation
            contentDispo = form['sdfFile'].headers['Content-Disposition']
            filename = cgi.parse_header(contentDispo)[1]['filename']
            ext = filename.split('.')[-1]
            
            if ext != 'sdf':
                #if the file entered is not a .sdf
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

        # path for rotating the viewing the molecule
        elif self.path == "/viewMol":

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

            name = str(postvars['moleculeName'][0])

            #global mol name 
            MyHandler.currDisplayMol = name
            
            mol = MolDisplay.Molecule();
            mol = db.load_mol( name );
            mol.sort();

            MolDisplay.radius = db.radius();
            MolDisplay.element_name = db.element_name();
            MolDisplay.header += db.radial_gradients();

            svg = mol.svg();

            # message = "molecule was added";
            # response_length = len(response_body.encode('utf-8'))
            self.send_response(200);
            self.send_header("Content-type", "text/plain");
            self.send_header("Content-length", len(svg));
            self.end_headers();
            self.wfile.write(svg.encode('utf-8'))

        #path for rotating the molecules
        elif (self.path == "/rotations"):

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            postvars = urllib.parse.parse_qs(body.decode('utf-8'))
       
            side = postvars['side'][0]
            #check the side being rotated followed by rotating
            if(side == 'sideY'):
                MyHandler.yRot = (MyHandler.yRot + 10) % 360
            elif(side == 'sideX'):
                MyHandler.xRot = (MyHandler.xRot + 10) % 360
            elif(side == 'sideZ'):
                MyHandler.zRot = (MyHandler.zRot + 10) % 360

    
            response_body = "Molecule Rotation Success"
            response_length = len(response_body.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", response_length)
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))

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
