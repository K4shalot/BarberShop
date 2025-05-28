document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.querySelector('#id_date');
    const barberInput = document.querySelector('#id_barber');

    function updateAvailableTimes() {
        const selectedDate = dateInput.value;
        const selectedBarber = barberInput ? barberInput.value : '';
        
        if (!selectedDate) {
            return;
        }

        console.log(`Запит на доступні години для дати: ${selectedDate} та барбера: ${selectedBarber}`);

        fetch(`/booking/get-available-times/?date=${selectedDate}&barber=${selectedBarber}`)
            .then(response => response.json())
            .then(data => {
                console.log('Відповідь від сервера:', data);

                const timeContainer = document.querySelector('.time-select');
                timeContainer.innerHTML = `
                    <p class="time-title">Оберіть годину:</p>
                `;

                if (data.available_times && data.available_times.length > 0) {
                    data.available_times.forEach(time => {
                        const label = document.createElement('label');
                        label.classList.add('time-option');
                        
                        const input = document.createElement('input');
                        input.type = 'radio';
                        input.name = 'time';
                        input.value = time;

                        const span = document.createElement('span');
                        span.textContent = time;

                        label.appendChild(input);
                        label.appendChild(span);

                        timeContainer.appendChild(label);
                    });
                } else {
                    timeContainer.innerHTML += `<p>На цю дату всі години зайняті. Спробуйте іншу дату 🙁</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    dateInput.addEventListener('change', updateAvailableTimes);
    barberInput && barberInput.addEventListener('change', updateAvailableTimes);

    const initialDate = dateInput.value;
    if (initialDate) {
        updateAvailableTimes();
    }
});