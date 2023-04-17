let noteForm;
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let noteParagraph;
let noteInput;
let pcoiId;


function editNote(pcoi_instance_id) {
    noteParagraph = document.getElementById('pcoi-note-id-' + pcoi_instance_id);
    noteInput = document.getElementById('note-input-' + pcoi_instance_id);
    noteForm = document.getElementById('note-form-' + pcoi_instance_id );
    pcoiId = pcoi_instance_id;
    // document.getElementById('plan-id-input').value = planId;
    noteInput.addEventListener('blur', saveNote);
    noteInput.addEventListener('keydown', handleEnter);
    noteParagraph.style.display = 'none';
    noteInput.style.display = '';
    noteInput.value = noteParagraph.textContent;
    noteInput.focus();
    noteInput.select();
}

function saveNote() {
    const updatedNote = noteInput.value.trim();

    if (updatedNote !== noteParagraph.textContent) {
        fetch(`/update_note_checklist/${pcoiId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: `pcoi_id=${pcoiId}&note=${encodeURIComponent(updatedNote)}`,
        })
            .then(response => {
                if (response.ok) {
                    console.log('Note updated successfully!')
                    noteParagraph.textContent = updatedNote;
                    noteParagraph.style.display = '';
                    noteInput.style.display = 'none';
                    // Redirect to checklist
                    window.location.href = '/checklist/';

                }
            });
    } else {
        noteParagraph.style.display = '';
        noteInput.style.display = 'none';

    }


}
  function handleEnter(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            noteForm.submit();
        }
    }