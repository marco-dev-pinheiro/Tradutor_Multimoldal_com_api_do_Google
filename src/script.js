let recorder, chunks = [];
async function start() {
  const s = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(s);
  chunks = [];
  recorder.ondataavailable = e => chunks.push(e.data);
  recorder.onstop = async () => {
    const b = new Blob(chunks);
    const r = new FileReader();
    r.readAsDataURL(b);
    r.onloadend = () => google.colab.kernel.invokeFunction('callback_rec', [r.result], {});
  };
  recorder.start();
  document.getElementById('rec').disabled = true;
  document.getElementById('stop').disabled = false;
  document.getElementById('status').innerHTML = '<span class="recording-pulse"></span> Gravando Áudio...';
}

function stop() {
  recorder.stop();
  document.getElementById('stop').disabled = true;
  document.getElementById('rec').disabled = false;
  document.getElementById('status').innerText = "⏳ Processando tradução...";
}

