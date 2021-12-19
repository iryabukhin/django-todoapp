function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    headers: {'X-CSRFToken': getCookie('csrftoken')}
});

$(document).ready(function () {
    'use strict';

    $('#todo_list tr.todo-item td').css('cursor', 'pointer');
    $('#todo_list tr').click(function (event) {
        event.preventDefault();
        if (event.target.tagName === 'TD') {
            var taskId = $(this).data('id');
            window.location = '/todo/' + taskId + '/update';
        }
    });

    $('#todo_list').click(function (event) {

        if (event.target.tagName != 'BUTTON') {
            return;
        }

        var tr = $(event.target).closest('tr');
        var id = tr.data('id');

        var action = $(event.target).data('action');
        if (action) {
            handleAction(action, id, event.target);
        }
    });

    function handleAction(action, taskId, element) {
        var tr = $(element).closest('tr');

        if (action === 'complete') {
            $.ajax('/todo/' + taskId + '/complete', {method: 'PUT'})
                .done(function (response) {
                    console.log(response);

                    tr.removeClass('alert-danger').addClass('alert-success');
                    tr.find('.todo-item__status').text('Completed');
                    tr.find('i.fa').removeClass('fa-check').addClass('fa-repeat');
                }).fail(function (response) {
                alert('Failed updating task!');
            });
        } else if (action === 'delete') {
            $.ajax('/todo/' + taskId + '/delete', {
                method: 'DELETE'
            }).done(function (response) {
                console.log(response);
                tr.removeClass('alert-success').addClass('alert-danger');
                tr.fadeOut(1000);
            }).fail(function (response) {
                alert('Could not delete task!');
            });
        }
    }

    function refreshElement(elem) {
        $(elem).hide().show(0);
    }

    var doComplete = function (id, status) {
        $.ajax({
            url: '/api/todos/' + id,
            data: JSON.stringify({'completed': status}),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            type: 'PATCH',
            contentType: 'application/json',
            success: function (data, status, request) {
                console.log('Response received', data);
                var li = checkbox.closes('li.list-group-item');
                if (listItem && checked) {
                    listItem.classList.add('completed')
                } else if (listItem) {
                    listItem.classList.remove('completed')
                }
            },
            error: function (request, status, err) {
                checkbox.disabled = false;
            }
        });
    };

});