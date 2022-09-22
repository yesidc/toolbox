const plan_collapse = document.getElementsByClassName('plan-collapse')
for (i of plan_collapse) {
    // triggered when the user clicks on the course/plan's name and categories/blocks are shown (human touch, teaching material etc. )
    i.addEventListener('show.bs.collapse', event => {
        // subsequently handled by django select_plan view
        console.log('first child')
        console.log(event.target.children[0].id)
        $.ajax(
            {
                type: 'GET',
                url: '/select_plan/',
                data: {
                    plan_id: event.target.children[0].id// this id refers to id assigned to the FIRST child node of the  html element that triggers this event, which is the plan's pk
                },
                success: function (response) {

                    $('#plan_name_dom').text(response.plan_name_ajax)


                    for (const c_done of response.category_ready){
                        //ticks off the (sidebar)checkbox if user has already selected at least one idea for any given category
                        document.getElementById(c_done+response.plan_id_response ).checked = true
                    }

                    // when the user selects a plan (using the left-navigation bar); the checkboxes on the block_content page are updated accordingly/dynamically
                    if (document.getElementById('online-idea-container')!== null) {
                        let request_new_template = new XMLHttpRequest();
                        request_new_template.open('GET', '/update_selected_idea/');
                        request_new_template.onload = function () {
                            // the response is the rendered HTML

                            let myHTML = request_new_template.response;

                            // templated HTML returned by the server (managed by update_selected_idea view.)
                            document.getElementById('online-idea-container').innerHTML = myHTML;

                        };
                        request_new_template.send();
                    }



                }

            }
        )

    })
}


// closes the messages
$('.alert').alert()