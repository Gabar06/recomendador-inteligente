/*
 * Script para gestionar el flujo del ejercicio 2 de acentuación.
 *
 * Intercepta el envío del formulario de cada pregunta, envía la respuesta
 * mediante fetch hacia el servidor y muestra la retroalimentación de
 * inmediato.  También permite solicitar una explicación al modelo de
 * lenguaje invocando un endpoint dedicado y continuar a la siguiente
 * pregunta o ver los resultados finales.
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
  const form = document.getElementById('exercise2-form');
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
      // Limpiar cualquier retroalimentación previa
      feedbackBox.innerHTML = '';
      // Mostrar el mensaje de acierto o error
      const msgP = document.createElement('p');
      msgP.textContent = data.message;
      msgP.classList.add('font-semibold');
      feedbackBox.appendChild(msgP);

      // Botón de Explicar
      const explainBtn = document.createElement('button');
      explainBtn.textContent = 'EXPLICAR';
      explainBtn.className = 'btn explain-btn';
      feedbackBox.appendChild(explainBtn);
      // Botón de Continuar
      const continueBtn = document.createElement('button');
      continueBtn.textContent = 'CONTINUAR';
      continueBtn.className = 'btn continue-btn';
      feedbackBox.appendChild(continueBtn);

      // Explicación: se solicitará al servidor con el ID del intento
      explainBtn.addEventListener('click', async () => {
        try {
          explainBtn.disabled = true;
          const expRes = await fetch(`${explainEndpoint}?attempt_id=${data.attempt_id}`, {
            method: 'GET',
          });
          const expData = await expRes.json();
          const expP = document.createElement('p');
          expP.textContent = expData.explanation;
          expP.classList.add('mt-2');
          feedbackBox.appendChild(expP);
        } catch (err) {
          console.error(err);
        }
      });

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