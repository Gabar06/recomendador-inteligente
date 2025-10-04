/*
 * Script genérico para ejercicios de opción múltiple (puntuación,
 * mayúsculas y reglas ortográficas).
 *
 * Este archivo intercepta el envío del formulario de cada pregunta,
 * envía la respuesta mediante fetch al servidor y muestra la
 * retroalimentación de inmediato.  También permite solicitar una
 * explicación al modelo de lenguaje invocando un endpoint dedicado y
 * continuar a la siguiente pregunta o ver los resultados finales.
 *
 * La retroalimentación puede incluir etiquetas HTML (por ejemplo,
 * <strong>) para resaltar la respuesta correcta.  Por ello se usa
 * innerHTML en lugar de textContent al insertar el mensaje.
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
      // Limpiar retroalimentación previa
      feedbackBox.innerHTML = '';
      // Mostrar el mensaje de acierto o error con posible HTML
      const msgP = document.createElement('p');
      msgP.innerHTML = data.message;
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
      // Manejar clic en Explicar: mostrar explicación en un alerta
      explainBtn.addEventListener('click', async () => {
        try {
          explainBtn.disabled = true;
          const expRes = await fetch(`${explainEndpoint}?attempt_id=${data.attempt_id}`, {
            method: 'GET',
          });
          const expData = await expRes.json();
          if (expRes.ok) {
            alert(expData.explanation);
          } else {
            alert('No se pudo obtener la explicación.');
          }
        } catch (err) {
          alert('No se pudo obtener la explicación.');
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