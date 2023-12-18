var liElements = document.querySelectorAll('.people li');
var firstLi = liElements[0];
var spanText = firstLi.querySelector('.name').textContent;

document.querySelector('.chat[data-chat="' + spanText + '"]').classList.add('active-chat');
document.querySelector('.person[data-chat="' + spanText + '"]').classList.add('active');


let friends = {
    list: document.querySelector('ul.people'),
    all: document.querySelectorAll('.left .person'),
    name: ''
  },
  chat = {
    container: document.querySelector('.message-container .right'),
    current: null,
    person: null,
    name: document.querySelector('.message-container .right .top .name')
  }

friends.all.forEach(f => {
  f.addEventListener('mousedown', () => {
    f.classList.contains('active') || setAciveChat(f)
  })
});

function setAciveChat(f) {
  friends.list.querySelector('.active').classList.remove('active')
  f.classList.add('active')
  chat.current = chat.container.querySelector('.active-chat')
  chat.person = f.getAttribute('data-chat')
  chat.current.classList.remove('active-chat')
  chat.container.querySelector('[data-chat="' + chat.person + '"]').classList.add('active-chat')
  friends.name = f.querySelector('.name').innerText
  chat.name.innerHTML = friends.name
}


// -------------------------------------------
function searchByName() {
  var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("searchMessager");
    filter = input.value.toUpperCase();
    ul = document.getElementById("messagerList");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("span")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
// -------------------------------------------
// -------------------------------------------

var currentUserId 
let sock = new SockJS("http://localhost:8080/stomp");
let client = Stomp.over(sock);

//Nhận tin nhắn
client.connect({}, (frame) => {
  client.subscribe("/topic/messages", (payload) => {
    var chatMessage = JSON.parse(payload.body);
  });
});

// Gửi tin nhắn
var forms = document.getElementsByTagName("form");
for (var i = 0; i < forms.length; i++) {
  forms[i].addEventListener("submit", function (event) {
    event.preventDefault();
    var form = event.target;
    var action = form.getAttribute("action");
    var parts = action.split("/");
    var chatRoomId = parts[2];
    var senderId = parts[3];
    currentUserId = senderId;
    var recipientId = parts[4];
    var content = form.querySelector("input[name='content']").value;
    var chatMessage = {
      chatRoomId: chatRoomId,
      senderId: senderId,
      recipientId: recipientId,
      content: content,
    };

    client.send('/app/chat', {}, JSON.stringify(chatMessage));

    var chatRoom = form.closest(".chat");
    var bubbleHtml = '<div class="' + "bubble me" + '">' + content + "</div>";
    chatRoom.insertAdjacentHTML("beforeend", bubbleHtml);
    form.querySelector("input[name='content']").value = "";
  });
}
