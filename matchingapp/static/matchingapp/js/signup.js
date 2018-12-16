// Whenever the user presses the Enter key while in an input, the sign up function is called
// This is to make the form more user friendly, so they don't have use their mouse while filling it out
$(function(){
    $("input").keyup(function(e){
        if (e.keyCode === 13)
        {
            signUp();
        }
    });
});


/*
    When the user presses Enter or the Sign Up button, the signUp() method is called. The method initially checks
    the values of all of the form to ensure that they're all acceptable. If they're not, then the appropriate fields'
    borders are set to red and the error message is updated to inform the user of why it was unacceptable. If it is
    acceptable then the details are sent to the server. If the sign up is successful, the user is redirected to their
    profile page.
*/
function signUp() {
    let submittable = true;
    document.getElementById('errorMsg').innerHTML = "";
    if (document.getElementById('username').value === "" || !/^[a-zA-Z0-9_\-]+$/.test(document.getElementById('username').value))
    {
        document.getElementById('username').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Name cannot be empty and can only contain alphanumeric characters and _ or -<br />";
        submittable = false;
    }
    if (document.getElementById('password').value === document.getElementById('username').value)
    {
        document.getElementById('password').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Password cannot be the same as username<br />";
        submittable = false;
    }
    if (document.getElementById('password').value === "")
    {
        document.getElementById('password').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Password cannot be empty<br />";
        submittable = false;
    }
    if (document.getElementById('confirmPassword').value === "")
    {
        document.getElementById('confirmPassword').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Confirm Password cannot be empty<br />";
        submittable = false;
    }
    if (document.getElementById('confirmPassword').value !== document.getElementById('password').value)
    {
        document.getElementById('confirmPassword').style.borderColor = 'red';
        document.getElementById('password').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Passwords do not match<br />";
        submittable = false;
    }
    if (!(/[a-z]+/.test(document.getElementById('password').value) && /[A-Z]+/.test(document.getElementById('password').value) && /[0-9]+/.test(document.getElementById('password').value) && /[!@_]+/.test(document.getElementById('password').value) && document.getElementById('password').value.length >= 8))
    {
        document.getElementById('password').style.borderColor = 'red';
        document.getElementById('errorMsg').innerHTML += "Password must be at least 8 characters long and contain a combination of lower-case letters, upper-case letters, digits and special characters (!@_)<br />";
        submittable = false;
    }
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
    } else {
        let usrProf = {};
        usrProf.name = document.getElementById('name').value;
        usrProf.dob = document.getElementById('dob').value;
        usrProf.email = document.getElementById('email').value;
        usrProf.gender = document.getElementById('gender').value;
        let checkedHobbies = [];
        let selected = $('[name="hobby"]');
        for (var i = 0; i<selected.length; i++)
        {
            if (selected[i].checked)
            {
                checkedHobbies.push(selected[i].id);
                $('[id='+selected[i].id.replace(/\s/g, "")+'-label]').show();
                $('[id='+selected[i].id.replace(/\s/g, "")+'-br]').show();
            }
        }
        var csrftoken = Cookies.get('csrftoken');
        usrProf.checkedHobbies = checkedHobbies;
        $.ajax({
                url: '../signup/',
                type: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                data: {
                    username: $('#username').val(),
                    password: $('#password').val(),
                    profile: usrProf,
                    csrfmiddlewaretoken: csrftoken
                },
                success: function (data) {
                    profile = usrProf;
                    window.location.replace('../profile')
                },
                failure: function (data) {
                    document.getElementById('username').style.borderColor = 'red';
                    document.getElementById('password').style.borderColor = 'red';
                },
                error: function (jqXHR, textStatus, error) {
                    if (jqXHR.responseText === "Username already taken") {
                        document.getElementById('username').style.borderColor = 'red';
                        alert("Username already taken");
                    }
                }
            });
    }
}