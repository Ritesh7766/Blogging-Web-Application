document.getElementById('submit').addEventListener('click', function() {
    Array.from(document.getElementsByTagName('textarea')).forEach(element => {
        console.log('hello');
        element.value.replace(/\n/g, '<br');
    });
});