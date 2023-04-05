/*
 Name: Diya Parmar
 Student ID: 1168469 
*/

$(document).ready(function () {
    $.ajax({
        url: '/getMolecules',
        type: 'GET',
        dataType: 'json', 
        success: function (data, status, xhr) {
            var molList = $('#molecule-list'); 
            molList.empty(); 
            if (xhr.status === 204) {
                console.log("Database Empty")
                var selectEmpty = $('<div class="empty-bar"></div>').css('white-space', 'pre-line').text("To select and view a molecule, you have to upload a file first!\nClick 'Upload SDF' from the navigation bar above!");
                selectEmpty.on('click', function() {
                    window.location.href = 'upload.html';
                });
                molList.append(selectEmpty);
            }
            else {
                var molecules = data; 
                console.log("SUCEEDED");

                for (var i = 0; i < molecules.length; i++) {
                    var molecule = molecules[i];

                // create new molecule
                //var molAdd = $('<div class="molecule-bar"></div>');

                var molecule = molecules[i];

                var moleculeBar = $('<div class="molecule-bar"></div>');
                var moleculeButton = $('<button class="molecule-name"></button>').text(molecule.name);
                moleculeBar.append(moleculeButton);

                var moleculeCounts = $('<div class="molecule-counts"></div>').hide();
                moleculeCounts.append($('<span class="molecule-atoms"></span>').text('Atoms: ' + molecule.atom_count + ' \n'));
                moleculeCounts.append($('<span class="molecule-bonds"></span>').text('Bonds: ' + molecule.bond_count + ' \n'));

                // add hover event listeners to show/hide the molecule counts container
                moleculeButton.hover(function() {
                    $(this).next('.molecule-counts').show();
                }, function() {
                    $(this).next('.molecule-counts').hide();
                });

                
                moleculeBar.append(moleculeCounts);

                moleculeBar.on('click', function () {
                    var moleculeName = $(this).find('.molecule-name').text();
                    molProcess(moleculeName);
                });

                
                molList.append(moleculeBar);
                }
            }
        },
        error: function(xhr, textStatus, errorThrown){
            console.log(xhr.status);
            console.log(errorThrown);
        }
    });
    function molProcess(moleculeName) {
        $.ajax({
          url: '/viewMol', 
          type: 'POST',
          data: {'moleculeName': moleculeName},
          success: function (response) {
            console.log(response);
            window.location.href = '/display.html'; 
          },
          error: function (xhr, textStatus, errorThrown) {
            console.log(xhr.status);
            console.log(errorThrown);
          }
        });
    }
});