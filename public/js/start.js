(function($) {
    $('#start').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/start',
            contentType: 'application/json',
            beforeSend: function() {
                $('#start').prop('disabled', true);
                console.log(typeof $("#submittedSeconds").val());
                // setTimeout(function() {
                //     $('#start').prop('disabled', false);
                // }, $("#submittedSeconds").val());
            }
        };
        $.ajax(requestConfig).then(function(response) {
        });
    });
})(window.jQuery);