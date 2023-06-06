// preserve button state (buttons on the sidebar) on page reload (using local storage)
// Read and set initial state for each button on page load
window.onload = function () {
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

        // Get all the collapsible buttons
        var buttons = document.getElementsByClassName('keep-state-button');

        // Collapse all other buttons except the clicked one
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i] !== button) {
                buttons[i].setAttribute('aria-expanded', 'false');
                var target = buttons[i].dataset.bsTarget;
                var toggle = new bootstrap.Collapse(document.querySelector(target), {
                    toggle: false
                })
                toggle.hide();
            }
        }




    // // save the state of the button being clicked
    // var button = document.getElementById(buttonID);
    // var currentState = button.getAttribute("aria-expanded");
    //
    // var buttons = document.querySelectorAll('.keep-state-button');
    //
    //     buttons.forEach(function (button) {
    //     button.setAttribute("aria-expanded", "false");
    // });
    //
    // buttons.forEach(function (button) {
    //     var buttonId = button.getAttribute("id");
    //     // close all buttons
    //     //button.setAttribute("aria-expanded", "false");
    //     // in local storage, set the state of all buttons to closed
    //     try {
    //         localStorage.setItem("button-state-" + buttonId, "closed");
    //
    //     } catch (error) {
    //         console.log('Error caught successfully:', error.message)
    //     }
    // })
    //
    // // if the button was initially closed, open it and store the state in local storage
    // if (currentState === "true") {
    //     button.setAttribute("aria-expanded", "true");
    //     localStorage.setItem("button-state-" + buttonID, "open");
    //
    // }
    //
    // // if the button is open, close it and store the state
    // if (currentState === "true") {
    //     //button.setAttribute("aria-expanded", "false");
    //     localStorage.setItem("button-state-" + buttonID, "open");
    //     // if the button is closed, open it and store the state
    // } else {
    //     //button.setAttribute("aria-expanded", "true");
    //     localStorage.setItem("button-state-" + buttonID, "closed");
    // }
}