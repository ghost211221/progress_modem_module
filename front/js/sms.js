$(document).ready(async function() {
    $('#send_sms').click(function() {
        $('#clear_sms_text').val('');
    })

    $('#send_sms').click(function() {
        let passed = sms_controller.validate_send();
        if (passed) {
            sms_controller.send_sms();
        }
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