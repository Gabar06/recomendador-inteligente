/*
 * Script para el ejercicio interactivo de puntuación.
 *
 * Este archivo se encarga de registrar los clics del usuario en los
 * espacios entre palabras, enviar la información al servidor mediante
 * AJAX, mostrar la retroalimentación y actualizar la puntuación.  Tras
 * cada intento se ofrecen opciones para pedir una explicación y
 * continuar con el siguiente signo.  Cuando se completan todos los
 * signos, se redirige a la página de resultados.
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

document.addEventListener('DOMContentLoaded', () => {
  const exercise = document.getElementById('exercise');
  if (!exercise) return;
  let currentStep = parseInt(exercise.dataset.step, 10);
  const totalSteps = parseInt(exercise.dataset.total, 10);
  let score = parseInt(exercise.dataset.score, 10);
  const submitUrl = exercise.dataset.submitUrl;
  const explainUrl = exercise.dataset.explainUrl;
  const feedbackBox = document.getElementById('feedback-box');
  const scoreDisplay = document.getElementById('score-display');

  // Manejar clics en cada espacio.  Los espacios clicables se identifican
  // mediante la clase .space.clickable.  Una vez que se ha respondido un
  // paso, se bloquean los clics hasta que se presione continuar.
  document.querySelectorAll('.space.clickable').forEach((spaceEl) => {
    spaceEl.addEventListener('click', async (ev) => {
      // Evitar clics si hay retroalimentación pendiente
      if (feedbackBox.dataset.locked === '1') return;
      const index = parseInt(ev.target.dataset.index, 10);
      try {
        const formData = new FormData();
        formData.append('index', index);
        formData.append('step', currentStep);
        const csrftoken = getCookie('csrftoken');
        const response = await fetch(submitUrl, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'Error inesperado');
        }
        // Insertar el signo de puntuación en el lugar correcto
        const selector = `.space[data-index="${data.correct_index}"]`;
        const correctSpace = document.querySelector(selector);
        if (correctSpace) {
          correctSpace.textContent = data.expected_punctuation;
          correctSpace.classList.remove('clickable');
          correctSpace.classList.add('font-bold', 'text-green-600');
        }
        // Actualizar la puntuación local
        if (data.is_correct) {
          score = data.score;
        }
        scoreDisplay.textContent = `Correctas ${score} de ${totalSteps}`;
        // Mostrar mensaje y botones
        feedbackBox.innerHTML = '';
        const msgP = document.createElement('p');
        msgP.textContent = data.message;
        msgP.className = data.is_correct ? 'text-green-700 fw-bold' : 'text-red-700 fw-bold';
        feedbackBox.appendChild(msgP);
        const explainBtn = document.createElement('button');
        explainBtn.textContent = 'EXPLICAR';
        explainBtn.className = 'btn btn-outline-info btn-sm me-2 mt-2';
        feedbackBox.appendChild(explainBtn);
        const continueBtn = document.createElement('button');
        continueBtn.textContent = 'CONTINUAR';
        continueBtn.className = 'btn btn-success btn-sm mt-2';
        feedbackBox.appendChild(continueBtn);
        // Bloquear clics hasta que el usuario decida continuar
        feedbackBox.dataset.locked = '1';
        // Explicación de OpenAI
        explainBtn.addEventListener('click', async () => {
          try {
            explainBtn.disabled = true;
            const resExp = await fetch(`${explainUrl}?attempt_id=${data.attempt_id}`, { method: 'GET' });
            const expData = await resExp.json();
            const expP = document.createElement('p');
            expP.textContent = expData.explanation;
            expP.className = 'mt-2';
            feedbackBox.appendChild(expP);
          } catch (err) {
            const errorP = document.createElement('p');
            errorP.textContent = 'No se pudo obtener la explicación.';
            errorP.className = 'text-danger mt-2';
            feedbackBox.appendChild(errorP);
          }
        });
        continueBtn.addEventListener('click', () => {
          currentStep = data.next_step;
          feedbackBox.innerHTML = '';
          feedbackBox.dataset.locked = '';
          // Si el ejercicio terminó, redirigir a la página de resultados
          if (data.finished) {
            window.location.href = data.result_url;
          }
        });
      } catch (err) {
        console.error(err);
        feedbackBox.innerHTML = '';
        const errP = document.createElement('p');
        errP.textContent = err.message;
        errP.className = 'text-danger';
        feedbackBox.appendChild(errP);
      }
    });
  });
});