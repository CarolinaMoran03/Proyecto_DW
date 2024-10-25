function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Comprobar si esta cookie es la que buscamos
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken');

async function senData(event) {
    event.preventDefault();

    let inputDescription = document.querySelector("#newItemInput").value;

    try {
        const res = await fetch("/add-new-item/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  
            },
            body: JSON.stringify({ description: inputDescription })
        });

        if (!res.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await res.json();
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

document.getElementById("miFormulario").addEventListener("submit", senData);
