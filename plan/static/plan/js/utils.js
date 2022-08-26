// user can delete/add an idea to her plan by ticking off the checkbox
const idea_checkbox = document.getElementsByClassName('idea-checkbox')


// get requests sent are handle by use_idea view
for (i of idea_checkbox) {
    i.addEventListener('change', (event) => {

        if (event.currentTarget.checked) {
            alert('checked');
            // request managed by use_idea view.


            $.ajax(
                {
                    type: 'GET',
                    //url: i.id + '/save_idea/'
                    url: '/save_idea/',
                    data: {
                        idea_id: event.target.id //Online Idea id.
                    }
                }
            )

        } else {
            alert('not checked');
        }


    })

}