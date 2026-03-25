const API_URL = "http://127.0.0.1:8000/peliculas/";

//obtiene y muestra la lista de peliculas
async function obtenerPeliculas() {
    const respuesta = await fetch(API_URL);
    const peliculas = await respuesta.json();
    const listaPeliculas = document.getElementById("lista-peliculas");
    listaPeliculas.innerHTML = "";

    peliculas.forEach(pelicula => {
        const li= document.createElement("li");
        li.textContent = `${pelicula.titulo} - ${pelicula.director} (${pelicula.anio})`;

        //boton para editar

        const btnEditar = document.createElement("button");
        btnEditar.textContent = "Editar";
        btnEditar.onclick = () => editarPelicula(pelicula);
        li.appendChild(btnEditar);
        //eliminar
        const btnEliminar = document.createElement("button");
        btnEliminar.textContent = "Eliminar";
        btnEliminar.onclick = () => eliminarPelicula(pelicula.id);
        li.appendChild(btnEliminar);

        listaPeliculas.appendChild(li);
    });
}
//agrega pelicula
async function agregarPelicula(event) {
    event.preventDefault();
    const titulo = document.getElementById("titulo").value;
    const director = document.getElementById("director").value;
    const anio = document.getElementById("anio").value
    const pelicula_id = document.getElementById("pelicula_id").value;
    
    const method = pelicula_id ? "PUT" : "POST"; //determina metodo, si agrego o modifico
    const url = pelicula_id ? API_URL + pelicula_id + "/" : API_URL;

    const respuesta = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body :JSON.stringify({titulo, director, anio})
    });

    if (respuesta.ok){
        obtenerPeliculas();
        limpiarFormulario();
    }
}

function editarPelicula(pelicula) {
    document.getElementById("titulo").value = pelicula.titulo;
    document.getElementById("director").value = pelicula.director;
    document.getElementById("anio").value = pelicula.anio;
    document.getElementById("pelicula_id").value = pelicula_id; // guarda la id
    document.querySelector("button[type='submit']").textContent = "Actualizar Pelicula";
}

async function eliminarPeliculas(pelicula_id) {
    const respuesta = await fetch(API_URL + pelicula_id + "/", {
        method: "DELETE"
    });

    if (respuesta.ok) {
        obtenerPeliculas();
    }
}
//limpiar le formulario 
function limpiarFormulario() {
    document.getElementById("titulo").value = "";
    document.getElementById("director").value = "";
    document.getElementById("anio").value = "";
    document.getElementById("pelicula_id").value = ""; // limpia la id
    document.querySelector("button[type='submit']").textContent = "Agregar Pelicula";
//vuelve al original 
}
//inicia
document.getElementById("formulario-pelicula").addEventListener("submit", agregarPelicula);
obtenerPeliculas(); 