// preserve button state (buttons on the sidebar) on page reload (using local storage)
// Read and set initial state for each button on page load
window.onload = function () {
    var active_user_plan = document.getElementById("active-user-plan-data").dataset.plan;
    console.log('active user plan', active_user_plan);
        // iterate across all items in the local storage and set their value to 'closed'
        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            localStorage.setItem(key, "closed");
        }

        // set the active user plan to 'open'
        if (active_user_plan) {
            localStorage.setItem(active_user_plan, "open");
        }

    // Get all the (sidebar) anchor tags (these are the plan names)
    var buttons = document.querySelectorAll('.keep-state-button');
    buttons.forEach(function (button) {
        var buttonId = button.getAttribute("id");
        var buttonState = localStorage.getItem("button-state-" + buttonId); // buttonId === id="plan-side-bar-{{ p.plan_name |add_hyphen }}
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
// Function to toggle and store (sidebar) button state.
function toggleButtonState(buttonID) {

       //buttonID is the id of the button being clicked  where id="plan-side-bar-{{ p.plan_name |add_hyphen }}"

       var button = document.getElementById(buttonID);

        // Get all the (sidebar) collapsible buttons (these are the plan names)
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

                // in local storage, set the state buttons to closed
                try {
                    localStorage.setItem("button-state-" + buttons[i].getAttribute("id"), "closed");

                } catch (error) {
                    console.log('Error caught successfully:', error.message)
                }
            }
        }
        var target_clicked_button = button.dataset.bsTarget;
        var toggle_clicked_button = new bootstrap.Collapse(document.querySelector(target_clicked_button), {
            toggle: true
        })
        toggle_clicked_button.show();
        // save to the localStorage the state of the button being clicked
        localStorage.setItem("button-state-" + buttonID, "open");

}