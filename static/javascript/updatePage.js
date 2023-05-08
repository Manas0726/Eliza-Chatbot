
var KeywordResponseList = [];
let selectedValue
const jsonList = document.getElementById("jsonList");

document.addEventListener("DOMContentLoaded", function (event) {
  const coreKey = document.getElementById("coreKey");
  const subKey = document.getElementById("subKey");
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
        selectedValue = event.target.value;
        console.log(selectedValue);
        // Clear the subKey options before making the fetch request
        subKey.innerHTML = "";
        fetch("/keywordMsg/" + selectedValue + "/")
          .then((response) => response.json())
          .then((data) => {
            // var KeywordResponseList_json = data.KeywordResponseList;
            // KeywordResponseList = JSON.parse(KeywordResponseList_json);
            // console.log(KeywordResponseList);
            // jsonList.innerText = KeywordResponseList;
          });
          fetch("/buttonmsg/" + selectedValue + "/")
          .then((response) => response.json())
          .then((data) => {
            var mylist_json = data.mylist;
            mylist = JSON.parse(mylist_json);
            console.log(mylist)
            for(let j = 0; j < mylist.length-1 ; j++){
              var subKeyDisplay = document.createElement("option")
              subKeyDisplay.value = mylist[j];
              subKeyDisplay.text = mylist[j];
              subKey.appendChild(subKeyDisplay)
            }
          })
      });
    });
});


// const myForm = document.querySelector('#myForm');
// const result = document.getElementById('result');

// function inputFetch() {
//   const inputField = document.getElementById("subKey").value;
//   const updatedKey = document.getElementById("textInput").value;
//   const subKeyVal = document.getElementById("coreKey").value;

//   fetch("/updatedKey/" + subKeyVal + "/" + inputField + "/" + updatedKey + "/")
//     .then((response) => response.json())
//     .then((data) => {
//       if (data.success) {
//         result.innerText = data.message;
//         console.log(data.message);
//         document.getElementById("subKey").value = "";
//           document.getElementById("corekey").value = "";
//           location.reload();
//       } else {
//         result.innerText = data.message;
//         console.log("already exists");
//       }
//     });
// }

// myForm.addEventListener('submit', function(event) {
//   event.preventDefault(); // prevent the form from being submitted

//   let coreKey = document.querySelector('#coreKey');
//   let subKey = document.querySelector('#subKey');
//   let textInput = document.querySelector('#textInput');

//   if (coreKey.value === 'Choose from here' || subKey.value === 'Choose from here' || textInput.value === 'Choose from here' ) {
//     alert('Please choose a valid option!');
//   } else {
//     // Submit the form using fetch
//     inputFetch();
//   }
// });

function inputFetch() {
  const inputField = document.getElementById("subKey").value;
  const updatedKey = document.getElementById("textInput").value;
  const subKeyVal = document.getElementById("coreKey").value;
  const result = document.getElementById("result");

  if (subKeyVal === "Choose from here" || inputField === "Choose from here" || updatedKey === "Choose from here") {
    alert("Choose options!");
  } else {
    fetch("/updatedKey/" + subKeyVal + "/" + inputField + "/" + updatedKey + "/")
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // result.innerText = data.message;
          alert(data.message);
          document.getElementById("subKey").value = "";
          document.getElementById("textInput").value = "";
          document.getElementById("coreKey").value = "";
          location.reload();
        } else {
          // result.innerText = data.message;
          alert(data.message);
          document.getElementById("subKey").value = "";
          document.getElementById("textInput").value = "";
          document.getElementById("coreKey").value = "";
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
  const textArea = document.querySelector('#textInput');

  if (coreKey.value === 'Choose from here' && subKey.value === 'Choose from here' && textArea.value === 'Choose from here') {
    alert('Please enter some values!');
    
  } else {
    // Submit the form using fetch
    inputFetch();
  }
});
