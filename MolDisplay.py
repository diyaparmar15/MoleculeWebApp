# /*
# Name: Diya Parmar
# Student ID: 1168469
# */


import molecule;

# radius = { 'H': 25,
# 'C': 40,
# 'O': 40,
# 'N': 40,
# }

# element_name = { 'H': 'grey',
# 'C': 'black',
# 'O': 'red',
# 'N': 'blue',
# }

header = """<svg version="1.1" width="1000" height="1000"
xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""
offsetx = 500
offsety = 500



# Atom class consists init, str and svg methods
# Create an Atom class. This class should be a wrapper class for your atom class/struct in your C
# code. Objects of the Atom class should be initialized by calling an Atom( c_atom ) constructor
# method with an atom class/struct as its argument. The constructor should store the atom
# class/struct as a member variable. It should also initialize a member variable, z, to be the value
# in the wrapped class/struct.

class Atom ():

    def __init__ (self,c_atom ):
        self.atom = c_atom
        self.z = c_atom.z


    # Add an __str__ method to the Atom class. This method takes no arguments. You will need this
    # for debugging. Make this return a string that displays the element, x, y, and z values of the
    # wrapped atom.
    def __str__(self):
        return (f'Element: {self.atom.element}, x: {self.atom.x}, y: {self.atom.y,}, z: {self.atom.z}')

    # This svg method calculates x and y coordinates radius and colour of the atom being displayed
    def svg(self):
        cx = (self.atom.x * 100.0) + offsetx
        cy = (self.atom.y * 100.0) + offsety
        r = radius[self.atom.element]
        fill = element_name[self.atom.element]
        return ('  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (cx, cy, r, fill))





# Bond class consists of init, str and svg methods
# Create a Bond class. This class should be a wrapper class for your bond class/struct in your C
# code. Objects of the Bond class should be initialized by calling a Bond( c_bond ) constructor
# function with an bond class/struct as its argument. The constructor should store the bond
# class/struct as a member variable. It should also initialize a member variable, z, to be the value
# in the wrapped class/struct

class Bond():

    def __init__ (self,c_bond ):
        self.bond = c_bond
        self.z = c_bond.z

    # Add an __str__ method to the Bond class. This method takes no arguments. You will need this
    # for debugging. Make this return a string that displays the relevant information of the wrapped
    # bond.
    def __str__(self):
        return ' a1=' + str(self.bond.a1) + ' a2=' + str(self.bond.a2) + ' x1=' +str(self.bond.x1) + ' x2='+str(self.bond.x2)+ ' y1='+str(self.bond.y1)+' y2='+str(self.bond.y2)+' z='+str(self.bond.z)+' len='+str(self.bond.len)+' dx='+str(self.bond.dx)+' dy='+str(self.bond.dy)

    # The bond svg method calculates the x and y position cordinates for the bond to be displayed
    # the bonds are created in rectangular shapes which are known to be called polygons 
    #
    def svg(self):

        # Calculate the 4 coordinates with the offset for a bond illustration
        x1 = (self.bond.x1 * 100) + offsetx
        y1 = (self.bond.y1 * 100) + offsety
        x2 = (self.bond.x2 * 100) + offsetx
        y2 = (self.bond.y2 * 100) + offsety

        # Assign the difference in X and difference in Y into variables
        bdy = self.bond.dy
        bdx = self.bond.dx

        # Calculate the x coordiantes
        x1p = x1 + bdy * 10
        x1n = x1 - bdy * 10
        x2p = x2 + bdy * 10
        x2n = x2 - bdy * 10

        # Calculate the y coordinates
        y1p = y1 + bdx * 10
        y1n = y1 - bdx * 10
        y2p = y2 + bdx * 10
        y2n = y2 - bdx * 10

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x1n, y1p, x1p, y1n, x2p, y2n, x2n, y2p)


# Molecule Class consists of svg, str and parse methods

class Molecule(molecule.molecule):


    # Essentially this method combines that atoms array and bonds array into 1
    # adn then sorting by the z value of the atoms and bonds
    def svg (self):
        
        final = []

        i = 0
        j = 0

        # Assign the atom and bond numbers to variables
        atomNum = self.atom_no
        bondNum = self.bond_no

        # while the i iterator is less than the atomNum and j iterator is less than the bondNum
        while i < atomNum and j < bondNum:

            # make the current atom into the atom at i
            # make the current bond into the bond at j
            atom_cur = Atom (self.get_atom(i))
            bond_cur = Bond (self.get_bond(j))

            # if the z values of the atom are less than the bond
            if atom_cur.z < bond_cur.z:
                # append the current atom svg and increment the iterator i
                final.append(atom_cur.svg())
                i = i + 1

            #otherwise append the current bond svg and increment iterator j
            else:
                final.append(bond_cur.svg())
                j = j + 1

        # loop while the iterator i is less than the atom number
        while i < atomNum:
            atom_cur = Atom(self.get_atom(i))
            final.append(atom_cur.svg())
            i = i + 1
            
         # loop while the iterator j is less than the bond number
        while j < bondNum:
            bond_cur = Bond (self.get_bond(j))
            final.append(bond_cur.svg())
            j = j + 1
        
        # use the join method to combine all the atoms and bonds in one string
        string = ''.join(final)

        end = header + string + footer

        return end


    # This method that prints out the bonds and the atoms in the molecule for debugging
    # purposes. This method takes no arguments.
    def __str__(self):

        temp_str = ""

        #loop through all atoms
        for i in range(self.atom_no):
            temp_str = temp_str + Atom(self.get_atom(i)).__str__()

        #loop through all atoms
        for i in range(self.bond_no):
            temp_str = temp_str + Bond(self.get_bond(i)).__str__()

        return temp_str



    # The purpose of this method is to read a sdf file and parse all the relevant information
    # into th=o its respectuve location so it can be worked with to create the images
    # TA helped with this function (decode)
    def parse(self, file):

        items = []

        # skip the first 3 lines in the sdf file as there is no content to be read there
        file.readline()
        file.readline()
        file.readline()

        #split the files into each line
        fVar = file.readline().split()

        # scan in info in the sdf file to read the number of bonds and atoms
        n1 = fVar[0]
        n2 = fVar[1]

        #typecast the read string into an integer
        n1int = int(n1)
        n2int = int(n2)
        
        # Loop through until the number read for atoms in file  [0]
        for i in range(n1int):
            #convert string into bytes
            items = file.readline().split() 
            # .decode('utf-8')
            print(items)
            # append the x, y, z values for each atom
            self.append_atom(items[3], float(items[0]), float(items[1]), float(items[2]))


         # Loop through until the number read for bonds in file [1]
        for i in range(n2int):
            #convert string into bytes
            items = file.readline().split() # remove decode calls
            # .decode('utf-8')
             # append the x, y, z values for each bond
            self.append_bond(int(items[0]) - 1, int(items[1]) - 1, int(items[2]))


