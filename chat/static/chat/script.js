var friendName = document.querySelector('#friendName').textContent;
setInterval(() => {
    fetch('https://chatappp.pythonanywhere.com/get_messages/'+friendName)
    .then(res => res.json())
    .then(data => {
        console.log(data);
        if(data.unread_messages) {
            data.unread_messages.forEach(message => {
                const div = document.querySelector('#messages');
                const div_message = document.createElement('div');
                div_message.style.border = '1px solid black';
                div_message.innerHTML = `${friendName}: <b>${message}</b>`;
                div.prepend(document.createElement('br'), div_message);            
            });
        }
    });
}, 2000);