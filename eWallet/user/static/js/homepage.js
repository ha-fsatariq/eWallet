// homepage.js
$(document).ready(function() {
    // Initially show the amount
    $('#amount').show();
    
    // Toggle amount visibility on button click
    $('.btn-action').click(function() {
        $('#amount').toggle();
        $(this).text(function(i, text) {
            return text === 'Hide Balance' ? 'Show Balance' : 'Hide Balance';
        });
    });
});
