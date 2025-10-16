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
          window.location.href = data.next_url;
        });
      } else {
        const continueBtn = document.createElement('button');
        continueBtn.textContent = 'CONTINUAR';
        continueBtn.className = 'btn continue-btn';
        feedbackBox.appendChild(continueBtn);
        continueBtn.addEventListener('click', () => {
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

document.addEventListener('DOMContentLoaded', () => {
  wireForm('exercise1-form');
  wireForm('exercise2-form');
  wireForm('exercise3-form');
});