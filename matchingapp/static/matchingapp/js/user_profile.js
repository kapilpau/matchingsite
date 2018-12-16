// When the user presses the edit button, the spans have to be converted to inputs to allow the user to be able to edit
// their profile. It also displays all of the possible hobbies that the user can select
function switchToEdit() {
    $('[name="hobby"]').show();
    document.getElementById('editBtn').hidden = true;
    document.getElementById('saveBtn').hidden = false;
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


// When the user saves their profile, it runs a number of checks on the data provided is acceptable
// If it is, then the data is sent to the server through an AJAX query. If the update succeeds, it
// updates the inputs to be spans with the new values
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
    document.getElementById('editBtn').hidden = false;
    document.getElementById('saveBtn').hidden = true;
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
    $.ajax({
        url: 'updateProfile/',
        type: 'PUT',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        data: profile,
        success: function (data) {
            dob = new Date(profile.dob);
            const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            document.getElementById('name').outerHTML = "<span id='name'>"+profile.name+"</span>";
            document.getElementById('dob').outerHTML = "<span id='dob'>"+ dob.getDate() + " " + monthNames[dob.getMonth()] + " " + dob.getFullYear() +"</span>";
            document.getElementById('email').outerHTML = "<span id='email'>"+ profile.email +"</span>";
            document.getElementById('gender').outerHTML = "<span id='gender'>"+ profile.gender +"</span>";
        },
        failure: function (data) {
        },
        error: function (data) {
        }
    });
}


// Users can update their profile picture. The update happens through an AJAX query and updates the image shown
// with JQuery, without the user having to refresh the page
function uploadNewProfileImage() {
    var csrftoken = Cookies.get('csrftoken');
    var formData = new FormData();
    var new_img = document.getElementById('newProfileImg').files[0];
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
        },
        failure: function (data) {
        },
        error: function (data) {
        },
        processData: false
    });
}


$(function(){
    document.getElementById('resetPassword').onclick = function() {
      document.getElementById('myModal').style.display = "block";
      document.getElementById('existingPassword-label').style.display = "block";
      document.getElementById('newPassword-label').style.display = "block";
      document.getElementById('confirmPassword-label').style.display = "block";

    };

    document.getElementsByClassName("close")[0].onclick = function() {
      document.getElementById('myModal').style.display = "none";
    };

    window.onclick = function(event) {
      if (event.target === document.getElementById('myModal')) {
        document.getElementById('myModal').style.display = "none";
      }
    };
    $(document).on('keyup', function (e) {
        if (e.keyCode === 27)
        {
            document.getElementById('myModal').style.display = "none";
        }
    })
});

function updatePassword() {
    let submittable = true;
    if (document.getElementById('newPassword').value === "" && !(/[a-z]+/.test(document.getElementById('newPassword').value) && /[A-Z]+/.test(document.getElementById('newPassword').value) && /[0-9]+/.test(document.getElementById('newPassword').value) && /[!@_]+/.test(document.getElementById('newPassword').value))){
        document.getElementById('newPassword').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Password must be at least 8 characters long and contain a combination of lower-case letters, upper-case letters, digits and special characters (!@_)<br />";
        submittable = false;
    }

    if (document.getElementById('confirmPassword').value !== document.getElementById('newPassword').value){
        document.getElementById('errorMsg').innerHTML += "<br />";
        submittable = false;
    }
    let csrftoken = Cookies.get('csrftoken');

    if (submittable)
    {
        $.ajax({
            url: '/saveNewPassword/',
            type: 'POST',
            data: {
                oldPassword: document.getElementById('existingPassword').value,
                newPassword: document.getElementById('newPassword').value,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (data) {
                document.getElementById('myModal').style.display = "none";
            },
            error: function (data) {
                if (data.responseText === 'Incorrect existing password')
                {
                    document.getElementById('existingPassword').style.borderColor = 'red';
                }
            },
            failure: function (data) {
                alert('Something went wrong');
            }

        });
    }
}