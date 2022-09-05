// user can delete/add an idea to her plan by ticking off the checkbox found on the idea overview page.
const idea_checkbox = document.getElementsByClassName('idea-checkbox')


// get requests sent are handle by use_idea view
for (i of idea_checkbox) {
    i.addEventListener('change', (event) => {

        if (event.currentTarget.checked) {
            alert('Online Idea Added to your course plan');
            // request managed by use_idea view, that subsequently adds idea to the course plan.


            $.ajax(
                {
                    type: 'GET',
                    //url: i.id + '/save_idea/'
                    url: '/use_idea/',
                    data: {
                        idea_id: event.target.id, //Online Idea id.
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
                        idea_id: event.target.id,     //Online Idea id.
                        delete_id: true,
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
for (i of plan_collapse){
    // triggered when the user clicks on the course/plan's name and categories/blocks are shown (human touch, teaching material etc. )
    i.addEventListener('show.bs.collapse', event => {
     // subsequently handled by django select_plan view
    $.ajax(
        {
            type:'GET',
            url:'/select_plan/',
            data:{
                plan_name: event.target.id// this id refers to id assigned to the html element, which is the plan's pk
            },
            success: function (response){
                $('#plan_name_dom').text(response.plan_name_ajax)
            }

        }
    )
})
}



// closes the messages
$('.alert').alert()