document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    const chatbotStates = {
        GREETING: 'greeting',
        STATE: 'state',
        DISTRICT: 'district',
        CITY: 'city',
        MUSEUM: 'museum',
        ADULTS: 'adults',
        CHILDREN: 'children',
        PAYMENT: 'payment'
    };

    let currentState = chatbotStates.GREETING;
    let bookingInfo = {};
    let museums = [];

    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
        messageElement.innerHTML = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getMuseums() {
        fetch('/get_museums', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                state: bookingInfo.state,
                district: bookingInfo.district,
                city: bookingInfo.city
            }),
        })
        .then(response => response.json())
        .then(data => {
            museums = data;
            if (museums.length > 0) {
                let museumList = "Here are the available museums:<br>";
                museums.forEach((museum, index) => {
                    museumList += `${index + 1}. ${museum.name}<br>`;
                });
                museumList += "Please enter the number of the museum you'd like to visit.";
                addMessage(museumList);
                currentState = chatbotStates.ADULTS; // Transition to ADULTS state after displaying the museum list
            } else {
                addMessage("No museums available for the selected location. Please try again.");
                currentState = chatbotStates.GREETING;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            addMessage("Sorry, I couldn't fetch the museum list. Please try again later.");
            currentState = chatbotStates.GREETING;
        });
    }

    function botResponse(message) {
        switch (currentState) {
            case chatbotStates.GREETING:
                addMessage("Hello! Welcome to the Museum Ticket Booking Chatbot. How can I assist you today?");
                currentState = chatbotStates.STATE;
                break;
            case chatbotStates.STATE:
                addMessage("Great! To help you book museum tickets, I'll need some information. Please enter your state.");
                currentState = chatbotStates.DISTRICT;
                break;
            case chatbotStates.DISTRICT:
                bookingInfo.state = message;
                addMessage("Thank you! Now, please enter your district.");
                currentState = chatbotStates.CITY;
                break;
            case chatbotStates.CITY:
                bookingInfo.district = message;
                addMessage("Excellent! Please enter your city.");
                currentState = chatbotStates.MUSEUM;
                break;
            case chatbotStates.MUSEUM:
                bookingInfo.city = message;
                getMuseums();
                // Stay in the MUSEUM state until user selects a valid museum
                break;
            case chatbotStates.ADULTS:
                const museumIndex = parseInt(message) - 1;
                if (museumIndex >= 0 && museumIndex < museums.length) {
                    bookingInfo.museum = museums[museumIndex];
                    addMessage(`You've selected ${bookingInfo.museum.name}. How many adult tickets do you need?`);
                    currentState = chatbotStates.CHILDREN;
                } else {
                    addMessage("Invalid selection. Please enter a valid museum number.");
                }
                break;
            case chatbotStates.CHILDREN:
                bookingInfo.adults = parseInt(message);
                addMessage("How many child tickets do you need?");
                currentState = chatbotStates.PAYMENT;
                break;
            case chatbotStates.PAYMENT:
                bookingInfo.children = parseInt(message);
                addMessage("Great! Here's a summary of your booking:");
                addMessage(`State: ${bookingInfo.state}`);
                addMessage(`District: ${bookingInfo.district}`);
                addMessage(`City: ${bookingInfo.city}`);
                addMessage(`Museum: ${bookingInfo.museum.name}`);
                addMessage(`Adult tickets: ${bookingInfo.adults}`);
                addMessage(`Child tickets: ${bookingInfo.children}`);
                addMessage("Would you like to proceed to payment? (Yes/No)");
                break;
            default:
                if (message.toLowerCase() === 'yes') {
                    addMessage("Great! Redirecting you to the payment gateway...");
                    setTimeout(() => {
                        addMessage("Payment completed! Starting a new booking.");
                        currentState = chatbotStates.GREETING;
                        bookingInfo = {};
                        museums = [];
                        botResponse();
                    }, 2000);
                } else {
                    addMessage("Booking cancelled. Starting over.");
                    currentState = chatbotStates.GREETING;
                    bookingInfo = {};
                    museums = [];
                    botResponse();
                }
                break;
        }
    }

    sendButton.addEventListener('click', function() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            botResponse(message);
        }
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });

    // Start the conversation
    botResponse();
});
