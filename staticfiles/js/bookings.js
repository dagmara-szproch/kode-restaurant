document.addEventListener("DOMContentLoaded", function() {
  const editForm = document.getElementById("editForm");
  const peopleField = document.getElementById("id_number_of_people");
  const editButtons = document.querySelectorAll(".btn-edit");

  const closeButton = document.getElementById("closeButton");

  const cancelModal = new bootstrap.Modal(document.getElementById("cancelModal"));
  const cancelButtons = document.getElementsByClassName("btn-cancel");
  const cancelConfirm = document.getElementById("confirmCancel");

  /*
   * Initializes edit functionality for the provided edit buttons.
   * *
   * For each button in the `editButtons` collection:
   * - Retrives the associated booking's ID upon click.
   * - Fetches the current number of people for that booking.
   * - Populates the `peopleField` select input with the current number.
   * - Sets the `editForm` action attribute to `/booking/edit-booking/{bookingID}`.
   * - Displays the hidden edit form.
   * - Scrolls smoothly to the edit form for better user experience.
   */

  editButtons.forEach(button => {
    button.addEventListener("click", () => {
      const bookingId = button.dataset.id;
      const currentPeople = document.getElementById(`people${bookingId}`).innerText;

      peopleField.value = currentPeople;
      editForm.action = `/booking/edit-booking/${bookingId}/`;
      editForm.style.display = "block";

      // Scroll to form for better UX
      editForm.scrollIntoView({ behavior: "smooth" });
    });
  });

  /*
   * Initializes cancellation functionality using a Bootstrap modal for the provided cancel buttons
   * *
   * For each button in the `cancelButtons` collection:
   * - Retrives the associated booking's ID upon click.
   * - Stores the booking ID in a temporary variable.
   * - Updates the `confirmCancel` button's href.
   * - Shows the Bootstrap confirmation modal.
   * 
   * When the "Yes,Cancel" button is clicked:
   * - Checks if a booking ID is stored.
   * Redirects the user to `/booking/cancel-booking/{bookingID}` to performthe cancellation.
   */

  for (let button of cancelButtons) {
    button.addEventListener("click", (e) => {
      const bookingId = e.target.getAttribute("data-id");
      cancelConfirm.addEventListener("click", () => {
        window.location.href = `/booking/cancel-booking/${bookingId}`;
      }, { once: true });
      cancelModal.show();
    });
  }
  
  /* 
   * Handles the close button of the edit form.
   *
   * - When the `closeButton` is clicked:
   * - Hides the `editForm` by setting its display to 'none'.
   */
  closeButton.addEventListener('click', () => {
    editForm.style.display = 'none';
  });
});
