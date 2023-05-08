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
            result.innerText = KeywordResponseList;
          });
      });
    });
});