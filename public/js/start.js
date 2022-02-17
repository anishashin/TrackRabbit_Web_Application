(function($) {
    $('#cancel').prop('disabled', true);

    $('#start').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/start',
            contentType: 'application/json',
            beforeSend: function() {
                $('#start').prop('disabled', true);
                $('#submit').prop('disabled', true);
                $('#cancel').prop('disabled', false);
                let timeout = $("#submittedSeconds").val();
                timeout = parseInt(timeout) * 1000;
                setTimeout(function() {
                    $('#start').prop('disabled', false);
                    $('#submit').prop('disabled', false);
                    $('#cancel').prop('disabled', true);
                }, timeout);
            }
        };
        $.ajax(requestConfig).then(function(response) {
        });
    });

    $('#cancel').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/cancel',
            contentType: 'application/json',
            beforeSend: function() {
                $('#start').prop('disabled', false);
                $('#submit').prop('disabled', false);
                $('#cancel').prop('disabled', true);
            }
        };
        $.ajax(requestConfig).then(function(response) {
        });
    });
})(window.jQuery);