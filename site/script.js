const menuToggle = document.querySelector('.menu-toggle');
const siteNav = document.querySelector('#site-nav');
function closeMenu() {
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open menu');
  siteNav.classList.remove('open');
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  siteNav.classList.toggle('open', open);
});
siteNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.querySelectorAll('.brand, .header-actions a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && siteNav.classList.contains('open')) {
    closeMenu();
    menuToggle.focus();
  }
});

const backTop = document.querySelector('.back-top');
function updateBackTop() {
  backTop.classList.toggle('is-visible', window.scrollY > 600);
}
window.addEventListener('scroll', updateBackTop, { passive: true });
updateBackTop();
backTop.addEventListener('click', () => {
  closeMenu();
  window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
});

const sampleText = document.querySelector('#sample-text');
const fontSize = document.querySelector('#font-size');
const sizeOutput = document.querySelector('#size-output');
let sizeTouched = false;
if (window.innerWidth < 500) fontSize.value = '60';
function updateSize() {
  const size = Number(fontSize.value);
  sampleText.style.fontSize = size + 'px';
  sizeOutput.value = size + ' px';
}
fontSize.addEventListener('input', () => { sizeTouched = true; updateSize(); });
const sampleButtons = [...document.querySelectorAll('[data-sample]')];
function updateSelectedSample() {
  sampleButtons.forEach(button => button.setAttribute('aria-pressed', String(sampleText.value === button.dataset.sample)));
}
sampleButtons.forEach(button => button.addEventListener('click', () => {
  sampleText.value = button.dataset.sample;
  updateSelectedSample();
  sampleText.focus();
  sampleText.setSelectionRange(0, 0);
  sampleText.scrollTop = 0;
}));
sampleText.addEventListener('input', updateSelectedSample);
updateSize();
updateSelectedSample();
window.addEventListener('resize', () => {
  if (!sizeTouched) {
    fontSize.value = window.innerWidth < 500 ? '60' : '96';
    updateSize();
  }
});

const track = document.querySelector('#showcase-track');
const cards = [...track.querySelectorAll('.showcase-card')];
const count = document.querySelector('#carousel-count');
const previous = document.querySelector('#carousel-prev');
const next = document.querySelector('#carousel-next');
function currentCardIndex() {
  const left = track.scrollLeft;
  let best = 0;
  let distance = Infinity;
  cards.forEach((card, index) => {
    const gap = Math.abs(card.offsetLeft - cards[0].offsetLeft - left);
    if (gap < distance) { distance = gap; best = index; }
  });
  return best;
}
function updateCarousel() {
  const index = currentCardIndex();
  count.textContent = String(index + 1).padStart(2, '0') + ' / ' + String(cards.length).padStart(2, '0');
  previous.disabled = track.scrollLeft < 8;
  next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 8;
}
function moveCarousel(direction) {
  const index = Math.max(0, Math.min(cards.length - 1, currentCardIndex() + direction));
  track.scrollTo({ left: cards[index].offsetLeft - cards[0].offsetLeft, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
}
previous.addEventListener('click', () => moveCarousel(-1));
next.addEventListener('click', () => moveCarousel(1));
track.addEventListener('scroll', updateCarousel, { passive: true });
window.addEventListener('resize', updateCarousel);
updateCarousel();

const imageDialog = document.querySelector('#image-dialog');
const dialogImage = document.querySelector('#image-dialog-image');
const dialogCaption = document.querySelector('#image-dialog-caption');
const licenseDialog = document.querySelector('#license-dialog');
const licenseFrame = document.querySelector('#license-content');
const licenseTitle = document.querySelector('#license-dialog-title');
let lastDialogTrigger = null;
function openDialog(dialog, trigger) {
  lastDialogTrigger = trigger;
  dialog.showModal();
  dialog.querySelector('[data-close]').focus();
}
document.querySelectorAll('.image-link').forEach(link => link.addEventListener('click', event => {
  event.preventDefault();
  dialogImage.src = link.href;
  dialogImage.alt = link.querySelector('img').alt;
  dialogCaption.textContent = link.dataset.caption;
  openDialog(imageDialog, link);
}));
document.querySelectorAll('[data-license]').forEach(link => link.addEventListener('click', event => {
  event.preventDefault();
  licenseTitle.textContent = link.dataset.license;
  licenseFrame.src = link.href;
  licenseFrame.title = link.dataset.license + ' text';
  openDialog(licenseDialog, link);
}));
[imageDialog, licenseDialog].forEach(dialog => {
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    if (dialog === imageDialog) dialogImage.removeAttribute('src');
    if (lastDialogTrigger) lastDialogTrigger.focus();
  });
});

if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.classList.add('js-ready');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('[data-reveal]').forEach(element => observer.observe(element));
}
