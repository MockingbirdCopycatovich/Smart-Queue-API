async function loadSpecialists() {
    const response = await fetch("/api/v1/specialists");
    const specialists = await response.json();

    const list = document.getElementById("specialists-list");
    list.innerHTML = "";

    specialists.forEach(s => {
        const li = document.createElement("li");
        li.textContent = `${s.full_name} (${s.service_type})`;
        li.style.cursor = "pointer";
        li.onclick = () => loadSlots(s.id);
        list.appendChild(li);
    });
}

async function loadSlots(specialistId) {
    const response = await fetch(`/api/v1/slots?specialist_id=${specialistId}`);
    const slots = await response.json();

    const list = document.getElementById("slots-list");
    list.innerHTML = "";

    slots.forEach(slot => {
        const li = document.createElement("li");
        li.textContent =
            `${slot.start_time} – ${slot.end_time} | ${slot.status}`;
        list.appendChild(li);
    });
}

loadSpecialists();
