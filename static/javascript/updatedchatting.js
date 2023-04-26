// Global variables

let jsonData = [];
var buttonName;
var mylist = [];
var content;

// user response and adding event through handle button click

function UserResponse() {
  // Handle button click events

  var buttons = document.getElementsByClassName("btn-quick-reply");
  var chatBox = document.querySelector(".chat-box");

  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", handleButtonClick);
  }

  function handleButtonClick(event) {
    buttonName = event.target.id;

    // Display the user's message

    var userMsgDiv = document.createElement("div");
    userMsgDiv.classList.add("chat", "outgoing");
    userMsgDiv.innerHTML = `
      <div class="details">
        <p class="user-msg">${buttonName}</p>
      </div>
      <img class="userImg" src="/static/images/logo-figma.png" alt="" />
    `;
    chatBox.appendChild(userMsgDiv);

    fetch("/buttonmsg/" + buttonName + "/")
      .then((response) => response.json())
      .then((data) => {
        var mylist_json = data.mylist;
        mylist = JSON.parse(mylist_json);

        var botMsgDiv = document.createElement("div");
        botMsgDiv.classList.add("chat", "incoming1");

        var img = document.createElement("img");
        img.setAttribute("src", "/static/images/logo-figma.png");
        img.classList.add("userImg")
        img.style.width = "35px";
        img.style.height = "35px";

        var detailsDiv = document.createElement("div");
        detailsDiv.classList.add("details1");

        var pTag = document.createElement("p");
        pTag.setAttribute("id", "bot-msg");
        // pTag.innerHTML = mylist.join("<br>");
        var corekey = mylist[mylist.length-1]
        for (var i = 0; i < mylist.length-1; i++) {
          // imp code
          var button = document.createElement("button");
          button.classList.add("button_bot_response");
          button.innerHTML = mylist[i];

          button.addEventListener("click", function () {
            content = this.textContent;
            var subButtonUserResponse = document.createElement("div");
            subButtonUserResponse.classList.add("chat", "outgoing", "userImg");
            subButtonUserResponse.innerHTML = `

            <div class="details">
           <p class="user-msg">${content}</p>
            </div>
            <img class="userImg" src="/static/images/logo-figma.png" alt="" />
              `;
            chatBox.appendChild(subButtonUserResponse);

            chatBox.scrollTop = chatBox.scrollHeight;

            
            fetch("/subbuttonmsg/" + corekey +"/"+ content + "/")
            .then((response) => response.json())
            .then((data) =>{
            var ans=data.subbuttonresponse
            var subbuttonresponse=JSON.parse(ans)
            console.log(subbuttonresponse)
             var subButtonBotResponse = document.createElement("div");
             subButtonBotResponse.classList.add("chat", "incoming", "userImg");
             subButtonBotResponse.innerHTML = `
             <img class="userImg" src="/static/images/logo-figma.png" alt="" />
             <div class="details">
             <pre>  <p class="user-msg"> ${subbuttonresponse}</p></pre>
             </div>
               `;
             chatBox.appendChild(subButtonBotResponse);
             
             chatBox.scrollTop = chatBox.scrollHeight;

            })

          });
          // bot response for main button
          pTag.appendChild(button);
          chatBox.appendChild(botMsgDiv);
          botMsgDiv.appendChild(img);
          botMsgDiv.appendChild(detailsDiv);
          detailsDiv.appendChild(pTag);




          // imp code ends
          // Scroll to the bottom of the chat box
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      });
  }
}

UserResponse();


