$(function ($) {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('#form_mailer').submit(function (e){
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            // headers: {'X-CSRFToken': getCookie( name: 'csrftoken')},
            dataType: 'json',
            success: function (response) {
                console.log('ok - ', response)
                if (response.status === 201){
                    window.location.reload()
                }
            },
            error: function (response) {
                console.log('err - ', response)
                if (response.status === 400){
                  $('.alert-danger').removeClass('d-none')
                }
            }
        })
    })
})