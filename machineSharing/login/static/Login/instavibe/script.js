document.getElementById('profile-picture-input').addEventListener('change', function () {
    var file = this.files[0];
    var img = document.querySelector('.profile-picture img');
    var reader = new FileReader();

    reader.onloadend = function () {
        img.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    }
});

document.getElementById('save-btn').addEventListener('click', function () {
    var location = document.getElementById('location').value;
    var bio = document.getElementById('bio').value;
    var hashtags = document.getElementById('hashtags').value;

    // Save the information to the server or perform other actions as needed
});
