// handles the edit note functionality from the checklist page
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let width;

function autoResize(text_are_id) {
    // textarea auto resizes when user is editing the note
  var textarea = document.getElementById(text_are_id);
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}


document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.text-area-note').forEach(
        (element) => {
        element.value = element.textContent.trim()
        }
    )
});


function cancelEdit(pcoi_instance_id, pcoi_instance_note) {
    event.preventDefault(); // prevent form from submitting
    var save_note_button = document.getElementById('note-submit-'+pcoi_instance_id);
    var note_input = document.getElementById('note-input-'+pcoi_instance_id);
    var cancel_note_button = document.getElementById('note-cancel-'+pcoi_instance_id);
    save_note_button.classList.add('hidden');
    cancel_note_button.classList.add('hidden');

    note_input.value = pcoi_instance_note;

    note_input.classList.remove('editing');

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

