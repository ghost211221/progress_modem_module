$(document).ready(async function() {
    await connection_handler.init();

    $('#connect_port').click(function() {
        connection_handler.connect();
    })

    $('#comport_ok').click(function() {
        connection_handler.setup_port();
        if (connection_handler.previous_com !== '') {
            $('#connect_port').prop('disabled', false);
        }
        connection_handler.render_com_data();
    })

    $('#comport_cancel').click(function() {
        connection_handler.select_values_from_comport();
        if (connection_handler.previous_com === '') {
            $('#connect_port').prop('disabled', true);
        }
        connection_handler.render_com_data();
    })

    $('#com_ports_table').on('click', 'tbody tr', function(event) {
        $(this).addClass('selected').siblings().removeClass('selected');
    });

})

let com_port = {
    port: '',
    baudrate: '',
    flow_control: '',
    data_bits: '',
    stop_bits: '',
    parity: '',
    DCD: false,
    RI: false,
    DSR: false,
    CTS: false,
    DTR: false,
    RTS: false,
    connected: false,
    description: ''
}

let connection_handler = {
    com_ports: [],
    init: async function() {
        this.nest_comport_pars();
        setInterval(this.fill_com_port_table, 2000);
        let res = await this.get_port_data();
        this.select_values_from_comport();
        if (res) {
            this.render_com_data();
        }
        this.setup_connect_btn();
    },

    render_com_data: function() {
        this.render_status_string();
        this.render_status_lights();
        this.render_comdata_on_panel();
    },

    get_port_data: async function() {
        const response = await eel.e_get_comport_data()();
        com_port.port = response.comport;
        com_port.baudrate = response.baudrate;
        com_port.flow_control = response.flow_control;
        com_port.data_bits = response.data_bits;
        com_port.stop_bits = response.stop_bits;
        com_port.parity = response.parity;
        com_port.DCD = response.cd;
        com_port.RI = response.ri;
        com_port.DSR = response.dsr;
        com_port.CTS = response.cts;
        com_port.DTR = response.dtr;
        com_port.RTS = response.rts;
        com_port.connected = response.connected;
        com_port.description = response.description;
        return true
    },

    select_values_from_comport: function() {
        $('#port_name').val(com_port.port);
        $('#baudrate').val(com_port.baudrate);
        $('#flow_control').val(com_port.flow_control);
        $('#data_bits').val(com_port.data_bits);
        $('#stop_bits').val(com_port.stop_bits);
        $('#parity').val(com_port.parity);
        $('#description').val(com_port.description);
    },

    setup_connect_btn: function() {
        if (com_port.connected) {
            this.render_com_data();
            $('#connect_port').attr('mode', 'disconnect')
            $('#connect_port').html('Отключиться')
        } else {
            $('#connect_port').attr('mode', 'connect')
            $('#connect_port').html('Подключиться')
            if (com_port.port === '') {
                $('#connect_port').prop('disabled', true);
            }
        }
    },

    fill_com_port_table: function() {
        let that = this;
        let table = document.getElementById("com_ports_table_body");
        eel.e_get_comports_list()().then((response) => {
            if (that.com_ports !== response) {
                $("#com_ports_table_body tr").remove();
                for (let com of response) {
                    var row = table.insertRow(0
                        );
                    var cell1 = row.insertCell(0);

                    var cell2 = row.insertCell(1);
                    cell1.innerHTML = com.name;
                    cell2.innerHTML = com.description;
                }

                // that.handle_com_select();
                that.com_ports = response;
                $('#com_ports_table_body tr').each(function(i) {
                    $(this).click(function() {
                        let firstCell = $(this).find('td').first();
                        let lastCell = $(this).find('td').last();

                        com_port.description = $(lastCell).text()
                        com_port.port = $(firstCell).text()
                        $('#port_name').val(com_port.port);
                        $('#description').val(com_port.description);
                        $('#connect_port').prop('disabled', false);
                    });
                })
            }
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
                            $(selector).append(`<option id="${i.value}">${i.value}</option>`);
                        } else {
                            $(selector).append(`<option id="${i.value}">${i.value}</option>`);
                        }
                    }
                }
            }
        });
    },

    handle_com_select: function() {
        $('#com_ports_table_body tr').each(function(i) {
            $(this).click(function() {
                let firstCell = $(this).find('td').first();
                let lastCell = $(this).find('td').last();

                com_port.description = $(lastCell).text()
                com_port.port = $(firstCell).text()
                $('#port_name').val(com_port.port);
                $('#description').val(com_port.description);
                $('#connect_port').prop('disabled', false);
            });
        })
    },

    render_status_string: function() {
        let connection_status = com_port.connected ? 'подключено' : 'не подключено';
        let string = `AT: ${$('#port_name').val()} ${$('#baudrate').val()} ${$('#data_bits').val()} ${$('#parity').val()} Flow ctrl: ${$('#flow_control').val()} - ${connection_status}`;
        $('#status_string').text(string);
    },

    render_status_lights: function() {
        if (com_port.connected) {
            $( "#dtr" ).prop( "checked", com_port.DTR );
            $( "#rts" ).prop( "checked", com_port.RTS );
            $('#dcd').removeClass('indicator-init');
            $('#dcd').addClass(com_port.DCD ? 'indicator-enabled' : 'indicator-disabled');
            $('#ri').removeClass('indicator-init');
            $('#ri').addClass(com_port.RI ? 'indicator-enabled' : 'indicator-disabled');
            $('#dsr').removeClass('indicatorinit');
            $('#dsr').addClass(com_port.DSR ? 'indicator-enabled' : 'indicator-disabled');
            $('#cts').removeClass('indicator-init');
            $('#cts').addClass(com_port.CTS ? 'indicator-enabled' : 'indicator-disabled');
        } else {
            $( "#dtr" ).prop( "checked", false );
            $( "#rts" ).prop( "checked", false );
            $('#dcd').removeClass('indicator-enabled indicator-disabled');
            $('#dcd').addClass('indicator-init');
            $('#ri').removeClass('indicator-enabled indicator-disabled');
            $('#ri').addClass('indicator-init');
            $('#dsr').removeClass('indicator-enabled indicator-disabled');
            $('#dsr').addClass('indicator-init');
            $('#cts').removeClass('indicator-enabled indicator-disabled');
            $('#cts').addClass('indicator-init');
        }
    },

    render_comdata_on_panel: function() {
        $('#home_panel-port').text(com_port.port)
        $('#home_panel-baudrate').text(com_port.baudrate)
        $('#home_panel-flow_control').text(com_port.flow_control)
        $('#home_panel-data_bits').text(com_port.data_bits)
        $('#home_panel-stop_bits').text(com_port.stop_bits)
        $('#home_panel-parity').text(com_port.parity)
        $('#home_panel-status').text(com_port.connected ? 'Подключено' : 'Не подключено')
    },

    setup_port: function() {
        com_port.port = $('#port_name').val();
        com_port.description = $('#description').val();
        com_port.baudrate = $('#baudrate').val();
        com_port.flow_control = $('#flow_control').val();
        com_port.data_bits = $('#data_bits').val();
        com_port.stop_bits = $('#stop_bits').val();
        com_port.parity = $('#parity').val();

        eel.e_setup_device(
            com_port.port,
            com_port.description,
            com_port.baudrate,
            com_port.flow_control,
            com_port.data_bits,
            com_port.stop_bits,
            com_port.parity
        )().then(response => {
            if (response.status === 'success') {
                // setup successfull
            } else if (response.status === 'fail') {
                alert(response.msg);
            }
        })
    },

    connect: async function() {
        if ($('#connect_port').attr('mode') === 'connect') {
            eel.e_connect_device()().then(response => {
                if (response.status === 'success') {
                    // enable lights and assemble parameters string
                    com_port.connected = true;
                    com_port.DCD = response.cd;
                    com_port.RI = response.ri;
                    com_port.DSR = response.dsr;
                    com_port.CTS = response.cts;
                    com_port.DTR = response.dtr;
                    com_port.RTS = response.rts;
                    this.render_com_data();
                    $('#connect_port').attr('mode', 'disconnect');
                    $('#connect_port').html('Отключиться');
                    $('#init_device').prop('disabled', false);
                    $('#set_port_btn').prop('disabled', true);

                    $('.modem-info').removeClass('disabled');
                    $('.modem-info').addClass('enabled');

                } else if (response.status === 'fail') {
                    alert(response.msg);
                }
            })
        } else if (($('#connect_port').attr('mode') === 'disconnect')) {
            eel.e_close_connection()().then(response => {
                if (response.status === 'success') {
                    // enable lights and assemble parameters string
                    com_port.connected = false;
                    this.render_com_data();
                    $('#connect_port').attr('mode', 'connect')
                    $('#connect_port').html('Подключиться')
                    $('#init_device').prop('disabled', true);
                    $('#set_port_btn').prop('disabled', false);

                    $('.modem-info').removeClass('enabled');
                    $('.modem-info').addClass('disabled');
                } else if (response.status === 'fail') {
                    alert(response.msg);
                }
            })
        }
    }
}