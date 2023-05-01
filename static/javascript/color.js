window.onscroll = function () {
  var navbar = document.getElementById("menu-bar");

  var navMembers = navbar.getElementsByTagName("a");

  if (window.pageYOffset >= 30 && window.innerWidth >= 15) {
    // navbar.style.color = "black";
    navbar.style.backgroundColor = "rgba(13, 71, 161, 0.5)"; // add light black color
    navbar.style.backdropFilter = "blur(5px)"; // add backdrop filter
  } else {
    navbar.style.color = "white";
    navbar.style.removeProperty("background-color");
    navbar.style.removeProperty("backdrop-filter"); // remove backdrop filter
  }
  
  navbar.style.transition = "all 0.3s ease-in-out"; // add transition

};
