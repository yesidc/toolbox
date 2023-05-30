var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var course_titles = document.querySelectorAll('.course-name-sidebar');

function edit_plan_title(plan_id) {
    // when user clicks on the edit icon, the title becomes editable
    const update_title = document.getElementById('edit-title-' + plan_id);
    update_title.contentEditable = true;
    update_title.focus();

}

// handles the edit of the plan title
course_titles.forEach(function (course_title) {
    course_title.addEventListener('keydown', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            course_title.contentEditable = false;

            $.ajax(
                {
                    url: '/edit_plan_title/',
                    type: 'POST',
                    data: {
                        'planId':  course_title.getAttribute('data-object-id'),
                        'plan_name': course_title.textContent.trim(),
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function (response) {
                        // 'button-state-plan-side-bar-
                        var button_state = localStorage.getItem('button-state-plan-side-bar-'+ response.previous_name);
                        localStorage.setItem('button-state-plan-side-bar-'+ response.updated_name, button_state);
                        localStorage.removeItem('button-state-plan-side-bar-'+ response.previous_name);

                    },
                    error: function (xhr, status, error) {
                        console.log('Error: ' + error);
                    }
                });

        }
    })

})