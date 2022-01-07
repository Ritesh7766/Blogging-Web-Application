const options = document.getElementById('options').getElementsByTagName('button');

options[0].addEventListener('click', function() {
    document.getElementById('update').classList.toggle('activate')
});

Array.from(document.getElementsByClassName('modal-bg')).forEach(element => {
    element.getElementsByClassName('close2')[0].addEventListener('click', function() {
        element.classList.toggle('activate');
    });
});