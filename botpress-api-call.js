const SIMULATOR_URL = 'http://localhost:5000/api/message';

// Message and user ID to send
const message = "Hello there!";
const userId = 'botpress_user';

// Make the API call
fetch(SIMULATOR_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: message,
    user_id: userId
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
})
.then(data => {
  console.log('Bot response:', data.response);
})
.catch(error => {
  console.error('Error calling simulator:', error);
}); 