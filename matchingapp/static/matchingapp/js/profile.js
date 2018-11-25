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