function previewBannerImage(input) {
    const file = input.files[0];
    const preview = document.getElementById('banner-preview');
    const image = document.getElementById('banner-image');
    const removeButton = document.querySelector('#banner-preview .remove-button');

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            if (image) {
                image.src = e.target.result;
            } else {
                const newImage = document.createElement('img');
                newImage.id = 'banner-image';
                newImage.src = e.target.result;
                newImage.classList.add('preview-image');
                preview.appendChild(newImage);
            }

            if (removeButton) {
                removeButton.style.display = 'block';
            }
        }

        reader.readAsDataURL(file);
    }
}

function removeBannerImage() {
    document.getElementById('id_banner').value = '';
    document.getElementById('banner-image').src = '/media/bgs/default/default_banner.png';
}

function previewAvatarImage(input) {
    const file = input.files[0];
    const preview = document.getElementById('avatar-preview');
    const image = document.getElementById('avatar-image');
    const removeButton = document.querySelector('#avatar-preview .remove-button');

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            if (image) {
                image.src = e.target.result;
            } else {
                const newImage = document.createElement('img');
                newImage.id = 'avatar-image';
                newImage.src = e.target.result;
                newImage.classList.add('preview-image');
                preview.appendChild(newImage);
            }

            if (removeButton) {
                removeButton.style.display = 'block';
            }
        };
        reader.readAsDataURL(file);
    }
}

function removeAvatarImage() {
    document.getElementById('id_avatar').value = '';
    document.getElementById('avatar-image').src = '/media/avatars/default/default_avatar_light.png';
}