document.getElementsByClassName('danger-btn')[0].addEventListener('click', function() {
    document.getElementById('delete').classList.toggle('activate')
});

document.getElementById('submit').addEventListener('click', function() {
    document,this.getElementsByClassName('modal-bg')[0].classList.toggle('activate');
});

Array.from(document.getElementsByClassName('modal-bg')).forEach(element => {
    element.getElementsByClassName('close2')[0].addEventListener('click', function() {
        element.classList.toggle('activate');
    });
});