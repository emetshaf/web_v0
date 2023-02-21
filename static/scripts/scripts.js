$('document').ready(() => {
    $.get('http://0.0.0.0/api/v1/status/', (data, status) => {
        if (data['status'] === 'OK') $('#api_status').addClass('available');
        else $('#api_status').removeClass('available');
        });

    $('.signinButton').click(() => {
        signin($('#username').val(), $('#password').val());
    });
    $('.signupButton').click(() => {
        signup($('#username').val(), $('#password').val());
    });
});


function signin(username, password) {
    $.ajax({
        url: 'http:///localhost/auth/signin',
        type: 'POST',
        data: JSON.stringify({
            username: username,
            password: password,
        }),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    });
}

function signup(username, password) {
    $.ajax({
        url: 'http:///localhost/auth/signup',
        type: 'POST',
        data: JSON.stringify({
            username: username,
            password: password,
        }),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    });
}

// function fetchBooks() {
//     $.ajax({
//         url: 'http://0.0.0.0/api/v1/books/',
//         type: 'GET',
//         data: JSON.stringify({
//             username: username,
//             password: password,
//         }),
//     });
// }