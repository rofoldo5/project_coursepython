
document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById("client-form");
    if(form) {
        form.addEventListener('summit', (event) => {
            event.preventDefault();
            var cedula = document.getElementById('dni').value;
            console.log('DNI', cedula);
        })
    } else {
        console.error('Error: El formulario con ID "client-from" no fue encontrado en el DOM');
    }
})