
document.addEventListener("DOMContentLoaded", function () {
    const guessInput = document.getElementById("guess");
    const submitButton = document.getElementById("submit");
    const message = document.getElementById("message");
    const triesElement = document.getElementById("tries");

    let secretNumber = Math.floor(Math.random() * 100) + 1;
    let tries = 0;

    submitButton.addEventListener("click", function () {
        const userGuess = Number(guessInput.value);
        tries++;
        
        if (userGuess < 1 || userGuess > 100 || isNaN(userGuess)) {
            message.textContent = "Please enter a valid number between 1 and 100.";
            message.style.color = "red";
        } else if (userGuess < secretNumber) {
            message.textContent = "Too low! Try again.";
            message.style.color = "orange";
        } else if (userGuess > secretNumber) {
            message.textContent = "Too high! Try again.";
            message.style.color = "orange";
        } else {
            message.textContent = `Congratulations! You guessed the number in ${tries} tries.`;
            message.style.color = "green";
            secretNumber = Math.floor(Math.random() * 100) + 1; // Restart the game
            tries = 0; // Reset the tries count
        }

        triesElement.textContent = tries;
    });
});