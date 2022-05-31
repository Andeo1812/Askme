$(".like-answer").on('click', function (ev) {
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:80/like_answer/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'answer_id=' + $this.data('id')
        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text(parsed.likes + ' Likes');
        });
    })
})

$(".dislike-answer").on('click', function (ev) {
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:80/dislike_answer/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'answer_id=' + $this.data('id')
        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text(parsed.dislikes + ' Disikes');
        });
    })
})
