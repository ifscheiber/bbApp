// Recover Password Interceptor
document.getElementById('forgot-password-form').addEventListener('submit', function(event) {
    console.log('FORM SUBMITTED VIA AJAX')
    event.preventDefault();  // Prevent the default form submission behavior

    // Get the email value from the form
    const email = document.getElementById('recovery-email-box').value;

    // Send an AJAX request
    fetch('/recover_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Server response was not ok.');
            }
        })
        .then(data => {
            // Handle the response (e.g., show a message to the user)
            alert(data.message);
        });
});


