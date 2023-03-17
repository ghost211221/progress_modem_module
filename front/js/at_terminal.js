$(document).ready(async function() {
    at_terminal_handler.render_log();
    let res = await at_terminal_handler.get_cmds();
    if (res) {
        at_terminal_handler.render_groups();
        at_terminal_handler.render_cmds();
    }

    $('#send_cmd').click(function() {
        at_terminal_handler.send_manual_cmd();
    })

    $('#init_device').click(function() {
        eel.execute_operation('init')();
    })

    $('#clear_log').click(function() {
        $('#at_log').empty();
    })

    $('.escape_seq_btn').click(function() {
        at_terminal_handler.handle_escape_seq(this);
    })

})

eel.expose(process_logs);
function process_logs(records) {
    if (records.length > 0) {
        for (let record of records) {
            at_terminal_handler .render_log_record(record.cmd, record.echo, record.ans, record.datetime, record.hex);
        }
    }
}

eel.expose(process_answers);
function process_answers(record) {
    if (record.hasOwnProperty('data')) {
        $(`#${record.field}`).text(record.data);
    }
    if (record.hasOwnProperty('img')) {
        $(`#${record.field}`).attr('src', `../img/${record.img}`);
    }
}

eel.expose(update_field);
function update_field(fields_objects) {
    console.log(fields_objects);
    for (let field of fields_objects) {
        if (field.hasOwnProperty('data')) {
            $(`#${field.field}`).text(field.data);
        }
        if (field.hasOwnProperty('img')) {
            $(`#${field.field}`).attr('src', `../img/${field.img}`);
        }
    }
}


let at_terminal_handler = {
    cmds: [],

    handle_escape_seq: function(button) {
        let text = $('#input_cmd').val();
        let mode = $(button).attr('mode');
        if (mode === 'escape') {
            text += '\x1B';
        } else if (mode === 'ctrl+z') {
            text += '\x1A';
        } else {
            blurt('Не верный аттрибут', `Mode имеет недопустимое значение - /${mode}/`, 'error');
            return
        }

        $('#input_cmd').val(text);
    },

    send_manual_cmd: function() {
        let val = $('#input_cmd').val();
        if (val !== '') {
            this.send_cmd(val);
        }
    },
    send_cmd: function(cmd) {
        eel.e_communicate(cmd)().then(response => {
            if (response.status === 'success') {
                // this.render_log_record(cmd, response.ans.echo, response.ans.ans)
            }
        })
    },

    render_log: function() {
        eel.e_get_log()().then(response => {
            if (response.status === 'fail') {
                alert(response.msg)
            }
        })
    },

    render_log_record: function(cmd, echo, ans, timestamp, hex) {
        let html = $('#at_log').html();
        html += `<span>${cmd}</span><br>`;
        html += `<span class="log-blue">${echo}</span><br>`;

        if ($('#print_timestamp').prop('checked')) {
            html += `<span class="log-green">[ ${timestamp} ]</span>`
        }

        if ($('#print_hex').prop('checked')) {
            html += `<span class="log-green"> ${hex} | </span>`
        }


        html += `<span class="log-green">${ans}</span><br>`;
        $('#at_log').html(html);
        $('#at_log').scrollTop($('#at_log')[0].scrollHeight);
    },

    render_log_records: function() {
        that = this;
        eel.get_log_msgs()().then(response => {
            if (response.length > 0) {
                for (let record of response) {
                    at_terminal_handler.render_log_record(record.cmd, record.echo, record.ans, record.datetime, record.hex);
                }
            }
        })
    },

    render_groups: function() {
        for (let group of this.cmds) {
            $('#cmd_type_select').append(`<option id="cmd_group-${group.name}">${group.name}</option>`);
        }
    },

    render_cmds: function() {
        let group_selected = $('#cmd_type_select').val();
        $('#at_cmd_list').empty();

        for (let group of this.cmds) {
            if (group_selected === group.name) {
                let i = 0;
                for (let item of group.items) {
                    $('#at_cmd_list').append(`<li class="at-cmd list-group-item p-1" data-bs-toggle="popover" title="${item.text}"><a class="nav-link icons-link p-0" href="#" data-toggle="popover" id="at_cmd-${i}">${item.name}</a></li>`)
                    let selector = `#at_cmd-${i}`;
                    $(selector).click(function() {
                        $('#input_cmd').val(`${item.name}`);
                    })
                    i++;
                }
            }
        }
    },

    get_cmds: async function() {
        const response = await eel.e_get_cmds()();
        this.cmds = response;

        return true
    }
}