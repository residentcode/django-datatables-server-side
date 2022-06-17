$(document).ready(function () {
    let path_url = window.location.pathname
    let table = $('#table-orders').DataTable({
        pagingType: 'full_numbers',
        responsive: true,
        processing: true,
        serverSide: true,
        ajax: {
            url: path_url,
            type: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        },
        columnDefs: {},
        searchDelay: 500,
        lengthMenu: [10, 20, 25, 30, 50, 100],
        columns: [
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            { data: 'gender' },
            { data: 'city' },
        ],

    });

});