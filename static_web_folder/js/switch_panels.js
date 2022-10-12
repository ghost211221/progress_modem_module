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
            } else if (switcher.id === "panel_switch__network") {
                $('#panel-network').show()
            } else if (switcher.id === "panel_switch__at_terminal") {
                $('#panel-at-terminal').show()
            } else if (switcher.id === "panel_switch__phone_book") {
                $('#panel-phonebook').show()
            } else if (switcher.id === "panel_switch__sms") {
                $('#panel-sms').show()
            } else if (switcher.id === "panel_switch__positioning") {
                $('#panel-positioning').show()
            } else if (switcher.id === "panel_switch__fota") {
                $('#panel-fota').show()
            }
        })
    });
});