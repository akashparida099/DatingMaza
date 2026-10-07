function likeUser(name) {
    Swal.fire({
        title: 'Liked! ❤️',
        text: 'You liked ' + name + '. If they like you too, it will be a match!',
        icon: 'success',
        confirmButtonText: 'Keep Discovering',
        confirmButtonColor: '#dc3545'
    });
}

function passUser(name, button) {
    Swal.fire({
        title: 'Pass on ' + name + '?',
        text: 'We will show you another profile.',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes, Pass',
        cancelButtonText: 'Cancel',
        confirmButtonColor: '#6c757d'
    }).then(function(result) {
        if (result.isConfirmed) {
            var card = $(button).closest('.col-lg-4');
            card.fadeOut(400);
        }
    });
}

function applyFilters() {
    Swal.fire({
        title: 'Filters Applied 💕',
        text: 'Your discovery preferences have been updated.',
        icon: 'success',
        timer: 1600,
        showConfirmButton: false
    });
}