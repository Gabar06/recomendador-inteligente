/*
 * Script genérico para ejercicios de opción múltiple (puntuación,
 * mayúsculas y reglas ortográficas).
 *
 * ... (descripción existente) ...
 */


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

(function installLeaveGuard() {
  window.__allowLeave = false;

  history.pushState(null, "", location.href);

  window.addEventListener("popstate", function () {
    if (window.__allowLeave) return;
    const msg = "Si salís ahora, perdés tu progreso de este ejercicio. ¿Salir de todos modos?";
    if (confirm(msg)) {
      window.__allowLeave = true;
      const match = window.location.pathname.match(/\/mc\/([^\/]+)\/(\d+)/);
      if (match) {
        const slug = match[1];
        // Opcional: Limpiar progreso vía AJAX
        fetch(`/mc/${slug}/reset/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        })
          .then(() => {
            window.location.href = `/guia_aprendizaje`;
          })
          .catch(() => {
            window.location.href = `/guia_aprendizaje`; // Redirigir de todos modos si falla
          });
      } else {
        window.location.href = '/'; // Fallback
      }
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

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('mc-form');
  const feedbackBox = document.getElementById('feedback-box');
  if (!form || !feedbackBox) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitUrl = form.dataset.submitUrl;
    const explainEndpoint = form.dataset.explainEndpoint;
    const formData = new FormData(form);
    const csrftoken = getCookie('csrftoken');
    try {
      const response = await fetch(submitUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        },
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Ocurrió un error');
      }
      feedbackBox.innerHTML = '';
      form.querySelectorAll('input[type="radio"]').forEach((radio) => {
        radio.disabled = true;
      });
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
      }
      const msgP = document.createElement('p');
      msgP.innerHTML = data.message;
      msgP.classList.add('font-semibold');
      feedbackBox.appendChild(msgP);
      const explainBtn = document.createElement('button');
      explainBtn.textContent = 'EXPLICAR';
      explainBtn.className = 'btn explain-btn';
      feedbackBox.appendChild(explainBtn);
      const continueBtn = document.createElement('button');
      continueBtn.textContent = 'CONTINUAR';
      continueBtn.className = 'btn continue-btn';
      feedbackBox.appendChild(continueBtn);
      const explanationDiv = document.createElement('div');
      explanationDiv.id = 'explanation';
      feedbackBox.appendChild(explanationDiv);

      explainBtn.addEventListener('click', async () => {
        explainBtn.disabled = true;
        explanationDiv.innerHTML = '';
        const spinner = document.createElement('div');
        spinner.className = 'spinner';
        explanationDiv.appendChild(spinner);
        try {
          const expRes = await fetch(`${explainEndpoint}?attempt_id=${data.attempt_id}`, {
            method: 'GET',
          });
          const expData = await expRes.json();
          explanationDiv.innerHTML = '';
          if (expRes.ok) {
            let explanationText = expData.explanation || '';
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
        window.__allowLeave = true; // Permitir salida sin confirmación al continuar
        window.location.href = data.next_url;
      });
    } catch (err) {
      feedbackBox.innerHTML = '';
      const errP = document.createElement('p');
      errP.textContent = err.message;
      errP.classList.add('text-red-500');
      feedbackBox.appendChild(errP);
    }
  });
});

/**
 * Resalta palabras clave en el texto de la explicación.
 * ... (código existente) ...
 */
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