const close_buttons = document.getElementsByClassName('icon');

for (let i = 0; i < close_buttons.length; i++) {
    close_buttons[i].addEventListener('click', function() {
        const alerts = document.getElementsByClassName('alert');
        for (let i = 0; i < alerts.length; i++)
            alerts[i].remove();
    });
}