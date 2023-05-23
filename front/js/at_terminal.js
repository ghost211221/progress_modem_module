$(document).ready(async function() {
    at_terminal_handler.render_log();
    let res = await at_terminal_handler.get_cmds();
    if (res) {
        at_terminal_handler.render_groups();
        at_terminal_handler.render_cmds();
    }

    $('#cmd_type_select').change(function() {
        at_terminal_handler.render_cmds();
    })

    $('#send_cmd').click(function() {
        at_terminal_handler.send_manual_cmd();
    })

    $('#init_device').click(function() {
        eel.execute_operation('init')();
    })

    $('#network-get_operators_btn').click(function() {
        eel.execute_operation('get_operators_list')();
        $('#spinner_header').text('Поиск операторов')
        $('#spinner_modal').modal('show');
    })

    $('#network-refresh_info').click(function() {
        eel.execute_operation('refresh_network_info')();
    })

    $('#clear_log').click(function() {
        $('#at_log').empty();
    })

    $('.escape_seq_btn').click(function() {
        at_terminal_handler.handle_escape_seq(this);
    })


    $('#edit_cmds_modal').on('show.bs.modal', function (e) {
        at_terminal_handler.render_edit_cmds_modal_content();
    })

    $('#edit_cmds_groups_modal').on('show.bs.modal', function (e) {
        groups_edit_handler.render_groups_for_edit();
    })

    $('#edit_cmd-moveup').click(function() {
        let arr = get_cmd_list(at_terminal_handler.cmds, at_terminal_handler.selected_cmd_type)
        let current = $('.edit_cmds-cmd_li.selected');
        let prev = $(current).prev();
        let index_curr = arr.findIndex(x => x.name === $(current).find('a').text());
        let index_prev = arr.findIndex(x => x.name === $(prev).find('a').text());
        swapElements(arr, index_curr, index_prev);

        eel.save_cmds(at_terminal_handler.cmds)();
        at_terminal_handler.render_cmds();
        at_terminal_handler.render_edit_cmds_modal_content();
    })

    $('#edit_cmd-movedn').click(function() {
        let arr = get_cmd_list(at_terminal_handler.cmds, at_terminal_handler.selected_cmd_type);
        let current = $('.edit_cmds-cmd_li.selected');
        let next = $(current).next();
        let index_curr = arr.findIndex(x => x.name === $(current).find('a').text());
        let index_prev = arr.findIndex(x => x.name === $(next).find('a').text());
        swapElements(arr, index_curr, index_prev);

        eel.save_cmds(at_terminal_handler.cmds)();
        at_terminal_handler.render_cmds();
        at_terminal_handler.render_edit_cmds_modal_content();
    })

    $('#edit_cmd-edit').click(function() {
        let selected = $('.edit_cmds-cmd_li.selected');
        if (selected.length > 0) {
            $('#edit_cmd_modal').modal('show');
            $('#edit_cmd_cmd').val($(selected).find('a').text());
            $('#edit_cmd_text').val($(selected).find('a').attr('cmd_text'));
        }
    })

    $('#edit_cmd_ok').click(function() {
        let arr = get_cmd_list(at_terminal_handler.cmds, at_terminal_handler.selected_cmd_type);

        let name = $('#edit_cmd_cmd').val();
        let descr = $('#edit_cmd_text').val();

        let idx = arr.findIndex(x => x === at_terminal_handler.selected_cmd_for_edit);
        arr[idx].name = name;
        arr[idx].text = descr;

        eel.save_cmds(at_terminal_handler.cmds)();
        at_terminal_handler.render_cmds();
        at_terminal_handler.render_edit_cmds_modal_content();

        $('#edit_cmd_modal').modal('hide');
    })

    $('#add_cmd_ok').click(function() {
        let arr = get_cmd_list(at_terminal_handler.cmds, at_terminal_handler.selected_cmd_type);

        let name = $('#add_cmd_cmd').val();
        let descr = $('#add_cmd_text').val();

        arr.push({'name': name, 'text': descr});

        eel.save_cmds(at_terminal_handler.cmds)();
        at_terminal_handler.render_cmds();
        at_terminal_handler.render_edit_cmds_modal_content();

        $('#add_cmd_modal').modal('hide');
    })


    $('#edit_cmd-delete').click(function() {
        let arrIdx = at_terminal_handler.cmds.findIndex(x => x.name === at_terminal_handler.selected_cmd_type);

        at_terminal_handler.cmds[arrIdx].items = at_terminal_handler.cmds[arrIdx].items.filter(e => e !== at_terminal_handler.selected_cmd_for_edit)

        eel.save_cmds(at_terminal_handler.cmds)();
        at_terminal_handler.render_cmds();
        at_terminal_handler.render_edit_cmds_modal_content();

    })

    $('#copy_to_gorup_ok').click(function() {
        let selected = $('#copy_to_gorup_sel').val();

        if (selected !== '') {
            let arr = get_cmd_list(at_terminal_handler.cmds, selected);
            arr.push(at_terminal_handler.selected_cmd_for_edit);

            eel.save_cmds(at_terminal_handler.cmds)();
            at_terminal_handler.render_cmds();
            at_terminal_handler.render_edit_cmds_modal_content();
        }

        $('#copy_to_cmd_modal').modal('hide');
    })

    $('#move_to_gorup_ok').click(function() {
        let selected = $('#move_to_gorup_sel').val();

        if (selected !== '') {
            let arr = get_cmd_list(at_terminal_handler.cmds, selected);
            arr.push(at_terminal_handler.selected_cmd_for_edit);

            let arrIdx = at_terminal_handler.cmds.findIndex(x => x.name === at_terminal_handler.selected_cmd_type);
            at_terminal_handler.cmds[arrIdx].items = at_terminal_handler.cmds[arrIdx].items.filter(e => e !== at_terminal_handler.selected_cmd_for_edit);

            eel.save_cmds(at_terminal_handler.cmds)();
            at_terminal_handler.render_cmds();
            at_terminal_handler.render_edit_cmds_modal_content();
        }

        $('#move_to_cmd_modal').modal('hide');
    })


    $('#edit_cmds_groups-moveup').click(function() {
        let current = $('.edit_cmds_groups-group_li.selected');
        let prev = $(current).prev();
        let index_curr = at_terminal_handler.cmds.findIndex(x => x.name === $(current).find('a').text());
        let index_prev = at_terminal_handler.cmds.findIndex(x => x.name === $(prev).find('a').text());
        swapElements(at_terminal_handler.cmds, index_curr, index_prev);

        eel.save_cmds(at_terminal_handler.cmds)();
        at_terminal_handler.render_groups();
        at_terminal_handler.render_cmds();
        groups_edit_handler.render_groups_for_edit();
    })

    $('#edit_cmds_groups-movedn').click(function() {
        let current = $('.edit_cmds_groups-group_li.selected');
        let next = $(current).next();
        let index_curr = at_terminal_handler.cmds.findIndex(x => x.name === $(current).find('a').text());
        let index_prev = at_terminal_handler.cmds.findIndex(x => x.name === $(next).find('a').text());
        swapElements(at_terminal_handler.cmds, index_curr, index_prev);

        eel.save_cmds(at_terminal_handler.cmds)();
        at_terminal_handler.render_groups();
        at_terminal_handler.render_cmds();
        groups_edit_handler.render_groups_for_edit();
    })

    $('#rename_group_btn').click(function() {
        let selected = $('.edit_cmds_groups-group_li.selected');
        if (selected.length > 0) {
            $('#rename_group_modal').modal('show');
            $('#rename_group_input').val($(selected).find('a').text());
        }
    })

    $('#rename_group_ok').click(function() {
        for (let group of at_terminal_handler.cmds) {
            if (group.name === groups_edit_handler.selected_group_for_edit) {
                group.name = $('#rename_group_input').val();

                eel.save_cmds(at_terminal_handler.cmds)();
                at_terminal_handler.render_groups();
                at_terminal_handler.render_cmds();
                groups_edit_handler.render_groups_for_edit();
                $('#rename_group_modal').modal('hide');
            }
        }
    })

    $('#add_group_btn').click(function() {
        $('#add_group_modal').modal('show');
    })

    $('#add_group_ok').click(function() {
        let group_name = $('#add_group_input').val();
        if (group_name.length === 0) {
            return
        }

        at_terminal_handler.cmds.push({'name': group_name, 'items': []})
        eel.save_cmds(at_terminal_handler.cmds)();

        at_terminal_handler.render_groups();
        at_terminal_handler.render_cmds();
        groups_edit_handler.render_groups_for_edit();
    })

    $('#edit_cmds_groups-delete').click(function() {
        let selected = $('.edit_cmds_groups-group_li.selected').find('a').text();
        if (selected === undefined) {
            return
        }
        at_terminal_handler.cmds = at_terminal_handler.cmds.filter(e => e.name !== selected)

        eel.save_cmds(at_terminal_handler.cmds)();

        at_terminal_handler.render_groups();
        at_terminal_handler.render_cmds();
        groups_edit_handler.render_groups_for_edit();
    })

    $('#edit_cmds_groups-save').click(function() {
        if (groups_edit_handler.selected_cmd_for_edit !== '') {
            $('#save_group_modal').modal('show');
        }
    })

    $('#save_group_ok').click(function() {
        if ($('#save_group_input').val() === '' ) {
            $('#save_group_alert').show();
            return
        }

        eel.save_cmd_group(groups_edit_handler.selected_group_for_edit, $('#save_group_input').val())();
        $('#save_group_modal').modal('hide');
    })

    $('#add_group_input').change(function() {
        $('#save_group_alert').hide();
    })


    $('#network-operators_table').on('click', 'tbody tr', function(event) {
        $(this).addClass('selected').siblings().removeClass('selected');
    });

    $('#network-select_operator').click(function() {
        network_handler.select_operator()
    })

})

$(document).on('keypress',function(e) {
    if (e.which == 13 && $('#panel_heading').text() === 'Терминал ввода АТ-команд') {
        at_terminal_handler.send_manual_cmd();
    }
});

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
        if (field.hasOwnProperty('table_data')) {
            render_table(field.field, field.table_data);
        }

        if (field.hasOwnProperty('close_spinner')) {
            $('#spinner_modal').modal('hide');
        }
    }
}

function render_table(table_name, data_list) {
    let selector = `#${table_name} tbody`;
    $(selector).empty();
    for (let data of data_list) {
        let tr = $('<tr>');
        for (let key in data){
            let td = $('<td>');
            $(td).attr('key', key)
            $(td).attr('data', data[key])
            $(td).append(data[key]);
            $(tr).append(td);
        }
        $(selector).append(tr)
    }
}


const swapElements = (array, index1, index2) => {
    let temp = array[index1];
    array[index1] = array[index2];
    array[index2] = temp;
};

function get_cmd_list(cmds_dicts_list, group_name) {
    for (let group of cmds_dicts_list) {
        if (group.name === group_name) {
            return group.items
        }
    }
}


let at_terminal_handler = {
    cmds: [],
    selected_cmd_type: 'Generic',
    current_group: 'Generic',
    selected_cmd_for_edit: null,     // cmd selected for various edits

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
        html += '<br>'
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
        $('#cmd_type_select').empty();
        $('#copy_to_gorup_sel').empty();
        $('#move_to_gorup_sel').empty();
        for (let group of this.cmds) {
            let selected = this.selected_cmd_type !== null && group.name === this.selected_cmd_type ? 'selected' : '';
            $('#cmd_type_select').append(`<option id="cmd_group-${group.name}" ${selected}>${group.name}</option>`);
            $('#copy_to_gorup_sel').append(`<option id="copy_to_group-${group.name}">${group.name}</option>`);
            $('#move_to_gorup_sel').append(`<option id="move_to_group-${group.name}">${group.name}</option>`);
        }
    },

    render_cmds: function() {
        this.selected_cmd_type = $('#cmd_type_select').val();
        $('#at_cmd_list').empty();

        for (let group of this.cmds) {
            if (this.selected_cmd_type === group.name) {
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
    },

    render_edit_cmds_modal_content: function() {
        $('#edit_cmds-cmd_list').empty();
        let that = this;

        for (let group of this.cmds) {
            if (this.selected_cmd_type === group.name) {
                let i = 0;
                for (let item of group.items) {
                    let selector = `edit_cmd-${i}`;
                    $('#edit_cmds-cmd_list').append(`
                        <li class="list-group-item edit_cmds-cmd_li p-1">
                            <a class="nav-link icons-link p-0 edit_cmds-cmd_elem" href="#" def_text="${item.text}" def_name="${item.name}" cmd_text="${item.text}" id="${selector}">${item.name}</a>
                        </li>`)

                    $(`#${selector}`).click(function() {
                        $('#edit_cmd-cmd_description').empty();
                        $('#edit_cmd-cmd_description').append($(this).attr('cmd_text'));
                        $('.edit_cmds-cmd_elem').parent().removeClass('selected');
                        $(this).parent().addClass('selected');
                        that.selected_cmd_for_edit = item;

                    })

                    if (this.selected_cmd_for_edit !== null && this.selected_cmd_for_edit === item) {
                        let that_ = $(`#${selector}`)
                        $('#edit_cmd-cmd_description').empty();
                        $('#edit_cmd-cmd_description').append($(that_).attr('cmd_text'));
                        $('.edit_cmds-cmd_elem').parent().removeClass('selected');
                        $(that_).parent().addClass('selected');
                    }
                    i++;
                }
            }
        }
    }
}

let groups_edit_handler = {
    selected_group_for_edit: null,
    render_groups_for_edit: function() {
        $('#edit_cmds_groups-groups_list').empty();
        let that = this;

        for (let group of at_terminal_handler.cmds) {
            let selector = `edit_cmds_groups-${at_terminal_handler.cmds.indexOf(group)}`;
            $('#edit_cmds_groups-groups_list').append(`
                <li class="list-group-item edit_cmds_groups-group_li p-1">
                    <a class="nav-link icons-link p-0 edit_cmds_groups-group_elem" href="#" def_name="${group.name}" id="${selector}">${group.name}</a>
                </li>`)

            $(`#${selector}`).click(function() {
                $('.edit_cmds_groups-group_elem').parent().removeClass('selected');
                $(this).parent().addClass('selected');
                that.selected_group_for_edit = group.name;

            })

            if (this.selected_group_for_edit !== null && this.selected_group_for_edit === group.name) {
                let that_ = $(`#${selector}`)
                $('.edit_cmds-group_elem').parent().removeClass('selected');
                $(that_).parent().addClass('selected');
            }
        }
    }
}

let network_handler = {
    select_operator: function() {
        $('#network-operators_table .selected td').each(function() {
            if ($(this).attr('key') === 'operator_code') {
                eel.select_operator($(this).attr('data'))();
            }
        })
    }
}