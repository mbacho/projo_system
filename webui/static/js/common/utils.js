function Alert() {
    this.msg = '';
    this.title = '';
    this.alertBox = $('#alertBox');
}
Alert.prototype.isVisible = function () {
    return this.alertBox.is(':visible');
};
Alert.prototype.clear = function () {
    $('#alert_msg').html('');
    $('#alert_title').html('');
    this.alertBox.attr('class', 'alert alert-info');
};
/**
 *
 * @param msg alert message
 * @param title alert title
 * @param type alert type [success,info,danger,warning,]
 */
Alert.prototype.showAlert = function (msg, title, type) {
    this.clear();
    $('#alert_msg').html(msg);
    $('#alert_title').html(title);
    this.alertBox.removeClass('alert-info').addClass('alert-' + type || 'info');
    if (!this.isVisible())this.alertBox.removeClass('hidden');
};
Alert.prototype.hideAlert = function () {
    if (this.isVisible())this.alertBox.addClass('hidden');
    this.clear();
};

/*helper function to load alert box*/
function loadAlertBox() {
    if (_.isUndefined(window.alert_box)) {
        window.alert_box = new Alert();
    }
    return window.alert_box;
}