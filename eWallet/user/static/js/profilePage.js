$(document).ready(function() {
    $("#editButton").click(function() {
        $("input, textarea").removeAttr("readonly");
        $("#updateButton").show();
        $("#editButton").hide();
        $('#profileTag, #profileImage').show(); // Show the label and input elements
    });

    $("#profileForm").submit(function(event) {
        
        // Perform AJAX update here and then...
        $("input, textarea").attr("readonly", true);
        $("#updateButton").hide();
        $("#editButton").show();
        $('#profileTag, #profileImage').hide(); // Hide the label and input elements
    });
});
