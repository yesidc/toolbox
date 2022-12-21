const plan_collapse = document.getElementsByClassName('plan-collapse')
const all_plans = document.getElementsByClassName('all-plan-sidebar')
const plan_name_dom = document.getElementById('plan_name_dom')


function open_internal_link(internal_url) {
// Open internal links (specified in the json5 files)
    window.open(internal_url)

}

function slugify(str_slug){

    str_slug=str_slug.toLowerCase()
    str_slug=str_slug.trim()
    str_slug=str_slug.replace(/[^\w\s-]/g, '')
    str_slug=str_slug.replace(/[\s_-]+/g, '-')
    str_slug=str_slug.replace(/^-+|-+$/g, '');
    return str_slug;
}


function set_menu_color() {
    // set the color of EVERY  course plan shown on the side nav bar.
    for (i of all_plans) {
        i.style.backgroundColor = 'rgba(209, 242, 249, 0.9)'
    }
}


set_menu_color()

// sets the color of ACTIVE the nav bar plan  when the user accesses a different building block
try {
    document.getElementById('plan-side-bar-' + slugify(plan_name_dom.dataset.planName)).style.backgroundColor = '#e99f4c'
} catch (error) {

}


function set_plan_collapse_color() {
    for (p of plan_collapse) {
        p.style.backgroundColor = 'rgba(163,217,234,0.2)'
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
                        set_menu_color()
                        set_plan_collapse_color()

                        // sets the color of the ACTIVE plan's name on the sidebar
                        document.getElementById('plan-side-bar-' + slugify(response.plan_name_ajax)).style.backgroundColor = '#e99f4c'
                        // sets the color of the drop-down menu on the sidebar
                        document.getElementById(slugify(response.plan_name_ajax)).style.backgroundColor = '#ededd1'

                        for (const c_done of response.category_ready) {
                            //ticks off the (sidebar)checkbox if user has already selected at least one idea for any given category
                            document.getElementById(c_done + response.plan_id_response).checked = true
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
    const ask = confirm('Do you want to delete: ' + plan_name);
    if (ask) {
        document.location.href = "/delete_plan" + "/" + plan_id + "/"
        //document.location.href = "{% url 'delete_plan'%}"+ "/"+plan_id

    }
}



