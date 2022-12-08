function add_delete_idea() {
/**
 * Triggered when user interacts with any checkbox on the block_content page.
 * Manages all functionality related to either adding or deleting ideas from the current plan/course
    */
    let id_ = null

    if (event.currentTarget.checked) {
           var message_idea_added = '     <div class="alert alert-info alert-dismissible fade show" role="alert">\n' +
            '                                <button type="button" class="close" data-bs-dismiss="alert" aria-hidden="true">&times;\n' +
            '                                </button>\n' +
            '                                Idea successfully added to your plan\n' +
            '\n' +
            '                            </div>'


        // request managed by use_idea view, that subsequently adds idea to the course plan.


        $.ajax(
            {
                type: 'GET',
                url: '/use_idea/',
                data: {
                    idea_id: (event.target.id).split('-')[0], //Online Idea id.
                    current_category: document.getElementById('category-url-save-idea').dataset.categoryUrl,
                    plan_name_dom: document.getElementById('plan_name_dom').innerText


                },
                success: function (response) {


                    try {
                        id_ = response.category_id + response.plan_id

                        // if there is no plan id, ask user to create or select a plan.
                        if (document.getElementById(id_) == null) {
                            alert('First create a plan to be able to save your progress.')
                        } else {
                            document.getElementById(id_).checked = true;
                            $('.messages-js').append(message_idea_added)
                        }
                    } catch (e) {
                        console.log('Error caught successfully: ', e.message)
                    }




                }
            }
        )

    } else {

        var message_delete = '     <div class="alert alert-info alert-dismissible fade show" role="alert">\n' +
            '                                <button type="button" class="close" data-bs-dismiss="alert" aria-hidden="true">&times;\n' +
            '                                </button>\n' +
            '                                Idea succesfully deleted\n' +
            '\n' +
            '                            </div>'


        // Delete idea from the course plan (PlanCategoryOnlineIdea Object)
        $.ajax(
            {
                type: 'GET',
                url: '/use_idea/',
                data: {
                    idea_id: (event.target.id).split('-')[0],     //Online Idea id.
                    delete_idea: true,
                     current_category: document.getElementById('category-url-save-idea').dataset.categoryUrl,
                    plan_name_dom: document.getElementById('plan_name_dom').innerText

                },
                success: function (response) {


                    try {
                        id_ = response.category_id + response.plan_id

                        // if there is no plan id, ask user to create or select a plan.
                        if (document.getElementById(id_) !== null) {
                            $('.messages-js').append(message_delete)
                            let category_ready = []
                            // creates an array that contains the id for each of the (sidebar) category checkboxes that belong to plan
                            response.category_ready.forEach(function (c) {
                                category_ready.push(c + response.plan_id)
                            })
                            // if the checkbox' id is in the category_ready array; the checkbox is checked (it means the user has chosen at least one idea for that specific category).
                            // otherwise, checkbox is unchecked
                            $('.' + response.plan_id + 'block').each(function (i, obj) {

                                obj.checked = category_ready.includes(obj.id);

                            });
                        }
                    } catch (e) {
                        console.log('Error caught successfully: ', e.message)
                    }





                }
            }
        )
    }


}

function add_delete_idea_checklist(btn_id){
/**
 * When user deletes an idea using any of the delete buttons checklist page: request is subsequently handle by delete_pcoi_checklist django view. Upon success; the idea, note and associated delete button are deleted from DOM. (Note is kept in database)
 * @param btn_id {string} Contains the id of the pcoi instance to be deleted

*/
    $.ajax(
        {
            type: 'GET',
            url:'/delete_pcoi_checklist/',
            data: {
                pcoi_id: btn_id.split('-')[2], //PlanCategoryOnlineIdea instance id. This instance will be deleted from the database

            },
            success:function (response){
                 $('.'+ btn_id).remove()     // deletes the idea, note and delete button from the checklist page
            }
        }
    )

}