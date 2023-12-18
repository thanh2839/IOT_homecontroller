let mybutton = document.getElementById("backtoheader");
window.onscroll = function () {
    scrollFunction();
};
function scrollFunction() {
    if (
        document.body.scrollTop > 20 ||
        document.documentElement.scrollTop > 20
    ) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}
// ---------------------------------------

// -----------------------------------------------
function previewImage(event) {
    var file = event.target.files[0];
    if (file.size > 1024 * 1024) {
        alert("Image size should not exceed 1MB");
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        var preview = document.getElementById("thumbnail");
        preview.src = reader.result;
    };
    reader.readAsDataURL(file);
}

function validateForm() {
    const thumbnail = document.getElementById("thumbnail");
    if (thumbnail.getAttribute("src") === "data:image/png;base64,null") {
        alert("Hãy chọn 1 ảnh");
        return false;
    }

    return true;
}
const toggleButton = document.getElementById("toggleButton");
document.addEventListener("DOMContentLoaded", async () => {
    await fetch("/api/getStatus")
        .then((response) => {
            if (response.ok) return response.text();
            throw new Error("Response Error");
        })
        .then((data) => {
            if (data == "true") toggleButton.checked = true;
            else if (data == "false") toggleButton.checked = false;
        })
        .catch((error) => {
            console.error(error);
        });
});
toggleButton.addEventListener("click", async () => {
    const confirmed = confirm("Bạn có chắc chắn muốn thay đổi trạng thái cửa không?");
    if (!confirmed) {
        return; 
    }
    const apiUrl = toggleButton.checked ? "/api/open-door" : "/api/close-door";
    await fetch(apiUrl)
        .then((response) => {
            if (response.ok) return response.text();
            throw new Error("Response Error");
        })
        .then((data) => {})
        .catch((error) => {
            console.error(error);
        });
});

var currentUserId;
let sock = new SockJS("http://localhost:8080/stomp");
let client = Stomp.over(sock);
client.connect({}, (frame) => {
    client.subscribe("/topic/status", (payload) => {
        var user = JSON.parse(payload.body);
        if (user.status != null) toggleButton.checked = user.status;
    });
});
