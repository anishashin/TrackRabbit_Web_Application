(function($) {
    $('#start').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/start',
            contentType: 'application/json',
            beforeSend: function() {
                $('#start').prop('disabled', true);
                let timeout = $("#submittedSeconds").val();
                timeout = parseInt(timeout) * 1000;
                setTimeout(function() {
                    $('#start').prop('disabled', false);
                }, timeout);
            }
        };
        $.ajax(requestConfig).then(function(response) {
        });
    });
})(window.jQuery);