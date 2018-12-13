$(function(){
    document.getElementById('addBtn').onclick = function() {
      document.getElementById('myModal').style.display = "block";
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


function createChat() {
    if (document.querySelectorAll('input[type="checkbox"]:checked').length === 0){
        document.getElementById('checkBoxLabel').style.borderColor = 'red';
    } else {
        let others = [];
        let selected = $('[name="people"]');
        for (var i = 0; i<selected.length; i++)
        {
            if (selected[i].checked)
            {
                others.push(selected[i].id);
            }
        }
        $.ajax({
            url: '/findGroupChat/',
            type: 'POST',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                console.log(data);
                window.location.pathname ='/messages/' + data.id;
            },
            data: {
                'name': document.getElementById('chatName').val(),
                'others': others.join(',')
            }
        });
    }

}