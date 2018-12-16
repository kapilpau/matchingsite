// When the document has finished loading, an AJAX query is sent to get the list of hobbies from the database
// and that list is added to the table of hobbies
$(document).ready(function (e) {
    $('#addItemFormDiv').hide();
    $.ajax({
        url: 'hobbies/',
        type: 'GET',
        success: function (data) {
            $.each(JSON.parse(data), function (i, item) {
                let html = "";
                html += "<div id='" + item.pk + "' align='center' style='margin: 0 auto'>";
                html += "<div class='card' style='width: 15rem;'>";
                html += "<div class='card-body'>";
                html += "<div id='" + item.pk + "-name'>"+item.fields.name+"</div>";
                html += "<div id='" + item.pk + "-icons'><i class='material-icons' title='delete' onclick='doDelete("+item.pk+")'>clear</i></div>";
                html += "</div>";
                html += "</div>";
                html += "</div>";
                $('#product-table').append(html);
            });
        },
        failure: function (data) {
            console.log("Failure");
            console.log(data);
            alert(data);
        }
    });
});


// When the admin presses the delete button, they are prompted with a confirm box. When they confirm, an AJAX request
// is sent to the server, to delete the entry from the database
function doDelete(id) {
    if(confirm("Are you sure you want to remove " + document.getElementById(id + "-name").textContent)){
        $.ajax({
            url: 'deleteHobby/',
            contentType: "application/json",
            type: 'DELETE',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data: {
                'id': id
            },
            success: function (data) {
                $('#' + id).remove()
            }
        })
    }
}

// When the + is clicked, the add form is displayed and the + is hidden
function showForm() {
        $('#addItemFormDiv').show();
        $('#addBtn').hide();
}

// When the cancel button is clicked, the add form is hidden and the + is displayed
function hideForm() {
    $('#addItemFormDiv').hide();
    $('#addBtn').show();
}


// When the admin presses the add button, the value of the name field is check to ensure it is not equal to Name or isn't
// blank, and then it is submitted as an AJAX query. If that returns successfully then the hobby is appended to the table
function doAdd() {
        let name = $('#addFormNameField').val();
        if (name === "" || name === "Name"){
            document.getElementById('addFormNameField').style.borderColor = 'red';
            return;
        }
        var csrftoken = Cookies.get('csrftoken');
        let data = {
            'name': name,
            csrfmiddlewaretoken: csrftoken
        };
        $.ajax({
        url: 'addHobby/',
        type: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        data: data,
        success: function (data) {
            let html = "";
            html += "<tr id='" + data.id + "'>";
            html += "<td id='" + data.id + "-name'>"+name+"</td>";
            html += "<td id='" + data.id + "-icons'><i class='material-icons' title='delete' onclick='doDelete("+data.id+")'>clear</i></td>";
            html += "</tr>";
            $('#product-table').append(html);
            $('#addItemFormDiv').hide();
            $('#addBtn').show();
        },
        failure: function (data) {
            console.log("Failure");
            console.log(data);
            alert(data);
        }
    });
}
