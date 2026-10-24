const sampleText = document.querySelector('#sample-text');
const fontSize = document.querySelector('#font-size');
const sizeOutput = document.querySelector('#size-output');
const track = document.querySelector('#showcase-track');
const cards = [...track.querySelectorAll('.showcase-card')];
const count = document.querySelector('#carousel-count');
const previous = document.querySelector('#carousel-prev');
const next = document.querySelector('#carousel-next');
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
document.querySelectorAll('.brand, .header-cta').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && siteNav.classList.contains('open')) {
    closeMenu();
    menuToggle.focus();
  }
});
let sizeTouched = false;
if (window.innerWidth < 500) fontSize.value = '64';

function updateSize() {
  const size = Number(fontSize.value);
  sampleText.style.fontSize = size + 'px';
  sizeOutput.value = size + ' px';
}
fontSize.addEventListener('input', () => { sizeTouched = true; updateSize(); });
document.querySelectorAll('[data-sample]').forEach(button => {
  button.addEventListener('click', () => {
    sampleText.value = button.dataset.sample;
    sampleText.focus();
  });
});
updateSize();

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
  track.scrollTo({ left: cards[index].offsetLeft - cards[0].offsetLeft, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
}
previous.addEventListener('click', () => moveCarousel(-1));
next.addEventListener('click', () => moveCarousel(1));
track.addEventListener('scroll', updateCarousel, { passive: true });
window.addEventListener('resize', updateCarousel);
window.addEventListener('resize', () => {
  if (!sizeTouched) {
    fontSize.value = window.innerWidth < 500 ? '64' : '96';
    updateSize();
  }
});
updateCarousel();

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
