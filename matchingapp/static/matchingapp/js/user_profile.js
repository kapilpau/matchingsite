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
        document.getElementById('dob').value = profile.dobdate;
        document.getElementById('email').value = profile.email;
        document.getElementById('gender').value = profile.gender;
    }
}

function save() {
    let submittable = true;
    document.getElementById('errorMsg').innerHTML = "";
    if (document.getElementById('name').value === "" || !/^[a-zA-Z ]+$/.test(document.getElementById('name').value))
    {
        document.getElementById('name').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Name cannot be empty or have non-alphabetic characters<br />";
        submittable = false;
    }

    if (document.getElementById('dob').value === "" ||  (new Date() - new Date(document.getElementById('dob').value))/(1000*60*60*24*365) < 18 || (new Date() - new Date(document.getElementById('dob').value))/(1000*60*60*24*365) > 99)
    {
        document.getElementById('dob').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Must be between 18 and 99<br />";
        submittable = false;
    }

    if (document.getElementById('gender').value === "")
    {
        document.getElementById('gender').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Must select a gender<br />";
        submittable = false;
    }

    if (document.getElementById('email').value === "" || !/^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-z]+$/.test(document.getElementById('email').value))
    {
        document.getElementById('email').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Invalid or blank email address<br />";
        submittable = false;
    }

    if (document.querySelectorAll('input[type="checkbox"]:checked').length === 0)
    {
        document.getElementById('hobbiesDiv').style.border = 'solid red';
        document.getElementById('errorMsg').innerHTML += "Must select at least one hobby<br />";
        submittable = false;
    }

    if (!submittable){
        return;
    }

    let csrftoken = Cookies.get('csrftoken');
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
    var selected = $('[name="hobby"]');
    for (var i = 0; i<selected.length; i++)
    {
        if (selected[i].checked)
        {
            checkedHobbies.push(selected[i].id);
            $('[id='+selected[i].id.replace(/\s/g, "")+'-label]').show();
            $('[id='+selected[i].id.replace(/\s/g, "")+'-br]').show();
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
