/*
 Name: Diya Parmar
 Student ID: 1168469 
*/


$(document).ready(function () {
    //ajax GET request to get the molecules uploaded by the user
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

                // add hover event listeners to show/hide the molecule counts container which consists atom and bond counts
                moleculeButton.hover(function() {
                    $(this).next('.molecule-counts').show();
                }, function() {
                    $(this).next('.molecule-counts').hide();
                });

                
                moleculeBar.append(moleculeCounts);

                //find out which element button was clicked then process that molecule
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
    //function to process the molecule the user selected
    function molProcess(moleculeName) {
        $.ajax({
          url: '/viewMol', 
          type: 'POST',
          data: {'moleculeName': moleculeName},
          success: function (data) {
            console.log("IN Suc")
            console.log(data);
            $("#image").empty();
            $("#image").append(data);
            $('html, body').animate({
                scrollTop: $(document).height()
              }, 1000); 
          },
          error: function (xhr, textStatus, errorThrown) {
            console.log("IN Err")
            console.log(xhr.status);
            console.log(errorThrown);
          }
        });
    }
});


$(document).ready( 

    function(){
        
   //ajax GET request to display the molecule image
    $.ajax({
        url: "/moleculeFormation",
        type: "GET",
        dataType: "text",
        success: function(data, status, xhr){
            //empty the div and resize the image
            $("#image").empty()
            data = data.replace('width="1500"', 'width="600"');
            data = data.replace('height="1500"', 'height="600"');
            data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
            //add svg to div
            $("#image").append(data)
        }
    });

    //button for Rotate X was clicked
    $("#xRotation").click(function(){
        var side = "sideX";
        rotate(side)
        {
            $.ajax({
                url: "/moleculeFormation",
                type: "GET",
                dataType: "text",
                success: function(data, status, xhr){
                    //empty the div and resize the image
                    $("#image").empty()
                    data = data.replace('width="1500"', 'width="600"');
                    data = data.replace('height="1500"', 'height="600"');
                    data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                    //add svg to div
                    $("#image").append(data)
                }
            });
        }
    }),

    //button for Rotate Y was clicked
    $("#yRotation").click(function(){
        //call rotate method
        var side = "sideY";
        rotate(side)
        // GET request to display molecule on screen
        {
            $.ajax({
                url: "/moleculeFormation",
                type: "GET",
                dataType: "text",
                success: function(data, status, xhr){
                    //clear div
                    $("#image").empty()
                    //resize svg
                    data = data.replace('width="1500"', 'width="600"');
                    data = data.replace('height="1500"', 'height="600"');
                    data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                    //add svg to div
                    $("#image").append(data)
                }
            });
        }
    }),

    //button for Rotate Z was clicked
    $("#zRotation").click(function(){
        //call rotate method
        var side = "sideZ";
        rotate(side)
        {
            $.ajax({
                url: "/moleculeFormation",
                type: "GET",
                dataType: "text",
                success: function(data, status, xhr){
                    //empty the div
                    $("#image").empty()
                    //resize the image
                    data = data.replace('width="1500"', 'width="600"');
                    data = data.replace('height="1500"', 'height="600"');
                    data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                    //add the svg to div
                    $("#image").append(data)
                }
            });
        }
    })

    }
)

// POST request sending the rotation info 
function rotate(side){
    $.ajax({
        url: '/rotations', 
        type: 'POST',
        data: {'side': side},
        success: function (response) {
            console.log("Rotation Successful.");
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("Error in Rotation.");
        }
    });
}