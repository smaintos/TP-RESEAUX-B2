const WebSocket = require('ws');

const websocket = new WebSocket('ws://localhost:8765');

websocket.on('open', () => {
  console.log('Connecté au serveur WebSocket');

  websocket.send('Hello, serveur !');
});

websocket.on('message', (data) => {
  console.log(`Client a reçu: ${data}`);
});

const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on('line', async (userInput) => {
  await websocket.send(userInput);
});
