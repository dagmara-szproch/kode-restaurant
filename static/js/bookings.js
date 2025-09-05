document.addEventListener("DOMContentLoaded", function() {
  const editForm = document.getElementById("editForm");
  const peopleField = document.getElementById("id_number_of_people");
  const editButtons = document.querySelectorAll(".btn-edit");
  const cancelButtons = document.querySelectorAll(".btn-cancel");

  // Handle Edit button
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

  // Handle Cancel button
  cancelButtons.forEach(button => {
    button.addEventListener("click", () => {
      const bookingId = button.dataset.id;
      if (confirm("Are you sure you want to cancel this booking?")) {
        window.location.href = `/booking/cancel-booking/${bookingId}/`;
      }
    });
  });
});