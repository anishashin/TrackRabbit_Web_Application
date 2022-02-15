(function($) {
    $('#start').click(function() {
        var requestConfig = {
            method: 'GET',
            url: '/start',
            contentType: 'application/json',
            beforeSend: function() {
                $('#start').prop('disabled', true);
                let timeout = $("#submittedSeconds").val();
                timeout = parseInt(timeout);
                console.log(typeof timeout);
                // setTimeout(function() {
                //     $('#start').prop('disabled', false);
                // }, $("#submittedSeconds").val());
            }
        };
        $.ajax(requestConfig).then(function(response) {
        });
    });
})(window.jQuery);