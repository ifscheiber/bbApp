$(document).ready(function() {
    $("#form-login").submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting immediately

        // Get form data
        var formData = $(this).serialize();

        // AJAX request
        $.post("/login", formData, function(response) {
            if (response.success) {
                let navbarLogo = document.getElementById("navbar-logo-login"); // Replace with the actual ID of your navbar logo
                let position = navbarLogo.getBoundingClientRect();


                // Play the animation
                $("#content-login").fadeOut(function() {
                    $("#navbar-login").fadeIn(function() {
                        // This code will run after the fadeIn completes
                        $(this).css("display", "flex"); // or whatever display value you want
                    });
                    $("#logo-login").css({
                        "height": "75px",
                        "top": 0,
                        "left": "500px",
                        "transform": "none"
                    });

                    // After animation, redirect
                    setTimeout(function() {
                        window.location.href = response.redirect_url;
                    }, 1000);
                });
            } else {
                // Display error message
                alert(response.message);
            }
        });
    });
});
