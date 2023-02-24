$('document').ready(() => {
    author_filters = {};
    $('.authors .popover :checkbox').change(function () {
        author_id = this.getAttribute('data-id');
        author_name = this.getAttribute('data-name');
        if (this.checked) {
            author_filters[author_id] = author_name;
        } else {
            delete author_filters[author_id];
        }
        text = Object.values(author_filters).join(', ');
        $('.authors .filter-subtitle').text(text);
    });

    language_filters = {};
    $('.languages .popover :checkbox').change(function () {
        language_id = this.getAttribute('data-id');
        language_name = this.getAttribute('data-name');
        if (this.checked) {
            language_filters[language_id] = language_name;
        } else {
            delete language_filters[language_id];
        }
        text = Object.values(language_filters).join(', ');
        $('.languages .filter-subtitle').text(text);
    });


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