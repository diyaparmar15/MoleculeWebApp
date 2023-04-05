/*
 Name: Diya Parmar
 Student ID: 1168469 
*/

$(document).ready(function() {
    $('#uploadBtn').on('click', function(e) {
        e.preventDefault();

        var moleculeName = $('#molName').val().trim();
        var fileSDF = $('#sdfFile')[0].files[0];
        var regex = /^[a-zA-Z0-9_\-]+$/;

        if (!moleculeName.match(regex)) {
            alert('Invalid name for the Molecule');
            return;
        }

        var formData = new FormData();
        formData.append('molName', moleculeName);
        formData.append('sdfFile', fileSDF);

        $.ajax({
            url: 'upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Element added");
            },
            error: function(xhr, status, error) {
                if (xhr.status === 400) {
                    alert("Submission Invalid.");
                } else {
                    alert("Error: " + error);
                }
                console.log(xhr.responseText);
            }
        });
    });
});

