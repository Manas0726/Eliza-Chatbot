var KeywordResponseList = [];
const jsonList = document.getElementById("jsonList");
const result = document.getElementById("result");

document.addEventListener("DOMContentLoaded", function (event) {
  const coreKey = document.getElementById("coreKey");
  // Fetch the major and sub keywords from the server
  fetch("/coreKeyword/")
    .then((response) => response.json())
    .then((data) => {
      const MajorKeyword_json = data.MajorKeyword;
      const MajorKeyword = JSON.parse(MajorKeyword_json);

      // Populate the major keyword options
      for (let i = 0; i < MajorKeyword.length; i++) {
         var coreKeyDisplay = document.createElement("option");
        coreKeyDisplay.value = MajorKeyword[i];
        coreKeyDisplay.text = MajorKeyword[i];
        coreKey.appendChild(coreKeyDisplay);
      }
      coreKey.addEventListener("change", function (event) {
        const selectedValue = event.target.value;
        console.log(selectedValue);
        fetch("/keywordMsg/" + selectedValue + "/")
          .then((response) => response.json())
          .then((data) => {
            var KeywordResponseList_json = data.KeywordResponseList;
            KeywordResponseList = JSON.parse(KeywordResponseList_json);
            console.log(KeywordResponseList);
            jsonList.innerText = KeywordResponseList;
          });
      });
    });
});

// new Subkeyword storing

function inputFetch() {
  const inputField = document.getElementById("subKey").value;
  const textField = document.getElementById("textArea").value;
  const subKeyVal = document.getElementById("coreKey").value;
  const result = document.getElementById("result");

  if (subKeyVal === "" || inputField === "" || textField === "") {
    alert("Choose options!");
  } else {
    fetch("/addElement/" + subKeyVal + "/" + inputField + "/" + textField + "/")
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // result.innerText = data.message;
          alert(data.message);
          document.getElementById("subKey").value = "";
          document.getElementById("textArea").value = "";
          location.reload();
        } else {
          // result.innerText = data.message;
          alert("already exists");
          document.getElementById("subKey").value = "";
          document.getElementById("textArea").value = "";
          document.getElementById("coreKey").value;
          location.reload();
        }
      });
  }
}

const myForm = document.querySelector('#myForm');

myForm.addEventListener('submit', function(event) {
  event.preventDefault(); // prevent the form from being submitted

  const coreKey = document.querySelector('#coreKey');
  const subKey = document.querySelector('#subKey');
  const textArea = document.querySelector('#textArea');

  if (coreKey.value === '' && subKey.value === '' && textArea.value === '') {
    alert('Please enter some values!');
    
  } else {
    // Submit the form using fetch
    inputFetch();
  }
});

