window.onscroll = function () {
  var navbar = document.getElementById("menu-bar");


  var navMembers = navbar.getElementsByTagName("a");

  if (window.pageYOffset >= 900 && window.innerWidth >= 850) {
    navbar.style.color = "black";

    for (var i = 0; i < navMembers.length; i++) {
      navMembers[i].style.color = "black";
    }
  } else {
    for (var i = 0; i < navMembers.length; i++) {
      navMembers[i].style.removeProperty("color");
    }
    navbar.style.color = "white";

  }
};
