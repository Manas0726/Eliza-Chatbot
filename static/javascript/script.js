window.addEventListener('scroll', function(){
    
    let navbar = document.getElementsById('menu-bar');

    if(window.pageYOffset >= 0) {
        navbar.idList.add('sticky');
    }else {
        navbar.classList.remove('sticky');
    }
});