document.addEventListener('DOMContentLoaded', () => {
    const history = document.getElementById('history');
    const usernameInput = document.getElementById('username');
    const userMessageInput = document.getElementById('userMessage');
    const inputForm = document.getElementById('inputForm');

    const websocket = new WebSocket('ws://localhost:8765');

    websocket.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);
        const clientUsername = data.username;
        const clientMessage = data.message;
        
        const label = document.createElement('label');
        const message = document.createElement('p');
        const text = document.createTextNode(" : " + clientMessage);
        
        label.appendChild(document.createTextNode(clientUsername));
        label.style.color = "#" + data.color;
        message.appendChild(label);
        message.appendChild(text);
        history.appendChild(message);
    });

    inputForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const data = {
            username: usernameInput.value,
            message: userMessageInput.value
        };
        await websocket.send(JSON.stringify(data));
        userMessageInput.value = '';
    });

    websocket.addEventListener('close', () => {
        console.log('WebSocket client disconnected');
    });
});
