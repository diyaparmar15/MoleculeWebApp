/*
Name: Diya Parmar
Student ID: 1168469
*/


#include "mol.h"

 
/*
This function should copy the values pointed to by element, x, y, and z into the atom stored at
atom. You may assume that sufficient memory has been allocated at all pointer addresses.
Note that using pointers for the function “inputs”, x, y, and z, is done here to match the
function arguments of atomget.
*/

void atomset( atom *atom, char element[3], double *x, double *y, double *z ) {


    //Copy values pointed to by elements into the atom struct
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    strcpy(atom->element, element);

}


/*
This function should copy the values in the atom stored at atom to the locations pointed to by
element, x, y, and z. You may assume that sufficient memory has been allocated at all pointer
addresses. Note that using pointers for the function “input”, atom, is done here to match the
function arguments of atomset.
*/

void atomget( atom *atom, char element[3], double *x, double *y, double *z ){

    //Copy values pointed from the atom struct into the elemnts being pointed to
    *x =atom->x;
    *y =atom->y;
    *z =atom->z;
    strcpy(element, atom->element);

}

/*
This function should compute the z, x1, y1, x2, y2, len, dx, and dy values of the bond and set
them in the appropriate structure member variables.
*/
void compute_coords( bond *bond ){

    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;

    bond->dx = bond->x2 - bond->x1;
    bond->dy = bond->y2 - bond->y1;

    bond->len = sqrt(bond->dx * bond->dx + bond->dy * bond->dy);

    if (bond->len != 0) {
        bond->dx = bond->dx / bond->len;
        bond->dy = bond->dy / bond->len;
    } else {
        bond->dx = 0;
        bond->dy = 0;
    }
    bond->z = ((bond->atoms[bond->a1].z + bond->atoms[bond->a2].z)) / 2; //ad and divide
}


/*
This function should copy the values a1, a2 and epairs into the corresponding structure
attributes in bond. You may assume that sufficient memory has been allocated at all pointer
addresses. Note you are not copying atom structures, only the addresses of the atom
structures.
*/
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom**atoms, unsigned char *epairs ){

    //Copy values pointed to by elements into the bond struct
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;

}


/*
This function should copy the structure attributes in bond to their corresponding arguments:
a1, a2 and epairs. You may assume that sufficient memory has been allocated at all pointer
addresses. Note you are not copying atom structures, only the addresses of the atom
structures.
*/
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom**atoms, unsigned char *epairs ){

    //Copy values pointed from the bond struct into the elemnts being pointed to    
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;

    //compute coords
    compute_coords(bond);

}


/*
This function should return the address of a malloced area of memory, large enough to hold a
molecule. The value of atom_max should be copied into the structure; the value of atom_no in
the structure should be set to zero; and, the arrays atoms and atom_ptrs should be malloced
to have enough memory to hold atom_max atoms and pointers (respectively). The value of
bond_max should be copied into the structure; the value of bond_no in the structure should be
set to zero; and, the arrays bonds and bond_ptrs should be malloced to have enough memory
to hold bond_max bonds and pointers (respectively).
*/
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){

    //Create new molecule temp variable
    molecule *newMolTemp = malloc(sizeof(struct molecule));

    //Pass the parameters through to equal each other
    newMolTemp->atom_max = atom_max;
    newMolTemp->atom_no = 0;

    //Memory allocation for temp variable
    newMolTemp->atoms = (atom*)malloc(sizeof(struct atom)*atom_max);

    //Error checking for NULL atoms
    if(newMolTemp->atoms ==NULL) {
        fprintf(stderr, "%s", "Memory allocation error, (newMolTemp->atoms = NULL");
        free(newMolTemp);
        return NULL;
    }

    newMolTemp->atom_ptrs = (atom**)malloc(sizeof(struct atom)*atom_max);

     //Error checking for NULL atom ptrs
    if(newMolTemp->atom_ptrs ==NULL) {
        fprintf(stderr, "%s", "Memory allocation error, (atom ptr = NULL");
        free(newMolTemp->atoms);
        free(newMolTemp);
        return NULL;
    }

    newMolTemp->bond_max = bond_max;
    newMolTemp->bond_no = 0;
    newMolTemp->bonds = (bond*)malloc(sizeof(struct bond)*bond_max);

     //Error checking for NULL bonds
    if(newMolTemp->bonds ==NULL) {
        fprintf(stderr, "%s", "Memory allocation error, (bonds = NULL)");
        free(newMolTemp->atom_ptrs);
        free(newMolTemp->atoms);
        free(newMolTemp);
        return NULL;
    }
    
    newMolTemp->bond_ptrs = (bond**)malloc(sizeof(struct bond)*bond_max);

    //Error checking for NULL bond ptrs
    if(newMolTemp->bond_ptrs ==NULL) {
        fprintf(stderr, "%s", "Memory allocation error, (bonds ptr = NULL)");
        free(newMolTemp->bonds);
        free(newMolTemp->atom_ptrs);
        free(newMolTemp->atoms);
        free(newMolTemp);
        return NULL;
    }

    return newMolTemp;
}


/*
This function should return the address of a malloced area of memory, large enough to hold a
molecule. Additionally, the values of atom_max, atom_no, bond_max, bond_no should be
copied from src into the new structure. Finally, the The arrays atoms, atom_ptrs, bonds and
bond_ptrs must be allocated to match the size of the ones in src. Finally, you should use
molappend_atom and molappend_bond (below) to add the atoms from the src to the new
molecule (note that this will also initialize the corresponding pointer arrays). You should re-use
(i.e. call) the molmalloc function in this function.
*/
molecule *molcopy( molecule *src ){

    //Memory allocation for temp variable
    molecule *newTempMol = molmalloc(src->atom_max, src->bond_max);

    //Loop through while i is less than the number of atoms
    for(int i = 0; i <src->atom_no; i++) {

        //Append the atoms into src using the molappend_atom function
        molappend_atom(newTempMol, &src->atoms[i]);
    }


    //Loop through while i is less than the number of bonds
    for(int i = 0; i <src->bond_no; i++) {

        //Append the bonds into src using the molappend_bond function
        molappend_bond(newTempMol, &src->bonds[i]);
    }
    return newTempMol;
}

/*
This function should free the memory associated with the molecule pointed to by ptr. This
includes the arrays atoms, atom_ptrs, bonds, bond_ptrs
*/
void molfree( molecule *ptr ){

    //Free all memory associated with a molecule
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

/*
This function should copy the data pointed to by atom to the first “empty” atom in atoms in the
molecule pointed to by molecule, and set the first “empty” pointer in atom_ptrs to the same
atom in the atoms array incrementing the value of atom_no. If atom_no equals atom_max, then
atom_max must be incremented, and the capacity of the atoms, and atom_ptrs arrays
increased accordingly. If atom_max was 0, it should be incremented to 1, otherwise it should be
doubled. Increasing the capacity of atoms, and atom_ptrs should be done using realloc so
that a larger amount of memory is allocated and the existing data is copied to the new location
*/
void molappend_atom( molecule *molecule, atom *atom ){

    //Check if atom_no is greater than atom_max
    if(molecule->atom_no == molecule->atom_max) {
        
        //if atom max is = to 0, increment the size of maximum atoms by 1
        if(molecule->atom_max == 0){
            molecule->atom_max += 1;
        }
        //otherwise double the space for atoms max
        else{
            molecule->atom_max *= 2;
        }

        //Reallocate for the atoms
        molecule->atoms = (struct atom*)realloc(molecule->atoms,sizeof(struct atom)* molecule->atom_max );

        //Error checking if atoms are NULL
        if(molecule->atoms == NULL) {
            fprintf(stderr, "%s", "Memory allocation error, (molappend atoms = NULL) Exiting...");
            molfree(molecule);
            exit(0);
        }

        molecule->atom_ptrs = (struct atom**)realloc(molecule->atom_ptrs,sizeof(struct atom*)* molecule->atom_max );
        
        //Error checking if atom_ptrs are NULL
        if(molecule->atom_ptrs == NULL) {
            fprintf(stderr, "%s", "Memory allocation error, (molappend atom ptrs = NULL) Exiting...");
            molfree(molecule);
            exit(0);
        }

        if(molecule->atom_max != 1){

            //Loop through the number of atoms and assign the atom pointers to the atoms
            for(int i = 0; i<molecule->atom_no; i++) {
                molecule->atom_ptrs[i] = &molecule->atoms[i];
            }
        }
    }

    //Copying data and pointing to the pointer in atom_ptr array
    molecule->atoms[molecule->atom_no] = *atom;
    molecule ->atom_ptrs[molecule->atom_no] = &(molecule->atoms[molecule->atom_no]);

    molecule->atom_no++;

}


/*
This function should operate like that molappend_atom function, except for bonds.
*/
void molappend_bond( molecule *molecule, bond *bond ){

    //Check if bond_no is greater than bond_max
    if(molecule->bond_no == molecule->bond_max) {
        
         //if bond max is = to 0, increment the size of maximum bonds by 1
        if(molecule->bond_max == 0){
            molecule->bond_max += 1;
        }
        //otherwise double the space for bond max
        else{
            molecule->bond_max *= 2;
        }

        //Reallocate for the bonds
        molecule->bonds = (struct bond*)realloc(molecule->bonds, sizeof(struct bond)*molecule->bond_max);

        //Error checking if bonds are NULL
        if(molecule->bonds == NULL) {
            fprintf(stderr, "%s", "Memory allocation error, (molappend bonds = NULL), Exiting...");
            molfree(molecule);
            exit(0);
        }

        //Memory reallocation for bond_ptrs to the size of bond_max
        molecule->bond_ptrs = (struct bond**)realloc(molecule->bond_ptrs,sizeof(struct bond*)* molecule->bond_max);


        //Error checking if bond ptrs are NULL   
        if(molecule->bond_ptrs == NULL) {
            fprintf(stderr, "%s", "Memory allocation error, (molappend bond ptrs = NULL) Exiting...");
            molfree(molecule);
            exit(0);
        }

        if(molecule ->bond_max != 1){

            //Loop through the number of bonds and assign the bond pointers to the bonds
            for(int i = 0; i<molecule ->bond_no; i++) {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
            }
        }
    }

    //Copying data and pointing to the pointer in bond_ptr array
    molecule->bonds[molecule->bond_no] = *bond;
    molecule ->bond_ptrs[molecule->bond_no] = &(molecule->bonds[molecule->bond_no]);

    molecule->bond_no++;

}


/*
This function should sort the atom_ptrs array in place in order of increasing z value. I.e.
atom_ptrs[0] should point to the atom that contains the lowest z value and
atom_ptrs[atom_no-1] should contain the highest z value. It should also sort the bond_ptrs
array in place in order of increasing “ z value”. Since bonds don’t have a z attribute, their z
value is assumed to be the average z value of their two atoms. I.e. bond_ptrs[0] should point
to the bond that has the lowest z value and bond_ptrs[atom_no-1] should contain the highest
z value.Hint: use qsort
*/
void molsort( molecule *molecule ){

    //Call the q-sort function by using the 2 helper functions created for comparing atoms and bonds
    //Sort the atoms and bonds
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), atom_comp);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), bond_comp);

}


/*
This function will allocate, compute, and return an affine transformation matrix corresponding
to a rotation of deg degrees around the x-axis. This matrix must be freed by the user when no-
longer needed.
*/
void xrotation( xform_matrix xform_matrix, unsigned short deg ){

    //Convert the degrees into radians by the following formula
    double radians = deg * (M_PI / 180);

    //Assign rotation matrix values for x
    xform_matrix[0][0] = 1.00;
	xform_matrix[0][1] = 0.00;
	xform_matrix[0][2] = 0.00;

	xform_matrix[1][0] = 0.00;
	xform_matrix[1][1] = cos(radians);
	xform_matrix[1][2] = -sin(radians);

	xform_matrix[2][0] = 0.00;
	xform_matrix[2][1] = sin(radians);
	xform_matrix[2][2] = cos(radians);

}


/*
This function will allocate, compute, and return an affine transformation matrix corresponding
to a rotation of deg degrees around the y-axis. This matrix must be freed by the user when no-
longer needed.
*/
void yrotation( xform_matrix xform_matrix, unsigned short deg ){

    //Convert the degrees into radians by the following formula
    double radians = deg * (M_PI / 180);

    //Assign rotation matrix values for y
    xform_matrix[0][0] = cos(radians);
	xform_matrix[0][1] = 0.00;
	xform_matrix[0][2] = sin(radians);

	xform_matrix[1][0] = 0.00;
	xform_matrix[1][1] = 1.00;
	xform_matrix[1][2] = 0.00;

	xform_matrix[2][0] = -sin(radians);
	xform_matrix[2][1] = 0.00;
	xform_matrix[2][2] = cos(radians);

}


/*
This function will allocate, compute, and return an affine transformation matrix corresponding
to a rotation of deg degrees around the z-axis. This matrix must be freed by the user when no-
longer needed.
*/
void zrotation( xform_matrix xform_matrix, unsigned short deg ){

    //Convert the degrees into radians by the following formula
    double radians = deg * (M_PI / 180);

    ////Assign rotation matrix values for z
    xform_matrix[0][0] = cos(radians);
	xform_matrix[0][1] = -sin(radians);
	xform_matrix[0][2] = 0.00;

	xform_matrix[1][0] = sin(radians);
	xform_matrix[1][1] = cos(radians);
	xform_matrix[1][2] = 0.00;

	xform_matrix[2][0] = 0.00;
	xform_matrix[2][1] = 0.00;
	xform_matrix[2][2] = 1.00;
}


/*
This function will apply the transformation matrix to all the atoms of the molecule by
performing a vector matrix multiplication on the x, y, z coordinates
*/

void mol_xform( molecule *molecule, xform_matrix matrix ) {

  //Create an atom array consisting 3 values: x,y,z
  double atom1[3];

  //Loop through the number of atoms and perform the matrix multiplication for each element
  for (int i = 0; i < molecule->atom_no; i++) {

     atom *newAtom = &molecule->atoms[i];

    //Assigning each array index with the value of x,y and z from the struct
     atom1[0] = molecule->atoms[i].x;
     atom1[1] = molecule->atoms[i].y;
     atom1[2] = molecule->atoms[i].z;

    //Perform matrix multiplication by multiplying and adding the elements in order of the matrix to acheive the total of x,y and z
    newAtom->x = (matrix[0][0] * atom1[0]) + (matrix[0][1] * atom1[1]) + (matrix[0][2] * atom1[2]);
    newAtom->y = (matrix[1][0] * atom1[0]) + (matrix[1][1] * atom1[1]) + (matrix[1][2] * atom1[2]);
    newAtom->z = (matrix[2][0] * atom1[0]) + (matrix[2][1] * atom1[1]) + (matrix[2][2] * atom1[2]);

  }
  for(int i = 0; i < molecule->bond_no; i++){
    compute_coords(&molecule->bonds[i]);
  }
}


/*
Helper Function to compare atoms to be used in Q-sort and used in the molsort function
*/
int atom_comp(const void *atom1, const void *atom2) {

    //Declare new atom pointers
    atom **atom_a;
    atom **atom_b;

    //Atoms pointers are equal to struct atom multiplied with atom1 and atom2
    atom_a = (atom **)atom1;
    atom_b = (atom **)atom2;

    //Checking if the z value from first atom is less than the other, if so return -1
    if (((*atom_a)->z) < ((*atom_b)->z)){
        return -1;
    }
    //otherwise if the z value from the first atom is greater than the other, return 1
    else if (((*atom_a)->z)> ((*atom_b)->z)){
        return 1;
    }
    else {
    return 0;
    }

  return ((*atom_a)->z - (*atom_b)->z);
}

/*
Helper Function to compare bonds to be used in Q-sort and used in the molsort function
*/
int bond_comp(const void *bond1, const void *bond2) {


  //Declare new bond pointers
  bond **bond_a;
  bond **bond_b;

  //Bond pointers are equal to struct bond multiplied with bond1 and bond2
  bond_a = (bond **)bond1;
  bond_b = (bond **)bond2;

   //Checking if the z value from first atom is less than the other, if so return -1
    if (((*bond_a)->z) < ((*bond_b)->z)){
        return -1;
    }
    //otherwise if the z value from the first atom is greater than the other, return 1
    else if (((*bond_a)->z)> ((*bond_b)->z)){
        return 1;
    }
    else {
    return 0;
    }

  return ((*bond_a)->z - (*bond_b)->z);
}

int main(){
    return 0;
}













