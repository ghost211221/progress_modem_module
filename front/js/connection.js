$(document).ready(function() {
    connection_handler.nest_comport_pars();
    connection_handler.refresh_com_port_table();

    $('#connect_port').click(function() {
        connection_handler.connect();
    })

    $('#comport_ok').click(function() {
        connection_handler.previous_com = connection_handler.current_com;
        $('#connect_port').prop('disabled', false);

        connection_handler.render_status_string();
    })

    $('#comport_cancel').click(function() {
        $('#port_name').val(connection_handler.previous_com);
        if (connection_handler.previous_com === '') {
            $('#connect_port').prop('disabled', true);
            connection_handler.render_status_string();
        }
    })
})

let connection_handler = {
    previous_com: '',
    current_com: '',
    connected: false,
    refresh_com_port_table: function() {
        $("#com_ports_table_body tr").remove();
        let table = document.getElementById("com_ports_table_body");
        eel.e_get_comports_list()().then((response) => {
            for (let com of response) {
                var row = table.insertRow(0
                    );
                var cell1 = row.insertCell(0);

                var cell2 = row.insertCell(1);
                cell1.innerHTML = com.name;
                cell2.innerHTML = com.description;
            }

            this.handle_com_select();
        });
    },

    nest_comport_pars: function() {
        $('#baudrate').children().remove();
        $('#flow_control').children().remove();
        $('#data_bits').children().remove();
        $('#stop_bits').children().remove();
        $('#parity').children().remove();
        eel.e_get_comport_pars()().then((response) => {
            for (let item of response) {
                for (let [key, value] of Object.entries(item)) {
                    let selector = '#' + key;
                    for(let i of value) {
                        if (i.hasOwnProperty('selected')) {
                            $(selector).append(`<option id="${i.value}" selected>${i.value}</option>`);
                        } else {
                            $(selector).append(`<option id="${i.value}">${i.value}</option>`);
                        }
                    }
                }
            }
        });
    },

    handle_com_select: function() {
        let that = this;
        $('#com_ports_table_body tr').each(function(i) {
            $(this).click(function() {
                let firstCell = $(this).find('td').first();

                that.current_com = $(firstCell).text()
                $('#port_name').val(that.current_com);
                $('#connect_port').prop('disabled', false);
            });
        })
    },

    render_status_string: function() {
        let connection_status = 'подключено' ? this.connected : 'не подключено';
        let string = `AT: ${$('#port_name').val()} ${$('#baudrate').val()} ${$('#data_bits').val()} ${$('#parity').val()} Flow ctrl: ${$('#flow_control').val()} - ${connection_status}`;
        $('#status_string').text(string);
    },

    connect: function() {
        let port_name = $('#port_name').val();
        if ($('#connect_port').attr('mode') === 'connect') {
            if (port_name !== '') {
                eel.e_setup_device(
                    port_name,
                    $('#baudrate').val(),
                    $('#flow_control').val(),
                    $('#data_bits').val(),
                    $('#stop_bits').val(),
                    $('#parity').val()
                )().then(response => {
                    if (response.status === 'success') {
                        // enable lights and assemble parameters string
                        this.connected = true;
                        this.render_status_string();
                        $('#connect_port').attr('mode', 'disconnect')
                        $('#connect_port').html('Отключиться')
                    } else if (response.status === 'fail') {
                        alert(response.msg);
                    }
                })
            }
        } else if (($('#connect_port').attr('mode') === 'disconnect')) {
            eel.e_close_connection()().then(response => {
                if (response.status === 'success') {
                    // enable lights and assemble parameters string
                    this.connected = false;
                    this.render_status_string();
                    $('#connect_port').attr('mode', 'connect')
                    $('#connect_port').html('Подключитья')

                } else if (response.status === 'fail') {
                    alert(response.msg);
                }
            })
        }
    }
}