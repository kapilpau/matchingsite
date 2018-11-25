function manageRequest(id, action) {
    let csrftoken = Cookies.get('csrftoken');
    $.ajax({
       url: '/manageRequest/',
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: {
           id: id,
           action: action
        },
        success: function (data) {
           console.log("Success");
            console.log(data);
            if (action === 'accept') {
                document.getElementById('matchesTable').innerHTML += '<tr id="match'+data.id+'"><td>'+data.name+'</td><td><i href="/messages/'+data.id+'/" class="material-icons">mail</i><i onclick="deleteMatch('+data.id+')" class="material-icons">clear</i></td></tr>';
            }
            let element = document.getElementById('req'+id);
            element.parentNode.removeChild(element);
        },
        failure: function (data) {
           console.log("Failure");
            console.log(data);
        },
        error: function (data) {
           console.log("Error");
            console.log(data);
        }
    });
}

function deleteMatch(id) {
    let csrftoken = Cookies.get('csrftoken');
    $.ajax({
       url: '/deleteMatch/',
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: {
           id: id
        },
        success: function (data) {
           console.log("Success");
            console.log(data);
            let element = document.getElementById('match'+id);
            element.parentNode.removeChild(element);
        },
        failure: function (data) {
           console.log("Failure");
            console.log(data);
        },
        error: function (data) {
           console.log("Error");
            console.log(data);
        }
    });
}