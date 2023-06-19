$(document).ready(async function() {
    $('#clear_sms_text').click(function() {
        $('#sms_text').val('');
    })

    $('#send_sms').click(function() {
        let passed = sms_controller.validate_send();
        if (passed) {
            sms_controller.send_sms();
        }
    })

    $('#sms-set_sms_number').click(async function() {
        let tel_num = $('#sms-sms_number').val();
        if (tel_num === '') {
            return
        }
        await eel.set_sms_number(tel_num)();
    })

    $('#sms-get_sms_list').click(function() {
        eel.get_sms_list()();
    })

    $('#sms-sms_table').on('click', 'tbody tr', function(event) {
        $(this).addClass('selected').siblings().removeClass('selected');
        $(this).find('td').each(function() {
            if ($(this).attr('key') === 'i') {
                eel.get_sms_text($(this).attr('data'))();
            }
        })
    });

    $('#sms-answer_sms').click(function() {
        $('#sms-sms_table .selected td').each(function() {
            if ($(this).attr('key') === 'i') {
                $('#sms_phone_number').val($(this).attr('data'));
            }
        })
    })

    $('#sms-delete_selected_sms').click(function() {
        $('#sms-sms_table .selected td').each(function() {
            if ($(this).attr('key') === 'i') {
                eel.delete_sms($(this).attr('data'))();
            }
        })
    })

    $('#sms-delete_all_sms').click(function() {
        eel.delete_all_sms()();
    })


    $('#sms-disable_sms_alert').click(function() {
        eel.disable_sms_alert()();
    })

})

let sms_controller = {
    phone_regex: /^\+?\d?\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/,
    validate_send: function() {
        let phone_number = $('#sms_phone_number').val();
        if (!this.phone_regex.test(phone_number)) {
            blurt('Не правильный номер телефона','Введите правильный номер телефона в формате +79ххххххххх')

            return false
        }

        let text = $('#sms_text').val();
        if (text === '') {
            blurt('Введите текст сообщения')

            return false
        }

        return true
    },

    send_sms: function() {
        let phone_number = $('#sms_phone_number').val();
        let text = $('#sms_text').val();
        eel.send_sms(phone_number, text)();
        // blurt('СМС отправлено')
    }
}