const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const course_titles = document.querySelectorAll('.course-name-sidebar');

function edit_plan_title(plan_id) {

    const update_title = document.getElementById('edit-title-' + plan_id);
    update_title.contentEditable = true;
    update_title.focus();

    // // Move the media file to the album
    // $.ajax(
    //     {
    //         url: '/edit_plan_title/',
    //         type: 'POST',
    //         data: {
    //             'planId': plan_id,
    //             'csrfmiddlewaretoken': csrfToken
    //         },
    //         success: function (response) {
    //             console.log('Response:', response)
    //             console.log('Note updated successfully!')
    //             // Redirect
    //             window.location.href = '/checklist/';
    //         },
    //         error: function (xhr, status, error) {
    //             console.log('Error: ' + error);
    //         }
    //     });

}

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
                        console.log('Response:', response)
                        console.log('Title updated !')

                    },
                    error: function (xhr, status, error) {
                        console.log('Error: ' + error);
                    }
                });

        }
    })

})