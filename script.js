/*
 Name: Diya Parmar
 Student ID: 1168469 
*/

/* javascript to accompany jquery.html */

// $(document).ready( 
//     /* this defines a function that gets called after the document is in memory */
//     function()
//     {

//       /* add a click handler for our button */
//       $("#button").click(
//         function()
//         {
//       /* ajax post */
//       $.post("/form_handler.html",
//         /* pass a JavaScript dictionary */
//         {
//           name: $("#name").val(),	/* retreive value of name field */
//           extra_info: "some stuff here"
//         },
//         function( data, status )
//         {
//           alert( "Data: " + data + "\nStatus: " + status );
//         }
//       );
//         }
//       );
//     }
//   );





$(document).ready(
    function(){
        $("#add_element").click(function () {

            console.log("Heree");
    
            $("form").submit(function (event) {
                event.preventDefault();
        
            });
    
            /* ajax post */
            $.post("/upload-form.html", {
                /* pass a JavaScript dictionary */
                eNumber: $("#elementNumber").val(),
                eCode: $("#elementCode").val(),
                eName: $("#elementName").val(),
                col1: $("#color1").val(),
                col2: $("#color2").val(),
                col3: $("#color3").val(),
                rad: $("#radius").val()
            }, function( data, status )
                    {
                      alert( "Data: " + data + "\nStatus: " + status );
                    }).done(function (data) {
                console.log(data);
                alert("Submission succeeded!");
            }).fail(function (xhr, status, error) {
                console.log(xhr)
                alert("Submission failed!");
            });
    
    
            $("#remove_element").click(function () {
    
                $("form").submit(function (event) {
                    event.preventDefault();
                });
    
                /* ajax post */
                console.log("removing");
                $.post("/upload-form.html", {
                    /* pass a JavaScript dictionary */
                    //operation: "remove",
                    reCode: $("#remove_element_code").val(),
                }).done(function (data) {
                    alert("Submission was successful!!");
                }).fail(function (xhr, status, error) {
                    console.log(xhr)
                    alert("Submission has failed!");
                });
            });
    
        })
    }
);


