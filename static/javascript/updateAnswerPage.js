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
        fetch("/keywordMsg/" + selectedValue + "/")
          .then((response) => response.json())
          .then((data) => {
            var KeywordResponseList_json = data.KeywordResponseList;
            KeywordResponseList = JSON.parse(KeywordResponseList_json);
            console.log(KeywordResponseList);
            jsonList.innerText = KeywordResponseList;
          });
          fetch("/buttonmsg/" + selectedValue + "/")
          .then((response) => response.json())
          .then((data) => {
            var mylist_json = data.mylist;
            mylist = JSON.parse(mylist_json);
            console.log(mylist)
            for(let j = 0; j < mylist.length-1; j++){
                var subKeyDisplay = document.createElement("option")
                subKeyDisplay.value = mylist[j];
                subKeyDisplay.text = mylist[j];
                subKey.appendChild(subKeyDisplay)
            }
          })
      });
    });
});

function inputUpdate(event) {
  event.preventDefault(); // Prevents default form submission behavior
  const inputField = document.getElementById("subKey").value;
  const subKeyVal = document.getElementById("coreKey").value;
  const updatedAnswer = document.getElementById("updatedAnswer").value;

  console.log(`CoreKey: ${subKeyVal}`);
  console.log(`Input field: ${inputField}`);
  console.log(`textfield:  ${updatedAnswer}`)
  // if (subKeyVal === "" || inputField === "") {
  //   alert("Choose options!");
  // } else {
    fetch("/updatedAns/" + subKeyVal + "/" + inputField + "/" + updatedAnswer + "/")
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);
    })
  // }
}


