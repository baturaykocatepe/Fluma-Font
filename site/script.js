const sampleText = document.querySelector('#sample-text');
const fontSize = document.querySelector('#font-size');
const sizeOutput = document.querySelector('#size-output');

function updateSize() {
  const size = Number(fontSize.value);
  sampleText.style.fontSize = `${size}px`;
  sizeOutput.value = `${size} px`;
}

fontSize.addEventListener('input', updateSize);
document.querySelectorAll('[data-sample]').forEach((button) => {
  button.addEventListener('click', () => {
    sampleText.value = button.dataset.sample;
    sampleText.focus();
  });
});
updateSize();
