document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault(); // prevenimos envío por defecto

  const errores = [...document.querySelectorAll(".error")];
  const hayErrores = errores.some(span => span.textContent !== "");

  // ✅ IDs corregidos aquí
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  if (hayErrores || username === "" || password === "") {
    alert("Completa los campos correctamente para iniciar sesión.");
    return;
  }

  // Deshabilitar el botón de inicio de sesión mientras se procesa la solicitud
  const loginButton = document.getElementById("loginButton");
  loginButton.disabled = true;

  document.getElementById("loading-screen").style.display = "flex";

  fetch("http://localhost:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  })
    .then(res => res.json())
    .then(data => {
      // Habilitar el botón nuevamente y ocultar el loading-screen
      loginButton.disabled = false;
      document.getElementById("loading-screen").style.display = "none";

      if (data.success) {
        localStorage.setItem("username", data.username);
        window.location.href = "dashboard.html"; // Redirigir al dashboard
      } else {
        alert(data.message || "Error al iniciar sesión.");
      }
    })
    .catch(err => {
      // Habilitar el botón nuevamente y ocultar el loading-screen
      loginButton.disabled = false;
      document.getElementById("loading-screen").style.display = "none";
      alert("Ocurrió un error al contactar al servidor.");
      console.error(err);
    });
});



