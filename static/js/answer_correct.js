$(".correct-answer").on('click', function (ev) {
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:8000/correct_answer/',
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
            $this.text(parsed.correct);
        });
    })
})

