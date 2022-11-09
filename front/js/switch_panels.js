$( document ).ready(function() {
    let panels = $('.main-panel');
    $('.panel-switcher').each(function() {
        let switcher = this;
        console.log(switcher.id);
        // console.log(this);
        // console.log(switcher);
        $(switcher).click(function() {
            console.log(switcher.id, " clicked");
            panels.each(function() {
                $(this).hide();
            })

            if (switcher.id === "panel_switch__connection") {
                $('#panel-home').show()
                $('#panel_heading').text('Соединение');
            } else if (switcher.id === "panel_switch__network") {
                $('#panel-network').show()
                $('#panel_heading').text('Сеть');
            } else if (switcher.id === "panel_switch__at_terminal") {
                $('#panel-at-terminal').show()
                $('#panel_heading').text('АТ терминал');
            } else if (switcher.id === "panel_switch__phone_book") {
                $('#panel-phonebook').show()
                $('#panel_heading').text('Телефонна книга');
            } else if (switcher.id === "panel_switch__sms") {
                $('#panel-sms').show()
                $('#panel_heading').text('СМС');
            } else if (switcher.id === "panel_switch__positioning") {
                $('#panel-positioning').show()
                $('#panel_heading').text('Позиционирование');
            } else if (switcher.id === "panel_switch__fota") {
                $('#panel-fota').show()
                $('#panel_heading').text('FOTA');
            }
        })
    });
});