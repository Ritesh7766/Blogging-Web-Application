document.querySelector('#mobile-menu').addEventListener('click', function() {
    document.getElementsByClassName('navbar')[0].classList.toggle('navbar-height');
    document.getElementsByClassName('collapse-menu')[0].classList.toggle('dropdown');
    this.classList.toggle('is-active');
});