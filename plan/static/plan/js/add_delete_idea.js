function add_delete_idea() {


    if (event.currentTarget.checked) {
           var message_idea_added = '     <div class="alert alert-info alert-dismissible fade show" role="alert">\n' +
            '                                <button type="button" class="close" data-bs-dismiss="alert" aria-hidden="true">&times;\n' +
            '                                </button>\n' +
            '                                Idea succesfully added to your plan\n' +
            '\n' +
            '                            </div>'
        $('.messages-js').append(message_idea_added)
        // request managed by use_idea view, that subsequently adds idea to the course plan.


        $.ajax(
            {
                type: 'GET',
                //url: i.id + '/save_idea/'
                url: '/use_idea/',
                data: {
                    idea_id: (event.target.id).split('-')[0], //Online Idea id.
                    plan_name_dom: document.getElementById('plan_name_dom').innerText

                },
                success: function (response) {
                    id_ = response.category_id + response.plan_id
                    document.getElementById(id_).checked = true;

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
        $('.messages-js').append(message_delete)
        //alert('Idea deleted');
        // Delete idea from the course plan (PlanCategoryOnlineIdea Object)
        $.ajax(
            {
                type: 'GET',
                url: '/use_idea/',
                data: {
                    idea_id: (event.target.id).split('-')[0],     //Online Idea id.
                    delete_idea: true,
                    plan_name_dom: document.getElementById('plan_name_dom').innerText
                },
                success: function (response) {


                    let category_ready = []
                    // creates an array that contains the id for each of the (sidebar) category checkboxes that belong to plan
                    response.category_ready.forEach(function (c){
                        category_ready.push(c+response.plan_id)
                    })
                    // if the checkbox' id is in the category_ready array; the checkbox is checked (it means the user has chosen at least one idea for that specific category).
                    // otherwise, checkbox is unchecked
                    $('.'+ response.plan_id+'block').each(function (i, obj) {

                        obj.checked = category_ready.includes(obj.id);

                    });

                }
            }
        )
    }


}

function add_delete_idea_checklist(btn_id){
    // deletes the idea, note and delete button from the checklist page
    $('.'+ btn_id).remove()

}