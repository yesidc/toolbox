// handles the edit note functionality from the checklist page
let noteForm;
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let noteParagraph;
let noteInput;
let pcoiId;
let width;


document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.text-area-note').forEach(
        (element) => {
        element.value = element.textContent.trim()
        }
    )
//     document.querySelectorAll('.edit-note-checklist').forEach((element) => {
//     element.addEventListener('blur', () => {
//         console.log('blur triggered');
//         document.querySelectorAll('.save-note-button').forEach((element) => {
//             element.style.display = 'none';
//         });
//     });
// });
});


function cancelEdit(pcoi_instance_id, pcoi_instance_note) {
    event.preventDefault(); // prevent form from submitting
    var save_note_button = document.getElementById('note-submit-'+pcoi_instance_id);
    var note_input = document.getElementById('note-input-'+pcoi_instance_id);
    var cancel_note_button = document.getElementById('note-cancel-'+pcoi_instance_id);
    save_note_button.classList.add('hidden');
    cancel_note_button.classList.add('hidden');
    // console.log('note_input.value:', note_input.value);
    // console.log('note_input.textContent:', note_input.textContent);
    note_input.value = pcoi_instance_note;

    note_input.classList.remove('editing');
    // note_input.removeEventListener('blur', () => {
    //         note_input.classList.remove('editing');
    //     });
}

function editNote(pcoi_instance_id) {
  var save_note_button = document.getElementById('note-submit-'+pcoi_instance_id);
  var note_input = document.getElementById('note-input-'+pcoi_instance_id);
  var cancel_note_button = document.getElementById('note-cancel-'+pcoi_instance_id);
  save_note_button.classList.remove('hidden');
  cancel_note_button.classList.remove('hidden');

  note_input.classList.add('editing');
  note_input.addEventListener('blur', () => {
            note_input.classList.remove('editing');


        });
}

// let save_note_button = document.querySelectorAll('.save-note-button');
// document.querySelectorAll('.text-area-note').forEach((element) => {
//     element.addEventListener('click', () => {
//
//         element.addEventListener('blur', () => {
//             element.classList.remove('editing');
//
//             save_note_button.forEach(function (element) {
//                 element.style.display = 'block';
//             });
//         });
//     });
// });


function adjustWidth() {
    var screenWidth = window.innerWidth;
    var elements = document.querySelectorAll('.text-area-note');

    if (screenWidth >= 768) { // medium screen size
        elements.forEach(function (element) {
            element.style.width = '500px';
        });
    } else { // small screen size
        elements.forEach(function (element) {
            element.style.width = '200px';
        });
    }
}

window.addEventListener('resize', adjustWidth);

function saveNote(pcoi_instance_id) {

    console.log('Saving note...')
    const updatedNote = document.getElementById('note-input-'+pcoi_instance_id).value.trim();

    console.log('Updated note:', updatedNote);

        // Move the media file to the album
        $.ajax(
            {
                url: '/update_note_checklist/',
                type: 'POST',
                data: {
                    'note': updatedNote,
                    'pcoiId': pcoi_instance_id,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function (response) {
                    console.log('Response:', response)
                    console.log('Note updated successfully!')
                    // Redirect
                    window.location.href = '/checklist/';
                },
                error: function (xhr, status, error) {
                    console.log('Error: ' + error);
                }
            });

    }

// const elements = document.querySelectorAll('.text-area-note');
// for (let i = 0; i < elements.length; i++) {
//   elements[i].style.width = '300px';
//   // do something with the element
// }
//
//   window.addEventListener('resize', function() {
//     width = 0
//   var myElement = document.getElementsByClassName('row-note')[0];
//   width = myElement.offsetWidth;
//   for (let i = 0; i < elements.length; i++) {
//   elements[i].style.width = width.toString() + 'px';
//   // do something with the element
// }
//   console.log('Element width:', width);
// });


//
//
//
//
//
//
// function editNote(pcoi_instance_id) {
//     noteParagraph = document.getElementById('pcoi-note-id-' + pcoi_instance_id);
//     noteInput = document.getElementById('note-input-' + pcoi_instance_id);
//     noteForm = document.getElementById('note-form-' + pcoi_instance_id );
//     pcoiId = pcoi_instance_id;
//     noteInput.addEventListener('blur', saveNote);
//     noteInput.addEventListener('keydown', handleEnter);
//    console.log(width)
//     noteInput.style.width = width + 'px';
//      noteInput.setAttribute('rows', 5)
//     noteParagraph.style.display = 'none';
//     noteInput.style.display = '';
//     noteInput.value = noteParagraph.textContent;
//     noteInput.focus();
//     noteInput.select();
// }
//


    // }
    // else {
//         noteParagraph.style.display = '';
//         noteInput.style.display = 'none';
//
//     }
//
//
// }
//   function handleEnter(event) {
//         if (event.keyCode === 13) {
//             event.preventDefault();
//             // noteForm.submit();
//             saveNote();
//         }
//     }