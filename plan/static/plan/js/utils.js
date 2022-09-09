// user can delete/add an idea to her plan by ticking off the checkbox found on the idea overview page.
const idea_checkbox = document.getElementsByClassName('idea-checkbox')


// get requests sent are handle by use_idea view
for (i of idea_checkbox) {
    i.addEventListener('click', (event) => {

        if (event.currentTarget.checked) {
            alert('Online Idea Added to your course plan');
            // request managed by use_idea view, that subsequently adds idea to the course plan.


            $.ajax(
                {
                    type: 'GET',
                    //url: i.id + '/save_idea/'
                    url: '/use_idea/',
                    data: {
                        idea_id: (event.target.id ).split('-')[0], //Online Idea id.
                        plan_name_dom: document.getElementById('plan_name_dom').innerText

                    }
                }
            )

        } else {
            alert('not checked');
            // Delete idea from the course plan (PlanCategoryOnlineIdea Object)
            $.ajax(
                {
                    type: 'GET',
                    url: '/use_idea/',
                    data: {
                        idea_id: (event.target.id ).split('-')[0],     //Online Idea id.
                        delete_idea: true,
                        plan_name_dom: document.getElementById('plan_name_dom').innerText
                    }
                }
            )
        }


    })

}

// Triggered when user saves idea to a plan/course using button on the overview_page
// if (window.location.pathname == '/') {
//     $("#save_idea_overview").click(function () {
//         alert('clicked')
//         $.ajax(
//             {
//                 type: 'GET',
//                 url: '/use_idea/',
//                 data: {
//                     plan_name_dom: document.getElementById('plan_name_dom').innerText
//                 }
//             }
//         )
//     })
// }

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
                    // location.reload()
                    $('#plan_name_dom').text(response.plan_name_ajax)


                    for (const c_done of response.category_ready){
                        console.log(c_done)
                        console.log(response.plan_id_response)
                        document.getElementById(c_done+response.plan_id_response ).checked = true
                    }
                    // $.ajax(
                    //     {type: 'GET',
                    //         url: '/' + response.current_category_url + '/'
                    //     }
                    //
                    // )

                    let request_new_template = new XMLHttpRequest();
                    request_new_template.open('GET', '/update_selected_idea/');
                    request_new_template.onload = function () {
                        // the response is the rendered HTML
                        // which django sends as return render(response, "your_template.html", context)
                        let myHTML = request_new_template.response;
                        // This is the important part
                        // Set that HTML to the new, templated HTML returned by the server
                        document.getElementById('online-idea-container').innerHTML = myHTML;
                    };
                    request_new_template.send();

                }

            }
        )
    })
}


// closes the messages
$('.alert').alert()