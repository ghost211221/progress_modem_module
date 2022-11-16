$(document).ready(function() {
    $('#send_cmd').click(function() {
        at_terminal_handler.send_cmd();
    })
})

let at_terminal_handler = {
    send_cmd: function() {
        let val = $('#input_cmd').val();
        if (val !== '') {
            eel.e_communicate(val)().then(response => {
                if (response.status === 'success') {
                    $('#at_log').append(`${val}\n`);
                    $('#at_log').append(`${response.ans}\n`);
                }
            })
        }
    }
}