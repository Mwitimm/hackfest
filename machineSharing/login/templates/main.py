import requests


def send_message(message):
    url = 'http://localhost:3000/send-message'
    message_content = message

    # Create a dictionary with the message content
    payload = {'message': message_content}

    try:
        response = requests.post(url, json=payload)  # Use 'json' instead of 'params'
        response.raise_for_status()  # Check for any errors in the response
        print(response.text)  # Print the response from the Node.js app
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

