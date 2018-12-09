/*
    When the user accepts or rejects a request, an AJAX request is sent to the server to accept or reject the request.
    If they accept the request, the accept and reject buttons are replaced with a Send Message button and a Delete Match
    button. If they reject the request, then the buttons are replaced with a Request Match button
 */
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
                    document.getElementById('matchesTable').innerHTML += '<tr id="match' + data.id + '"><td><a href="/profile/"' + data.id + '>' + data.name + '</td><td><a href="/findConvo/' + data.id + '/"><i class="material-icons">mail</i></a><i onclick="deleteMatch(' + data.id + ')" class="material-icons">clear</i></td></tr>';
                } else {
                    document.getElementById('controlsDiv').innerHTML = '<button href="/findConvo/'+data.id+'/">Send message</button><button onclick="deleteMatch('+data.id+')">Delete Match</button>'
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


/*
    When the user presses the delete match button, an AJAX request is sent to the server to delete the users from each
    other's matches, and the Send Message and Delete Match buttons are replaced with a Request Match button
 */
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