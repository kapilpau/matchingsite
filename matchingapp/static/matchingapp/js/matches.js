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
                if (document.getElementById('matchesTable')) {
                    document.getElementById('matchesTable').innerHTML += '<tr id="match' + data.id + '"><td>' + data.name + '</td><td><i href="/messages/' + data.id + '/" class="material-icons">mail</i><i onclick="deleteMatch(' + data.id + ')" class="material-icons">clear</i></td></tr>';
                } else {
                    document.getElementById('controlsDiv').innerHTML = '<button href="/messages/'+data.id+'/">Send message</button><button onclick="deleteMatch('+data.id+')">Delete Match</button>'
                }
            } else {
                if (document.getElementById('controlsDiv')) {
                    document.getElementById('controlsDiv').innerHTML = '<button onclick="requestMatch('+id+')">Request Match</button>'
                }
            }
            let element = document.getElementById('req'+id);
            if (element) {
                element.parentNode.removeChild(element);
            }
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
            if (element)
            {
                element.parentNode.removeChild(element);
            } else {
                    document.getElementById('controlsDiv').innerHTML = '<button onclick="requestMatch('+id+')">Request Match</button>'
            }
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