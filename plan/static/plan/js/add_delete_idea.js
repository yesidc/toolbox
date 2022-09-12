function add_delete_idea() {


    if (event.currentTarget.checked) {
        alert('Online Idea Added to your course plan');
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
        alert('Idea deleted');
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
                    //iterate through all checkboxes in a (sidebar )building block
                    // const checkbox = document.getElementsByClassName( response.plan_id+'block')
                    //  for (i of checkbox){
                    //      // you are not accesing the right element. this is not the chekcbox this is the p tag.
                    //      i.checked=false;
                    //  }

                    let category_ready = []
                    response.category_ready.forEach(function (c){
                        category_ready.push(c+response.plan_id)
                    })
                    $('.'+ response.plan_id+'block').each(function (i, obj) {

                        if (category_ready.includes(obj.id)){
                              obj.checked=true
                        }
                        else {
                            obj.checked=false
                        }

                    });

                }
            }
        )
    }


}