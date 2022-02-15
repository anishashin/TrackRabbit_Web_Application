(function($) {
    $('#start').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/start',
            contentType: 'application/json',
            beforeSend: function() {
                $('#start').prop('disabled', true);
            }
        };
        $.ajax(requestConfig).then(function(response) {
        });
    });
})(window.jQuery);