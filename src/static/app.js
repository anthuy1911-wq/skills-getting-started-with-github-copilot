document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;
        const participants = Array.isArray(details.participants) ? details.participants : [];
        const mapQuery = encodeURIComponent(details.address || name);
        const mapLink = `https://www.google.com/maps/search/?api=1&query=${mapQuery}`;
        const participantsList = participants.length
          ? `<ul class="participant-list">${participants
              .map((participant) => {
                const participantEmail = typeof participant === "object" && participant ? participant.email : participant;
                const participantDetails = typeof participant === "object" && participant
                  ? ` <span class="participant-meta">Class ${participant.student_class || "N/A"} • DOB ${participant.dob || "N/A"} • Interest ${participant.interest || "N/A"}</span>`
                  : "";

                return `
                  <li class="participant-row">
                    <div class="participant-info">
                      <span class="participant-email">${participantEmail}</span>
                      ${participantDetails}
                    </div>
                    <button type="button" class="participant-delete" data-activity="${name}" data-email="${participantEmail}" aria-label="Remove ${participantEmail} from ${name}">
                      🗑
                    </button>
                  </li>
                `;
              })
              .join("")}</ul>`
          : `<p class="no-participants">No participants yet.</p>`;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p class="address-line">
            <span class="location-icon" aria-hidden="true">📍</span>
            <strong>Address:</strong>
            <a href="${mapLink}" target="_blank" rel="noopener noreferrer">${details.address || "TBD"}</a>
          </p>
          <p><strong>Fee:</strong> $${details.fee ?? 0}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants">
            <h5>Participants</h5>
            ${participantsList}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });

      document.querySelectorAll(".participant-delete").forEach((button) => {
        button.addEventListener("click", async () => {
          const activityName = button.dataset.activity;
          const email = button.dataset.email;

          try {
            const response = await fetch(
              `/activities/${encodeURIComponent(activityName)}/participants?email=${encodeURIComponent(email)}`,
              { method: "DELETE" }
            );

            const result = await response.json();

            if (response.ok) {
              messageDiv.textContent = result.message;
              messageDiv.className = "success";
              await fetchActivities();
            } else {
              messageDiv.textContent = result.detail || "Failed to unregister participant.";
              messageDiv.className = "error";
            }

            messageDiv.classList.remove("hidden");
            setTimeout(() => messageDiv.classList.add("hidden"), 5000);
          } catch (error) {
            messageDiv.textContent = "Failed to unregister participant.";
            messageDiv.className = "error";
            messageDiv.classList.remove("hidden");
            console.error("Error unregistering participant:", error);
          }
        });
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const studentClass = document.getElementById("student-class").value;
    const dob = document.getElementById("dob").value;
    const interest = document.getElementById("interest").value;
    const activity = document.getElementById("activity").value;

    try {
      const params = new URLSearchParams({
        email,
        student_class: studentClass,
        dob,
        interest,
      });

      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?${params.toString()}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
