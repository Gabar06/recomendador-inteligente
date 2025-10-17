/*
 * Script de ejercicios de acentuación (e1, e2 y e3).
 *
 * Este archivo intercepta el envío del formulario y muestra la
 * retroalimentación en línea, deshabilitando las opciones para
 * evitar cambios posteriores.  También permite solicitar una
 * explicación adicional mediante un endpoint dedicado.  Mientras se
 * obtiene la explicación se muestra una animación de carga y, una
 * vez disponible, se resaltan palabras clave en negrita.
 */



// CSRF helper para obtener el token desde las cookies
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

// Guardia anti-retroceso
(function installLeaveGuard() {
  const RESTART_URL = "/acento_1/reiniciar/";
  window.__allowLeave = false;

  history.pushState(null, "", location.href);

  window.addEventListener("popstate", function () {
    if (window.__allowLeave) return;
    const msg = "Si salís ahora, perdés tu progreso de esta unidad. ¿Salir de todos modos?";
    if (confirm(msg)) {
      window.__allowLeave = true;
      location.href = RESTART_URL;
    } else {
      history.pushState(null, "", location.href);
    }
  });

  window.addEventListener("beforeunload", function (e) {
    if (window.__allowLeave) return;
    e.preventDefault();
    e.returnValue = "";
  });

  document.addEventListener("click", function (ev) {
    const a = ev.target.closest("a");
    if (a && a.dataset.allowLeave === "1") {
      window.__allowLeave = true;
    }
  });
})();

// Resalta palabras clave en la explicación con <strong>
function highlightImportantWords(text) {
  if (!text) return '';
  const keywords = ['correcta', 'correcto', 'incorrecta', 'incorrecto', 'regla', 'palabra', 'opción', 'respuesta'];
  let result = text;
  keywords.forEach((kw) => {
    const regex = new RegExp(`\\b${kw}\\b`, 'gi');
    result = result.replace(regex, (match) => `<strong>${match}</strong>`);
  });
  return result;
}

// Configura el manejo de envío para un formulario de ejercicio de acentuación
function wireForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;
  const feedbackBox = form.parentElement.querySelector('.feedback-box') || document.getElementById('feedback-box');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitUrl = form.dataset.submitUrl;
    const csrftoken = getCookie('csrftoken');
    const formData = new FormData(form);
    // Mostrar mensaje de procesamiento
    if (feedbackBox) feedbackBox.innerHTML = 'Procesando…';
    try {
      const response = await fetch(submitUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        },
        body: formData,
      });
      const data = await response.json();
      // Deshabilitar todas las entradas (radio y select) y el botón de envío
      form.querySelectorAll('input, select').forEach((el) => {
        el.disabled = true;
      });
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      // Limpiar retroalimentación
      feedbackBox.innerHTML = '';
      // Mensaje recibido del servidor (puede incluir HTML)
      const msgP = document.createElement('p');
      msgP.innerHTML = data.feedback_html || data.message || '';
      msgP.classList.add('font-semibold');
      feedbackBox.appendChild(msgP);
      // Contenedor para explicación
      const explanationDiv = document.createElement('div');
      explanationDiv.id = 'explanation';
      feedbackBox.appendChild(explanationDiv);
      // Explicar/Continuar
      if (data.attempt_id) {
        const explainBtn = document.createElement('button');
        explainBtn.textContent = 'EXPLICAR';
        explainBtn.className = 'btn explain-btn';
        feedbackBox.appendChild(explainBtn);
        const continueBtn = document.createElement('button');
        continueBtn.textContent = 'CONTINUAR';
        continueBtn.className = 'btn continue-btn';
        feedbackBox.appendChild(continueBtn);
        // Explicación
        explainBtn.addEventListener('click', async () => {
          explainBtn.disabled = true;
          explanationDiv.innerHTML = '';
          const spinner = document.createElement('div');
          spinner.className = 'spinner';
          explanationDiv.appendChild(spinner);
          try {
            const endpointTemplate = feedbackBox.getAttribute('data-explain-endpoint');
            let endpoint = endpointTemplate;
            if (endpointTemplate) {
              endpoint = endpointTemplate.replace(/0\/?$/, `${data.attempt_id}/`);
            }
            const expRes = await fetch(endpoint, {
              method: 'POST',
              headers: { 'X-CSRFToken': csrftoken },
            });
            const expData = await expRes.json();
            explanationDiv.innerHTML = '';
            if (expRes.ok) {
              let explanationText = expData.explanation_html || expData.explanation || '';
              explanationText = highlightImportantWords(explanationText);
              const p = document.createElement('p');
              p.innerHTML = explanationText;
              explanationDiv.appendChild(p);
            } else {
              const errP = document.createElement('p');
              errP.textContent = 'No se pudo obtener la explicación.';
              explanationDiv.appendChild(errP);
            }
          } catch (err) {
            explanationDiv.innerHTML = '';
            const errP = document.createElement('p');
            errP.textContent = 'No se pudo obtener la explicación.';
            explanationDiv.appendChild(errP);
          }
        });
        continueBtn.addEventListener('click', () => {
          window.__allowLeave = true;
          window.location.href = data.next_url;
        });
      } else {
        const continueBtn = document.createElement('button');
        continueBtn.textContent = 'CONTINUAR';
        continueBtn.className = 'btn continue-btn';
        feedbackBox.appendChild(continueBtn);
        continueBtn.addEventListener('click', () => {
          window.__allowLeave = true;
          window.location.href = data.next_url;
        });
      }
    } catch (err) {
      feedbackBox.innerHTML = '';
      const errP = document.createElement('p');
      errP.textContent = err.message || 'Ocurrió un error';
      errP.classList.add('text-red-500');
      feedbackBox.appendChild(errP);
    }
  });
}

// --- Guardia anti-retroceso para la guía ---
// Si el usuario intenta volver, advertimos y, si confirma, reiniciamos intento.
(function installLeaveGuard() {
  const RESTART_URL = "/acento_1/reiniciar/";
  // Flag global para permitir salidas "legítimas" (Continuar, links con permiso, etc.)
  window.__allowLeave = false;

  // Apila un estado vacío para que el primer "Atrás" dispare popstate
  history.pushState(null, "", location.href);

  // Botón Atrás del navegador
  window.addEventListener("popstate", function () {
    if (window.__allowLeave) return;
    const msg = "Si salís ahora, perdés tu progreso de esta unidad. ¿Salir de todos modos?";
    if (confirm(msg)) {
      window.__allowLeave = true;
      location.href = RESTART_URL;  // Volvemos a la Guía y limpiamos progreso
    } else {
      history.pushState(null, "", location.href); // Nos quedamos
    }
  });

  // Cerrar pestaña/recargar: muestra aviso nativo del navegador
  window.addEventListener("beforeunload", function (e) {
    if (window.__allowLeave) return;
    e.preventDefault();
    e.returnValue = ""; // Requerido para que aparezca el diálogo
  });

  // Si clickea un enlace con permiso explícito, no molestamos
  document.addEventListener("click", function (ev) {
    const a = ev.target.closest("a");
    if (a && a.dataset.allowLeave === "1") {
      window.__allowLeave = true;
    }
  });
})();

// --- BLOQUEO DURO DE "ATRÁS" EN EL NAVEGADOR ---
(function backBlock() {
  try {
    // Crea un estado fantasma y, si el usuario intenta volver, lo volvemos a empujar
    history.pushState(null, "", location.href);
    window.addEventListener("popstate", function () {
      // Mantener en la misma URL, evitando navegar atrás
      history.pushState(null, "", location.href);
    }, { passive: true });

    // Bloquea atajos comunes de "Atrás" (Alt+← en Windows, ⌘+[ en Mac)
    window.addEventListener("keydown", function (e) {
      const k = e.key?.toLowerCase();
      if ((e.altKey && k === "arrowleft") || (e.metaKey && k === "[")) {
        e.preventDefault();
      }
    });
  } catch (_) { /* meh */ }
})();

document.addEventListener('DOMContentLoaded', () => {
  wireForm('exercise1-form');
  wireForm('exercise2-form');
  wireForm('exercise3-form');
});