function switchToEdit() {
    $('[name="hobby"]').show();
    $('#editBtn').hide();
    $('#saveBtn').show();
    $("[id*='label']").show();
    $("[id*='br']").show();
    document.getElementById('name').outerHTML = "<input type='text' placeholder='Name' id='name' />";
    document.getElementById('dob').outerHTML = "<input type='date' placeholder='Date of Birth' id='dob' />";
    document.getElementById('email').outerHTML = "<input type='email' placeholder='Email' id='email' />";
    document.getElementById('gender').outerHTML = "<select id='gender'><option disabled selected value>Gender</option><option id='Male'>Male</option><option id='Female'>Female</option><option id='Other'>Other</option></select>";
    if (JSON.stringify(profile) !== "{}")
    {
        document.getElementById('name').value = profile.name;
        document.getElementById('dob').value = profile.dob;
        document.getElementById('email').value = profile.email;
        document.getElementById('gender').value = profile.gender;
    }
}

function save() {
    var csrftoken = Cookies.get('csrftoken');
    $('[name="hobby"]').hide();
    $("[id*='label']").hide();
    $("[id*='br']").hide();
    $('#editBtn').show();
    $('#saveBtn').hide();
    profile.name = document.getElementById('name').value;
    profile.dob = document.getElementById('dob').value;
    profile.email = document.getElementById('email').value;
    profile.gender = document.getElementById('gender').value;
    var checkedHobbies = [];
    var selected = $('[name="hobby"]')
    for (var i = 0; i<selected.length; i++)
    {
        if (selected[i].checked)
        {
            checkedHobbies.push(selected[i].id);
            // $('[id='+selected[i].id+']').show();
            $('[id='+selected[i].id+'-label]').show();
            $('[id='+selected[i].id+'-br]').show();
        }
    }
    profile.checkedHobbies = checkedHobbies;

    document.getElementById('name').outerHTML = "<span id='name'>"+profile.name+"</span>";
    document.getElementById('dob').outerHTML = "<span id='dob'>"+ profile.dob +"</span>";
    document.getElementById('email').outerHTML = "<span id='email'>"+ profile.email +"</span>";
    document.getElementById('gender').outerHTML = "<span id='gender'>"+ profile.gender +"</span>";
    $.ajax({
        url: 'updateProfile/',
        type: 'PUT',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        data: profile,
        success: function (data) {
            console.log(data);
        },
        failure: function (data) {
            console.log(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function uploadNewProfileImage() {
    var csrftoken = Cookies.get('csrftoken');
    var formData = new FormData();
    var new_img = document.getElementById('newProfileImg').files[0];
    console.log(new_img);
    formData.append('new_img', new_img, 'new_img.png');
    $.ajax({
        url: 'uploadNewProfileImage/',
        type: 'POST',
        data: formData,
        contentType: false,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            $('#profileImg').attr('src', data.url);
            console.log(data);
        },
        failure: function (data) {
            console.log(data);
        },
        error: function (data) {
            console.log(data);
        },
        processData: false
    });
}
