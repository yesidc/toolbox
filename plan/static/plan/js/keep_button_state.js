// preserve button state (buttons on the sidebar) on page reload (using local storage)
// Read and set initial state for each button on page load
window.onload = function ()  {
    var buttons = document.querySelectorAll('.keep-state-button');
    buttons.forEach(function (button) {
        var buttonId = button.getAttribute("id");
        var buttonState = localStorage.getItem("button-state-" + buttonId);
        if (buttonState === "open") {
            button.setAttribute("aria-expanded", "true");
            var target = button.dataset.bsTarget;
            var toggle = new bootstrap.Collapse(document.querySelector(target), {
                toggle: false
            });
            toggle.show();
        } else if (buttonState === "closed") {
            button.setAttribute("aria-expanded", "false");
            var target = button.dataset.bsTarget;
            var toggle = new bootstrap.Collapse(document.querySelector(target), {
                toggle: false
            });
            toggle.hide();
        } else {
            // If no state is stored in localStorage, use the default state specified in the data-button-state attribute
            var defaultButtonState = button.dataset.buttonState;
            if (defaultButtonState === "open") {
                button.setAttribute("aria-expanded", "true");
            } else if (defaultButtonState === "closed") {
                button.setAttribute("aria-expanded", "false");
            }
        }
    });
}

// todo remove button from the local storage when the plan is deleted.
// Function to toggle and store button state
function toggleButtonState(buttonID) {
    var button = document.getElementById(buttonID);
    var currentState = button.getAttribute("aria-expanded");
    // if the button is open, close it and store the state
    if (currentState === "true") {
        //button.setAttribute("aria-expanded", "false");
        localStorage.setItem("button-state-" + buttonID, "open");
        // if the button is closed, open it and store the state
    } else {
        //button.setAttribute("aria-expanded", "true");
        localStorage.setItem("button-state-" + buttonID, "closed");
    }
}