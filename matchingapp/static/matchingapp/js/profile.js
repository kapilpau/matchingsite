/*
    When the user requests to match with another user, through their profile, an AJAX request is sent to the server to
    add them to the requested user's requests. If that request is successful, the request match button is replaced with
    a cancel request button
*/
function requestMatch(id) {
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
        url: '/requestMatch/',
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: {
            id: id
        },
        success: function(data) {
            console.log("Success");
            console.log(data);
            document.getElementById('controlsDiv').innerHTML = '<button onclick="cancelRequest('+id+')">Cancel Request</button>';
        },
        failure: function(data) {
            console.log("Failure");
            console.log(data);
        },
        error: function(data) {
            console.log("Error");
            console.log(data);
        }
    });
}


/*
    If the user requests to cancel a match request, that is sent to the server through an AJAX requests. If the request
    is successful then user is removed from the requested user's list of requests, and the cancel request button
    is replaced with a request match button again
 */
function cancelRequest(id) {
    $.ajax({
        url: '/cancelRequest/',
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: {
            id: id
        },
        success: function(data) {
            console.log("Success");
            console.log(data);
            document.getElementById('controlsDiv').innerHTML = '<button onclick="requestMatch('+id+')">Request Match</button>';
        },
        failure: function(data) {
            console.log("Failure");
            console.log(data);
        },
        error: function(data) {
            console.log("Error");
            console.log(data);
        }
    });
}

// Once the document is ready, an onclick listener is added the admin toggle switch to allow admins to toggle admin
// status of other users
$(document).ready( function () {
        let id = window.location.pathname.split("/")[window.location.pathname.split("/").length -1];
        if (id === "") {
            id = window.location.pathname.split("/")[window.location.pathname.split("/").length -2];
        }
        $('#toggleAdmin').on('click', function () {
                console.log("Toggled");
                $.ajax({
                url: '/toggleAdmin/',
                type: 'POST',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                data: {
                    id: id
                },
                success: function(data) {
                    console.log("Success");
                    console.log(data);
                },
                failure: function(data) {
                    console.log("Failure");
                    console.log(data);
                },
                error: function(data) {
                    console.log("Error");
                    console.log(data);
                }
            });
        });

    }
);
