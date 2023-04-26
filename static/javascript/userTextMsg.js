  // // Get the submit button and input field
  // var rasamsg;
  // const submitBtn = document.getElementById("sendMsg");
  // const inputField = document.getElementById("textInput");

  // // Add event listener to submit button
  // submitBtn.addEventListener("click", (event) => {
  //   // Prevent the default form submission behavior
  //   event.preventDefault();

  //   // Get the value of the input field
  //   const inputValue = inputField.value;
  //   console.log(inputValue);
  //   fetch("/rasachat/" + inputValue + "/")
  //     .then((response) => response.json())
  //     .then((data) => {
  //       rasamsg = data.msg;
  //       console.log(data.msg);
  //       var subButtonUserResponse = document.createElement("div");
  //       subButtonUserResponse.classList.add("chat", "incoming", "responseImageContainer", "responseImg");
  //       subButtonUserResponse.innerHTML = `
  //         <img src="/static/images/logo-figma.png" alt="" />
  //         <div class="details">
  //       <p class="user-msg">${rasamsg}</p>
  //        <div class="responseImageContainer">
  //          <img class="responseImg" src="/static/images/background6.jpg" alt="">
  //        </div>

  //           `;
  //       chatBox.appendChild(subButtonUserResponse);

  //       chatBox.scrollTop = chatBox.scrollHeight;
  //     });

  //   if (inputValue.trim() === "") {
  //     alert("Please enter a message");
  //     return;
  //   } else {
  //     var chatBox = document.querySelector(".chat-box");
  //     var userMsgDiv = document.createElement("div");
  //     userMsgDiv.classList.add("chat", "outgoing");
  //     userMsgDiv.innerHTML = `
  //           <div class="details">
  //             <p class="user-msg">${inputValue}</p>
  //           </div>
  //           <img class="userImg" src="/static/images/20220326_161638.jpg" alt="" />
  //         `;
  //     chatBox.appendChild(userMsgDiv);
  //     // Clear the input field
  //     inputField.value = "";

  //     chatBox.scrollTop = chatBox.scrollHeight;
  //   }
  // });












// Get the submit button and input field
var rasamsg;
const submitBtn = document.getElementById("sendMsg");
const inputField = document.getElementById("textInput");
const chatBox = document.querySelector(".chat-box");

// Add event listener to submit button
submitBtn.addEventListener("click", (event) => {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Get the value of the input field
  const inputValue = inputField.value;

  if (inputValue.trim() === "") {
    alert("Please enter a message");
    return;
  } else {
    // Create the user message div and add it to the chat box
    const userMsgDiv = document.createElement("div");
    userMsgDiv.classList.add("chat", "outgoing");
    userMsgDiv.innerHTML = `
      <div class="details">
        <p class="user-msg">${inputValue}</p>
      </div>
      <img class="userImg" src="/static/images/20220326_161638.jpg" alt="" />
    `;
    chatBox.appendChild(userMsgDiv);

    // Clear the input field
    inputField.value = "";

    // Create the loader div and add it to the chat box
    const loaderDiv = document.createElement("div");
    loaderDiv.classList.add("chat", "incoming");
    loaderDiv.innerHTML = `
      <img class="botImg" src="/static/images/logo-figma.png" alt="" />
      <div class="details">
        <p class="load" id="load_id">
          <span class="loader-bar-2"></span>
          <span class="loader-bar-2"></span>
          <span class="loader-bar-2"></span>
        </p>
      </div>
    `;
    chatBox.appendChild(loaderDiv);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send the user message to Rasa
    fetch(`/rasachat/${inputValue}/`)
      .then((response) => response.json())
      .then((data) => {
        // Remove the loader div from the chat box
        chatBox.removeChild(loaderDiv);

        // Create the Rasa message div and add it to the chat box
        const rasamsgDiv = document.createElement("div");
        rasamsgDiv.classList.add("chat", "incoming", "responseImageContainer", "responseImg");
        rasamsgDiv.innerHTML = `
          <img src="/static/images/logo-figma.png" alt="" />
          <div class="details">
            <p class="user-msg">${data.msg}</p>
            <div class="responseImageContainer">
              <img class="responseImg" src="/static/images/background6.jpg" alt="">
            </div>
          </div>
        `;
        chatBox.appendChild(rasamsgDiv);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
      });
  }
});
