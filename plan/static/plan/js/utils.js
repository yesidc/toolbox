// div that contains the categories names and the (nested) ideas for each category on the sidebar
const plan_collapse = document.getElementsByClassName('plan-collapse')
// anchor tag that contains the plan's name on the sidebar
const all_plans = document.getElementsByClassName('all-plan-sidebar')
const plan_name_dom = document.getElementById('plan_name_dom')
// delete button on the sidebar (for each plan)
const delete_plan_button = document.getElementsByClassName('delete-plan-button')

function open_internal_link(internal_url) {
// Open internal links (specified in the json5 files)
    window.open(internal_url)

}

function hide_delete_button() {
    // hide the delete button on the sidebar
    for (i of delete_plan_button) {
        i.style.visibility = 'hidden'
    }

}

function slugify(str_slug) {

    str_slug = str_slug.toLowerCase()
    str_slug = str_slug.trim()
    str_slug = str_slug.replace(/[^\w\s-]/g, '')
    str_slug = str_slug.replace(/[\s_-]+/g, '-')
    str_slug = str_slug.replace(/^-+|-+$/g, '');
    return str_slug;
}


function set_menu_color() {
    // set the color of EVERY  course plan shown on the side nav bar.
    for (i of all_plans) {
        i.style.backgroundColor = '#4D1FAF'
    }
}


set_menu_color()

// sets the color of the ACTIVE  nav bar plan  when the user accesses a different building block
try {
    document.getElementById('plan-side-bar-' + slugify(plan_name_dom.dataset.planName)).style.backgroundColor = '#4D1FAF'
} catch (error) {

}


function set_plan_collapse_color() {
    // set the background color of the building block/teaching tools container
    for (p of plan_collapse) {
        p.style.backgroundColor = '#4786FF3D'
    }
}


for (i of plan_collapse) {
    // triggered when the user clicks on the course/plan's name and categories/blocks are shown (human touch, teaching material etc. )
    i.addEventListener('show.bs.collapse', event => {
        // subsequently handled by django select_plan view


        $.ajax(
            {
                type: 'GET',
                url: '/select_plan/',
                data: {
                    plan_id: event.target.getAttribute('data-plan-id')
                },
                success: function (response) {
                    try {
                        $('#plan_name_dom').text(response.plan_name_ajax)
                        // plan's name color
                        // set_menu_color()
                        //set_plan_collapse_color()

                        // sets the color of the ACTIVE plan's name on the sidebar
                        document.getElementById('plan-side-bar-' + slugify(response.plan_name_ajax)).style.backgroundColor = '#4D1FAF'
                        // hide all delete buttons
                        hide_delete_button()
                        // make delete button visible
                        document.getElementById('delete-sidebar-' + slugify(response.plan_name_ajax)).style.visibility = 'visible'
                        // sets the color of the drop-down menu on the sidebar
                        document.getElementById(slugify(response.plan_name_ajax)).style.backgroundColor = '#4786FF3D'

                        for (const c_done of response.category_ready) {
                            //shows (sidebar)check icon if user has already selected at least one idea for any given category

                            document.getElementById(c_done[0] + response.plan_id_response).style.visibility = 'visible'
                            const idea_container = document.getElementById('idea-' + c_done[0] + response.plan_id_response)
                            idea_container.innerHTML = ''
                            for (const idea of c_done[1]) {
                                var idea_paragraph = document.createElement('p')
                                idea_paragraph.textContent = idea
                                idea_paragraph.classList.add('p-teaching-tool-sidebar')
                                // add idea to idea_container
                                idea_container.appendChild(idea_paragraph)


                            }
                        }

                        // when the user selects a plan (using the left-navigation bar); the checkboxes on the block_content page are updated accordingly/dynamically

                        let idea_container = document.getElementById('online-idea-container')
                        if (idea_container !== null) {

                            let request_new_template = new XMLHttpRequest();
                            request_new_template.open('GET', window.location.pathname + '?mode=update');
                            request_new_template.onload = function () {
                                // the response is the rendered HTML

                                let myHTML = request_new_template.response;

                                // templated HTML returned by the server (managed by update_selected_idea view.)
                                idea_container.innerHTML = myHTML;

                            };
                            request_new_template.send();
                        }


                    } catch (error) {
                        console.log('Error caught successfully:', error.message)
                    }


                }

            }
        )

    })


}


function delete_plan(obj) {
    let plan_name = obj.getAttribute('data-object-name');
    let plan_id = obj.getAttribute('data-object-id');
    localStorage.removeItem('button-state-plan-side-bar-' + slugify(plan_name))
    console.log('deleted from localstorage', 'plan-side-bar-' + slugify(plan_name))
    const ask = confirm('Do you want to delete: ' + plan_name);
    if (ask) {
        document.location.href = "/delete_plan" + "/" + plan_id + "/"
        //document.location.href = "{% url 'delete_plan'%}"+ "/"+plan_id

    }
}



