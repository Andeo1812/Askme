$(".like-question").on('click', function (ev) {
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:8000/like_question/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'question_id=' + $this.data('id')
        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text(parsed.likes + ' Likes');
        });
    })
})

$(".dislike-question").on('click', function (ev) {
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:8000/dislike_question/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'question_id=' + $this.data('id')
        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text(parsed.dislikes + ' Disikes');
        });
    })
})
