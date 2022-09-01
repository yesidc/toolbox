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
                    url: '/save_idea/',
                    data: {
                        idea_name: event.target.id, //Online Idea id.
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
                    url: '/save_idea/',
                      data: {
                        idea_name: event.target.id,     //Online Idea id.
                        delete_idea: true,
                          plan_name_dom: document.getElementById('plan_name_dom').innerText
                    }
                }
            )
        }


    })

}

// closes the messages
$('.alert').alert()