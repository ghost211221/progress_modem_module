$(document).ready(function() {
    at_terminal_handler.render_log();

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
                    this.render_log_record(val, response.ans.echo, response.ans.ans)
                }
            })
        }
    },

    render_log: function() {
        eel.e_get_log()().then(response => {
            for (let record of response) {
                this.render_log_record(record[0], record[1], record[2]);
            }
        })
    },

    render_log_record: function(cmd, echo, ans) {
        let html = $('#at_log').html();
        html += `<span>${cmd}</span><br>`;
        html += `<span class="log-blue">${echo}</span><br>`;
        html += `<span class="log-green">${ans}</span><br>`;
        $('#at_log').html(html);
    }
}