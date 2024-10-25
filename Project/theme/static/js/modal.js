

document.addEventListener('DOMContentLoaded', function() {
    const openModalBtns = document.querySelectorAll('.openModalBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const addModal = document.getElementById('addModal');
    const companyFields = document.getElementById('companyFields');
    let currentField = '';

    function abrirModal(campo) {
        currentField = campo;
        addModal.classList.remove('hidden');
        if (currentField === 'company') {
            companyFields.classList.remove('hidden');
        } else {
            companyFields.classList.add('hidden');
        }
    }

    function cerrarModal() {
        addModal.classList.add('hidden');
        document.getElementById('newItemInput').value = '';
        document.getElementById('companyImage').value = '';
    }

    openModalBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const campo = e.target.dataset.field;
            abrirModal(campo);
        });
    });

    closeModalBtn.addEventListener('click', cerrarModal);

    document.getElementById('miFormulario').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        formData.append('field', currentField);

        fetch(`/add_${currentField}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success) {
                const select = document.querySelector(`select[name="${currentField}"]`);
                const option = new Option(data.description, data.id);
                select.add(option);
                select.value = data.id;

                document.getElementById('newItemInput').value = '';
                document.getElementById('companyImage').value = '';
                cerrarModal();
            } else {
                console.error('Error:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
