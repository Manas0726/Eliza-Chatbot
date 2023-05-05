function sendEmail(event) {
    event.preventDefault();
    const form = document.querySelector("form");
    const formData = new FormData(form);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_email", true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        const response = xhr.responseText;
        console.log(response);
        if (response === "success") {
          form.reset();
          const statusTxt = form.querySelector(".button-area span");
          statusTxt.style.color = "green";
          statusTxt.style.display = "block";
          statusTxt.innerText = "Your message has been sent!";
          setTimeout(() => {
            statusTxt.style.display = "none";
          }, 3000);
        }
      }
    }
    console.log(formData);
    xhr.send(formData);
  }
  