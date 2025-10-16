// CSRF helper
function getCookie(name){
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function wireForm(formId){
  const form = document.getElementById(formId);
  if(!form) return;

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const url = form.dataset.submitUrl;
    const data = new FormData(form);
    const box = form.parentElement.querySelector('.feedback-box');
    box.innerHTML = "Procesando…";

    const res = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: data
    });
    const json = await res.json();

    // render feedback + botones
    box.innerHTML = `
      <p>${json.feedback_html}</p>
      <div class="corrections"></div>
      <div class="button-group">
        ${json.attempt_id ? `<button class="btn explain-btn" id="explain-btn" data-attempt="${json.attempt_id}">EXPLICAR</button>` : ``}
        <a class="btn continue-btn" href="${json.next_url}">CONTINUAR</a>
      </div>
      <div id="explain-area"></div>
    `;

    // botón explicar (si aplica)
    const explainBtn = document.getElementById('explain-btn');
    if(explainBtn){
      explainBtn.addEventListener('click', async ()=>{
        explainBtn.disabled = true;
        const attemptId = explainBtn.dataset.attempt;
        const endpointTemplate = box.getAttribute('data-explain-endpoint'); // .../0/
        const endpoint = endpointTemplate.replace(/0\/?$/, `${attemptId}/`);
        const r = await fetch(endpoint, {method:'POST', headers:{'X-CSRFToken':getCookie('csrftoken')}});
        const j = await r.json();
        document.getElementById('explain-area').innerHTML = j.explanation_html;
        explainBtn.disabled = false;
      });
    }
  });
}

document.addEventListener('DOMContentLoaded', ()=>{
  wireForm('exercise1-form');
  wireForm('exercise2-form');
  wireForm('exercise3-form');
});
