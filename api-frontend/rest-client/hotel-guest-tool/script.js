const API_URL = "https://vm2208.kaj.pouta.csc.fi:8323";

let API_KEY = localStorage.getItem('hotel_api_key');
if (!API_KEY) {
    API_KEY = prompt("Ge din api_key tack!");
    localStorage.setItem('hotel_api_key', API_KEY);
}

async function getBookings() {
    const resp = await fetch(`${API_URL}/bookings?api_key=${API_KEY}`);
    const bookings = await resp.json();

    document.querySelector('#guest-name').innerText = bookings[0].firstname;

    let bookingsHtml = "";
    for (b of bookings) {
        // Lägg till ett select-element för att välja antalet stjärnor för varje bokning
        bookingsHtml += `
            <li>${b.datefrom} Room: ${b.room_number} (${b.type}) 
                <select class="stars-select" data-booking-id="${b.id}">
                    <option value="1">1 star</option>
                    <option value="2">2 stars</option>
                    <option value="3">3 stars</option>
                    <option value="4">4 stars</option>
                    <option value="5">5 stars</option>
                </select>
            </li>`;
    }
    document.querySelector('#bookings').innerHTML = bookingsHtml;

    // Lägg till händelselyssnare för select-elementen för att skicka stjärnor när användaren väljer
    document.querySelectorAll('.stars-select').forEach(select => {
        select.addEventListener('change', async (event) => {
            const bookingId = event.target.dataset.bookingId;
            const stars = event.target.value;

            // Skicka stjärnorna med en PUT-förfrågan
            const resp = await fetch(`${API_URL}/bookings/${bookingId}?api_key=${API_KEY}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ stars: stars })
            });

            const respData = await resp.json();
            console.log(respData);
        });
    });
}

getBookings();

async function createBooking() {
    const booking = {
        room: document.querySelector('#room').value,
        datefrom: document.querySelector('#datefrom').value
    };

    const resp = await fetch(`${API_URL}/bookings?api_key=${API_KEY}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(booking)
    });

    const respData = await resp.json();
    getBookings();
    console.log(respData);
}

async function getRooms() {
    const resp = await fetch(`${API_URL}/rooms`);
    const rooms = await resp.json();

    let roomsHtml = "<option>-- Välj rum</option>";
    for (room of rooms) {
        roomsHtml += `<option value="${room.id}">${room.room_number}</option>`;
    }
    document.querySelector('#room').innerHTML = roomsHtml;
}

getRooms();
