/*
 * Script para la encuesta de opinión.
 *
 * Este archivo intercepta el envío del formulario de cada pregunta
 * de la encuesta, envía la respuesta mediante fetch al servidor y
 * muestra un mensaje de confirmación sin recargar la página.  A
 * diferencia de los ejercicios de opción múltiple, no se muestran
 * botones de explicación ni retroalimentación sobre respuestas
 * correctas.  El usuario únicamente dispone de un botón para
 * continuar con la siguiente pregunta o finalizar la encuesta.
 */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('survey-form');
  const feedbackBox = document.getElementById('feedback-box');
  if (!form || !feedbackBox) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitUrl = form.dataset.submitUrl;
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
      // Limpiar retroalimentación previa
      feedbackBox.innerHTML = '';
      // Mostrar un mensaje genérico de éxito
      const msgP = document.createElement('p');
      msgP.textContent = data.message || '¡Respuesta guardada!';
      msgP.classList.add('font-semibold');
      feedbackBox.appendChild(msgP);
      // Botón de Continuar
      const continueBtn = document.createElement('button');
      continueBtn.textContent = 'CONTINUAR';
      continueBtn.className = 'continue-btn';
      feedbackBox.appendChild(continueBtn);
      // Continuar: redirige a la siguiente pregunta o a los resultados
      continueBtn.addEventListener('click', () => {
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