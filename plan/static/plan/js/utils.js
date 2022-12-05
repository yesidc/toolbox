const plan_collapse = document.getElementsByClassName('plan-collapse')
const all_plans = document.getElementsByClassName('all-plan-sidebar')
const plan_name_dom = document.getElementById('plan_name_dom')



function open_internal_link(internal_url){

    //var link_internal = window.location.host + internal_url
    window.open(internal_url)

}



if(plan_name_dom){

    document.getElementById('plan-side-bar-'+add_hyphen(plan_name_dom.dataset.planName)).style.backgroundColor='#e6e6ff'
}




function add_hyphen(plan){
    return plan.replaceAll(' ', '-');
}

function set_plan_collapse_color (){
    for(p of plan_collapse){
        p.style.backgroundColor='white'
    }
}

function set_menu_color(){
    for (i of all_plans){
        i.style.backgroundColor='white'
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

                    $('#plan_name_dom').text(response.plan_name_ajax)
                    // plan's name color
                    set_menu_color()
                    set_plan_collapse_color()

                    // sets the color of the plan's name on the sidebar
                    document.getElementById('plan-side-bar-'+add_hyphen(response.plan_name_ajax)).style.backgroundColor='#e6e6ff'
                    // sets the color of the drop-down menu on the sidebar
                    document.getElementById(add_hyphen(response.plan_name_ajax)).style.backgroundColor='#e6e6ff'

                    for (const c_done of response.category_ready){
                        //ticks off the (sidebar)checkbox if user has already selected at least one idea for any given category
                        document.getElementById(c_done+response.plan_id_response ).checked = true
                    }

                    // when the user selects a plan (using the left-navigation bar); the checkboxes on the block_content page are updated accordingly/dynamically
                    if (document.getElementById('online-idea-container')!== null) {
                        let request_new_template = new XMLHttpRequest();
                        request_new_template.open('GET', window.location.pathname+'?mode=update');
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


function delete_plan(obj) {
    let plan_name = obj.getAttribute('data-object-name');
    let plan_id = obj.getAttribute('data-object-id');
    const ask = confirm('Do you want to delete: ' + plan_name);
    if (ask){
        document.location.href = "/delete_plan"+ "/"+plan_id+"/"
        //document.location.href = "{% url 'delete_plan'%}"+ "/"+plan_id

    }
}


// closes the messages
// $('.alert').alert()


