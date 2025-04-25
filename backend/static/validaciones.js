// Elementos del formulario
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const telefono = document.getElementById("telefono");
const fechaNacimiento = document.getElementById("fechaNacimiento");
const form = document.getElementById("registroForm");

// Función para resaltar el campo en rojo si hay error
function resaltarCampo(input, msg, esValido) {
  input.classList.toggle("input-error", !esValido);
  msg.style.display = esValido ? "none" : "block";
}

// Validación del nombre de usuario
username.addEventListener("input", () => {
  const msg = document.getElementById("errorUsername");
  const esValido = username.value.length >= 3;
  msg.textContent = esValido ? "" : "Debe tener al menos 3 caracteres.";
  resaltarCampo(username, msg, esValido);
});

// Validación del correo
email.addEventListener("input", () => {
  const msg = document.getElementById("errorEmail");
  const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const esValido = valid.test(email.value);
  msg.textContent = esValido ? "" : "Correo inválido.";
  resaltarCampo(email, msg, esValido);
});

// Validación de la contraseña
password.addEventListener("input", () => {
  const msg = document.getElementById("errorPassword");
  const valid = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
  const esValido = valid.test(password.value);
  msg.textContent = esValido ? "" : "Mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número y 1 especial.";
  resaltarCampo(password, msg, esValido);
});

// Validación del número de teléfono
telefono.addEventListener("input", () => {
  const msg = document.getElementById("errorTelefono");
  const valid = /^(809|829|849)[-. ]?\d{3}[-. ]?\d{4}$|^\(?(809|829|849)\)?[-. ]?\d{3}[-. ]?\d{4}$/;
  const esValido = valid.test(telefono.value);
  msg.textContent = esValido ? "" : "Número inválido. Formatos aceptados: 809-000-0000, (809) 000-0000, etc.";
  resaltarCampo(telefono, msg, esValido);
});

// Validación de edad mínima
fechaNacimiento.addEventListener("input", () => {
  const msg = document.getElementById("errorFecha");
  const hoy = new Date();
  const nac = new Date(fechaNacimiento.value);
  let edad = hoy.getFullYear() - nac.getFullYear();
  const m = hoy.getMonth() - nac.getMonth();
  if (m < 0 || (m === 0 && hoy.getDate() < nac.getDate())) edad--;

  const esValido = edad >= 18;
  msg.textContent = esValido ? "" : "Debes ser mayor de 18 años.";
  resaltarCampo(fechaNacimiento, msg, esValido);
});

// Validar al enviar y enviar al servidor
form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const errores = [...document.querySelectorAll(".error")];
  const hayErrores = errores.some(span => span.textContent !== "");
  const campos = [username, email, password, telefono, fechaNacimiento];
  const camposVacios = campos.some(campo => campo.value.trim() === "");

  if (hayErrores || camposVacios) {
    alert("Completa todos los campos y corrige los errores antes de enviar.");
    return;
  }

  // Enviar al backend
  const datos = {
    username: username.value,
    email: email.value,
    password: password.value,
    telefono: telefono.value.replace(/\D/g, ""), // eliminar guiones, paréntesis
    fechaNacimiento: fechaNacimiento.value
  };

  try {
    const response = await fetch("http://localhost:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    if (resultado.success) {
      alert("¡Registro exitoso!");
      form.reset(); // Resetear formulario después de un registro exitoso
    } else {
      alert("Error: " + resultado.message);
    }
  } catch (error) {
    alert("Error al conectar con el servidor.");
    console.error(error);
  }
});