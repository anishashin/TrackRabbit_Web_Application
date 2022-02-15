(function($) {
    $('#start').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/start',
            contentType: 'application/json',
            beforeSend: function() {
                $('#start').prop('disabled', true);
                setTimeout(function() {
                    $('#start').prop('disabled', false);
                }, 5000);
            }
        };
        $.ajax(requestConfig).then(function(response) {
        });
    });
})(window.jQuery);