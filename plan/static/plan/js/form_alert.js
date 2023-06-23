// This file is used to display a confirmation message when the user tries to leave the page without saving the form

  document.getElementById('notes-form').addEventListener('submit', function(event) {
    // Form is being submitted, no need to display the confirmation message
    window.removeEventListener('beforeunload', confirmExit);
  });

  window.addEventListener('beforeunload', confirmExit);

  function confirmExit(event) {
    if (document.getElementById('notes-form').elements.length > 0) {
      event.preventDefault();
      event.returnValue = ''; // For older browsers
      return ''; // For modern browsers
    }
  }