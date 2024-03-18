document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const errorDisplay = document.getElementById('error');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const fileInput = document.getElementById('resume_file');
        const file = fileInput.files[0];

        if (!file) {
            errorDisplay.textContent = 'Please select a file.';
            return;
        }

        // Clear any previous error message
        errorDisplay.textContent = '';

        // You can perform additional validation or processing here before submitting the form
        form.submit(); // Submit the form
    });
});
