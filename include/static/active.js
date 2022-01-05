const tabs = document.getElementsByClassName('collapse-menu')[0].getElementsByTagName('a');

for (let i = 0; i < tabs.length; i++) 
    if (location.href === tabs[i].href) 
        tabs[i].classList.add('active');