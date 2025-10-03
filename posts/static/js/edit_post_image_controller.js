function preview_post_image(input, index) {
    const file = input.files[index];
    const attachment_block = document.querySelector(".attachments");
    const attachment = document.getElementById("attachment");
    const removeButton = document.querySelector("#attachment-preview .remove-button");

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            if (attachment) {
                attachment.src = e.target.result;
            } else {
                const newImage = document.createElement('img');
                newImage.id = "attachment";
                newImage.src = e.target.result;
                newImage.classList.add('preview-attachment');
                attachment_block.appendChild(newImage);
            }

            if (removeButton) {
                removeButton.style.display = "block"
            }
        }

        reader.readAsDataURL(file)
    }
}

function removeAttachment() {
    document.getElementById('id_attachment').value = "";
    document.getElementById("attachment").src = "";
}