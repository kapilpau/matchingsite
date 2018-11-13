$(document).ready(function (e) {
    $('#addItemFormDiv').hide();
    $('#editItemFormDiv').hide();
    $.ajax({
        url: 'hobbies/',
        type: 'GET',
        success: function (data) {
            $.each(JSON.parse(data), function (i, item) {
                let html = "";
                html += "<tr id='" + item.pk + "'>";
                html += "<td id='" + item.pk + "-name'>"+item.fields.name+"</td>";
                html += "<td id='" + item.pk + "-icons'><i class='material-icons' title='delete' onclick='doDelete("+item.pk+")'>clear</i></td>";
                html += "</tr>";
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

var csrftoken = Cookies.get('csrftoken');

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

function showForm() {
        $('#addItemFormDiv').show();
        $('#addBtn').hide();
}

function hideForm() {
    $('#addItemFormDiv').hide();
    $('#addBtn').show();
}

function doAdd() {
        let name = $('#addFormNameField').val();
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
