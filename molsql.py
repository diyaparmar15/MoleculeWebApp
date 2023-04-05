# /*
# Name: Diya Parmar
# Student ID: 1168469
# */

import os;
import sqlite3;
from MolDisplay import Atom, Bond, Molecule
import MolDisplay


class Database: 

    # This constructor should create/open a database connection to a file in the local directory called
    # “molecules.db” and store it as a class attribute. If reset is set to True, it should first delete
    # the file “ molecules.db” so that a fresh database is created upon connection.

    def __init__(self, reset=False):

        #if reset is True, and if molecules.db exists in the directory, delete it using os.remove 
        if(reset == True):
            if os.path.exists( 'molecules.db' ):
                os.remove( 'molecules.db' )
            
        #connection with SQLite database file
        self.conn = sqlite3.connect( 'molecules.db' )


    
    # This method should create the tables described above. If any of the tables already exist, it
    # should leave them alone and not re-create them

    def create_tables(self):

        #create table called Elements
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Elements(
            ELEMENT_NO INTEGER NOT NULL,
            ELEMENT_CODE VARCHAR(3) NOT NULL PRIMARY KEY,
            ELEMENT_NAME VARCHAR(3) NOT NULL,
            COLOUR1 CHAR(6) NOT NULL,
            COLOUR2 CHAR(6) NOT NULL,
            COLOUR3 CHAR(6) NOT NULL,
            RADIUS DECIMAL(3) NOT NULL
        ); """)

        #create table called Atoms
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms(
            ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ELEMENT_CODE VARCHAR(3) NOT NULL REFERENCES Elements(ELEMENT_CODE),
            X DECIMAL(7,4) NOT NULL,
            Y DECIMAL(7,4) NOT NULL,
            Z DECIMAL(7,4) NOT NULL
        );""")

        #create table called Bonds
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS Bonds(
            BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            A1 INTEGER NOT NULL,
            A2 INTEGER NOT NULL,
            EPAIRS INTEGER NOT NULL
        );""")

        #create table called Molecules
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS Molecules(
            MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            NAME TEXT UNIQUE NOT NULL
        ); """)

        #create table called MoleculeAtom
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS MoleculeAtom(
            MOLECULE_ID INTEGER NOT NULL REFERENCES Molecules(MOLECULE_ID),
            ATOM_ID INTEGER NOT NULL REFERENCES Atoms(ATOM_ID),
            PRIMARY KEY(MOLECULE_ID,ATOM_ID)
        ); """)

        #create table called MoleculeBond
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS MoleculeBond(
            MOLECULE_ID INTEGER NOT NULL REFERENCES Molecules(MOLECULE_ID),
            BOND_ID INTEGER NOT NULL REFERENCES Bonds(BOND_ID),
            PRIMARY KEY(MOLECULE_ID,BOND_ID)
        ); """)


    # This method should provide a method to use indexing (i.e. [key]) to set the values in the table
    # named table based on the values in the tuple values (see example code, below).

    def __setitem__( self, table, values ):


        #create a string with the number of question marks as values in the tuple
        stringTemp = "(" + ",".join(["?"] * len(values)) + ")"

        #inserts the needed number of question marks in the string
        query = f"INSERT INTO {table} VAlUES {stringTemp}"

        #pass the values to the query and commit changed to the database
        self.conn.execute(query, values)
        self.conn.commit()

        


    # This method should add the attributes of the atom object (class MolDisplay.Atom) to the
    # Atoms table, and add an entry into the MoleculeAtom table that links the named molecule to
    # the atom entry in the Atoms table.

    def add_atom( self, molname, atom ):

        #assign the cursor to a variable
        c = self.conn.cursor()

        #query to insert the 4 elements into the table 
        query = "INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z) VALUES (?, ?, ?, ?)"
        #execute the values from the query and commit changes
        c.execute(query, (atom.atom.element, atom.atom.x, atom.atom.y, atom.atom.z))
        self.conn.commit()

        #the atomID is set to the lastrowid on the cursor
        atomID = c.lastrowid

        #query to select the molname
        query = "SELECT MOLECULE_ID FROM Molecules WHERE NAME=?" 
        #execute the value into molname
        c.execute(query, (molname,))
        #get first row returned
        mol = c.fetchone()[0]

        #query to insert the 2 elements into the table
        query = "INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES (?, ?)"
        #execute the values from the query and commit changes
        c.execute(query, (mol, atomID))
        self.conn.commit()



    # This method should add the attributes of the bond object (class MolDisplay.Bond) to the
    # Bonds table, and add an entry into the MoleculeBond table that links the named molecule to
    # the atom entry in the Bonds table.

    def add_bond( self, molname, bond ):

        #assign the cursor to a variable
        c = self.conn.cursor()

        #query to insert the 3 elements into the table 
        query = "INSERT INTO Bonds (A1, A2, EPAIRS) VALUES (?, ?, ?)"
        #execute the values from the query and commit changes
        c.execute(query, (bond.bond.a1, bond.bond.a2, bond.bond.epairs))
        self.conn.commit()

        #the bondID is set to the lastrowid on the cursor
        bondID = c.lastrowid

        #query to select the molname
        query = "SELECT MOLECULE_ID FROM Molecules WHERE NAME=?" 
        #execute the value into molname
        c.execute(query, (molname,))
        #get first row returned
        mol = c.fetchone()[0]

        #query to insert the 2 elements into the table
        query = "INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES (?, ?)"
        #execute the values from the query and commit changes
        c.execute(query, (mol, bondID))
        self.conn.commit()


    # This function should create a MolDisplay.Molecule object, call its parse method on fp, add
    # an entry to the Molecules table and call add_atom and add_bond on the database for each
    # atom and bond returned by the get_atom and get_bond methods of the molecule.

    def add_molecule( self, name, fp ):

        #create a molecule object
        molecule = Molecule()

        #parse the data from the file 
        molecule.parse(fp)

        #query to insert the name int the table Molevules
        query = "INSERT INTO Molecules (NAME) VALUES (?)"
        #execute teh value into the name being passed into the method, commit changes 
        self.conn.execute(query, (name,))
        self.conn.commit()

        #iterate through the atoms in the parsed molecule and add each atom to the database
        for i in range(molecule.atom_no):
            self.add_atom(name, Atom(molecule.get_atom(i)))

        #iterate through the bonds in the parsed molecule and add each bond to the database
        for j in range(molecule.bond_no):
            self.add_bond(name, Bond(molecule.get_bond(j)))


    # This method returns a MolDisplay.Molecule object initialized based on the molecule named
    # name. It will retrieve all the atoms in the database associated with the named molecule and
    # append_atom them to the Molecule object in order of increasing ATOM_ID.

    def load_mol( self, name ):

        #assign the cursor to a variable
        c = self.conn.cursor()

        #selects all of the atoms that are in that molecule
        c.execute("""SELECT *
                            FROM Atoms, MoleculeAtom, Molecules
                             WHERE Atoms.ATOM_ID = MoleculeAtom.ATOM_ID AND Molecules.NAME = ? AND Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
                            ORDER BY ATOM_ID ASC""",(name,))

        #fetch the results from above SQL commamd
        atoms = c.fetchall()

        #object of Molecule
        mol = Molecule()

        #adds the atoms in to the molecule object
        for atom in atoms:
            mol.append_atom(atom[1], atom[2], atom[3], atom[4])

        #selects all of the bonds that are in that molecule
        c2 = self.conn.cursor()
        c2.execute("""SELECT *
                            FROM Bonds, MoleculeBond, Molecules
                             WHERE Bonds.BOND_ID = MoleculeBond.BOND_ID AND Molecules.NAME = ? AND Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                            ORDER BY BOND_ID ASC""", (name,))

        #fetch the results from above SQL commamd
        bonds = c2.fetchall()

        #add each bond to them the molecule object
        for bond in bonds:
            mol.append_bond(bond[1], bond[2], bond[3])

        #return the object 
        return mol


    # This method returns a Python dictionary mapping ELEMENT_CODE values to RADIUS values based
    # on the Elements table.
    def radius( self ):

        #dictionary to store the results of the radius elements
        radiusElements = {}

        #query to select the element code and radius from Elements table
        query = "SELECT ELEMENT_CODE, RADIUS FROM Elements"
        #execute the query
        data = self.conn.execute(query)

        #iterate through the rows and fill the dictionary with the data collected
        for row in data.fetchall():
            radiusElements[row[0]] = row[1]

        #return the dictionary results
        return radiusElements


    # This method returns a Python dictionary mapping ELEMENT_CODE values to ELEMENT_NAME
    # values based on the Elements table

    def element_name( self ):

        #assign the cursor to a variable
        c = self.conn.cursor()

        #query to select the element code and element radius from Elements table
        c.execute("SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements")

        #fetch the results from select commamd above
        elementName = c.fetchall()

        #pass elementName into dict constructor creating a dictionary object
        dictionary = dict(elementName)

        #return the dictionary results
        return dictionary



    #This method returns a Python string consisting of multiple concatenations
    def radial_gradients( self ):

        #empty string
        gradients = ""

        #assign the cursor to a variable
        c = self.conn.cursor()

        #query to select the element code, element name, colour1 colour 2 and colour 3. from Elements table
        c.execute("SELECT ELEMENT_CODE, ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements")
        
        #iterate through the rows and fill the dictionary with the data that I used to teach 
        for row in c.fetchall():

            #string var, format of svg files
            gradient = """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
              <stop offset="0%%" stop-color="#%s"/>
              <stop offset="50%%" stop-color="#%s"/>
              <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (row[1], row[2], row[3], row[4])
            gradients += gradient

        #return the string
        return gradients


    def test(self, remove):
        cursor = self.conn.cursor()
        cursor.execute("""DELETE FROM Elements WHERE ELEMENT_NAME = ?""", (remove,))
        self.conn.commit()


    def getMolecules(self):
        # Open Connection
        conn = sqlite3.connect('molecules.db')
        cursor = conn.cursor()

        # Select Molecule IDs, Names, Bond Counts, and Atom Counts
        query1 = """SELECT Molecules.MOLECULE_ID, Molecules.NAME, COUNT(DISTINCT Bonds.BOND_ID), COUNT(DISTINCT Atoms.ATOM_ID)
                    FROM Molecules
                    JOIN MoleculeBond ON Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                    JOIN Bonds ON MoleculeBond.BOND_ID = Bonds.BOND_ID
                    JOIN MoleculeAtom ON Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
                    JOIN Atoms ON MoleculeAtom.ATOM_ID = Atoms.ATOM_ID
                    GROUP BY Molecules.MOLECULE_ID"""
        cursor.execute(query1)
        molecule_results = cursor.fetchall()

        moleculeData = []

        # Loop Through Molecules
        for molecule_result in molecule_results:
            name = molecule_result[1]
            bond_count = molecule_result[2]
            atom_count = molecule_result[3]

            # Create Molecule Dictionary
            molecule = {
                "name": name,
                "bond_count": bond_count,
                "atom_count": atom_count
            }

         
            moleculeData.append(molecule)

        cursor.close()
        conn.close()

        return moleculeData
    
    def molExists(self, name):
        
        cursor = self.conn.cursor()
        query = "SELECT * FROM Molecules WHERE NAME = ?"
        cursor.execute(query, (name,))
   
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True


