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

  /**
   * Reproduce un breve sonido de clic utilizando la Web Audio API.
   * Se crea un oscilador de onda cuadrada de baja ganancia que suena
   * por una fracción de segundo para indicar que el usuario ha tocado
   * un espacio.  Esta función no depende de archivos externos y evita
   * recargar el servidor con solicitudes de audio.
   */
  function playClickSound() {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const oscillator = ctx.createOscillator();
      const gainNode = ctx.createGain();
      oscillator.type = 'square';
      oscillator.frequency.value = 500; // tono moderado
      gainNode.gain.value = 0.05;
      oscillator.connect(gainNode);
      gainNode.connect(ctx.destination);
      oscillator.start();
      oscillator.stop(ctx.currentTime + 0.07);
    } catch (e) {
      // En dispositivos o navegadores que no soportan AudioContext no hacemos nada
    }
  }

  /**
   * Avanza al siguiente paso del ejercicio una vez procesada la respuesta.
   * Elimina cualquier mensaje de retroalimentación y desbloquea los clics.
   * Si el ejercicio ha concluido, muestra las opciones de explicación y
   * continuar para ir a la página de resultados; de lo contrario, no
   * presenta botones adicionales.
   *
   * @param {Object} data - Objeto devuelto por el servidor tras el POST
   */
  function advanceStep(data) {
    currentStep = data.next_step;
    // Limpiar retroalimentación y desbloquear
    feedbackBox.innerHTML = '';
    feedbackBox.dataset.locked = '';
    // Si se ha terminado, mostrar botones para explicar y continuar
    if (data.finished) {
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
      // Explicación de OpenAI para el último intento
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
        window.location.href = data.result_url;
      });
    }
  }

  // Manejar clics en cada espacio.  Los espacios clicables se identifican
  // mediante la clase .space.clickable.  Una vez que se ha respondido un
  // paso, se bloquean los clics hasta que se procese la respuesta.
  document.querySelectorAll('.space.clickable').forEach((spaceEl) => {
    spaceEl.addEventListener('click', async (ev) => {
      // Evitar clics si hay retroalimentación pendiente
      if (feedbackBox.dataset.locked === '1') return;
      playClickSound();
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
        // Actualizar la puntuación local si fue correcta
        if (data.is_correct) {
          score = data.score;
        }
        scoreDisplay.textContent = `Correctas ${score} de ${totalSteps}`;
        // Preparar mensaje de retroalimentación
        feedbackBox.innerHTML = '';
        const msgP = document.createElement('p');
        msgP.textContent = data.message;
        msgP.className = data.is_correct ? 'text-green-700 fw-bold' : 'text-red-700 fw-bold';
        feedbackBox.appendChild(msgP);
        // Bloquear clics mientras se procesa la siguiente acción
        feedbackBox.dataset.locked = '1';
        // Si la respuesta fue correcta y no se ha terminado, avanzar automáticamente
        if (data.is_correct && !data.finished) {
          // Espera breve para que el usuario lea el mensaje
          setTimeout(() => {
            advanceStep(data);
          }, 700);
        } else if (!data.is_correct) {
          // Si es incorrecta, marcar el espacio seleccionado con error y mostrar botones
          ev.target.classList.add('error');
          // Crear botones de explicación y continuar para este intento
          const explainBtn = document.createElement('button');
          explainBtn.textContent = 'EXPLICAR';
          explainBtn.className = 'btn btn-outline-info btn-sm me-2 mt-2';
          feedbackBox.appendChild(explainBtn);
          const continueBtn = document.createElement('button');
          continueBtn.textContent = 'CONTINUAR';
          continueBtn.className = 'btn btn-success btn-sm mt-2';
          feedbackBox.appendChild(continueBtn);
          // Configurar eventos para estos botones
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
            // Limpiar marca de error al pasar al siguiente paso
            ev.target.classList.remove('error');
            advanceStep(data);
          });
        } else if (data.finished && data.is_correct) {
          // Última respuesta correcta: mostrar opciones
          // Mostrar botones para explicación y continuar al final
          const explainBtn = document.createElement('button');
          explainBtn.textContent = 'EXPLICAR';
          explainBtn.className = 'btn btn-outline-info btn-sm me-2 mt-2';
          feedbackBox.appendChild(explainBtn);
          const continueBtn = document.createElement('button');
          continueBtn.textContent = 'CONTINUAR';
          continueBtn.className = 'btn btn-success btn-sm mt-2';
          feedbackBox.appendChild(continueBtn);
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
            window.location.href = data.result_url;
          });
        }
      } catch (err) {
        console.error(err);
        feedbackBox.innerHTML = '';
        const errP = document.createElement('p');
        errP.textContent = err.message;
        errP.className = 'text-danger';
        feedbackBox.appendChild(errP);
        // Desbloquear para permitir nuevos intentos incluso en caso de error
        feedbackBox.dataset.locked = '';
      }
    });
  });
});