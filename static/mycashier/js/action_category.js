jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
               
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        console.log(getCookie('csrftoken'));
        if(getCookie('csrftoken')){
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            xhr.setRequestHeader("adam", window.location.href);
        }else{
            xhr.setRequestHeader("X-CSRFToken", getCookie('_xsrf'));
        }
    }
});

$.ajaxSetup({
    headers : {
        'Csrf-Token': $('meta[name="csrf-token"]').attr('content')
    }
});

$(function() {
    $('#create_new').click(function() {
        uni_modal("Add New Category", "manage_category")
    })
    $('.edit-data').click(function() {
        uni_modal("Edit Category", "manage_category?id=" + $(this).attr('data-id'))
    })
    $('.delete-data').click(function() {
        _conf("Are you sure to delete this Category?", "delete_category", [$(this).attr('data-id')])
    })
})

function delete_category($id) {
    // start_loader();
    $.ajax({
        url: "delete_category",
        method: "GET",
        data: {
            id: $id
        },
        dataType: "json",
        error: err => {
            console.log(err)
            alert("An error occured.");
            // end_loader();
            $("#confirm_modal").modal("toggle");
        },
        success: function(resp) {
            if (typeof resp == 'object' && resp.status == 'success') {
                location.reload();
            } else {
                alert("An error occured.");
                // end_loader();
            }
            $("#confirm_modal").modal("toggle");
        }
    })
}

$(document).ready( function () {
    $('#tableCategory').DataTable();
} );