(function($) {
    $('#start').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/start',
            contentType: 'application/json',
        };
        $.ajax(requestConfig).then(function(response) {
            $('#start').prop('disabled', true);
        });
    });
})(window.jQuery);