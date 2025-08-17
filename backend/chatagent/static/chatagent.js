async function api(path, body){
  const opts = {method: body ? 'POST' : 'GET', headers: {'Content-Type':'application/json'}};
  if(body) opts.body = JSON.stringify(body);
  const r = await fetch(path, opts);
  return await r.json();
}

async function loadScenarios(){
  try {
    const data = await api('/api/scenarios');
    const sel = document.getElementById('scenario');
    data.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s;
      opt.textContent = s;
      sel.appendChild(opt);
    });
  } catch {}
}

async function refreshState(){
  try {
    const data = await api('/api/state');
    document.getElementById('tick').textContent = data.tick ?? 0;
    const snap = data.snapshot || data;
    document.getElementById('snapshot').textContent = JSON.stringify(snap, null, 2);
  } catch {}
}

document.getElementById('play').onclick = async () => {
  const scenario = document.getElementById('scenario').value;
  await api('/api/play', {scenario});
  refreshState();
};

document.getElementById('pause').onclick = async () => {
  await api('/api/pause', {});
  refreshState();
};

document.getElementById('step1').onclick = async () => {
  await api('/api/step', {ticks:1});
  refreshState();
};

document.getElementById('step10').onclick = async () => {
  await api('/api/step', {ticks:10});
  refreshState();
};

document.getElementById('step100').onclick = async () => {
  await api('/api/step', {ticks:100});
  refreshState();
};

loadScenarios();
refreshState();
setInterval(refreshState, 1000);
