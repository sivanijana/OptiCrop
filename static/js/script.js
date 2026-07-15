document.addEventListener('DOMContentLoaded', function () {
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('light-theme');
      const icon = themeToggle.querySelector('i');
      icon.className = document.body.classList.contains('light-theme') ? 'fas fa-sun' : 'fas fa-moon';
    });
  }

  const counters = document.querySelectorAll('.counter');
  counters.forEach(counter => {
    const target = Number(counter.dataset.target || 0);
    let current = 0;
    const increment = target / 80;
    const update = () => {
      current += increment;
      counter.textContent = Math.floor(current).toLocaleString();
      if (current < target) requestAnimationFrame(update);
      else counter.textContent = target.toLocaleString();
    };
    update();
  });

  const form = document.getElementById('predictionForm');
  const button = document.getElementById('predictButton');
  if (form && button) {
    form.addEventListener('submit', () => {
      const text = button.querySelector('.btn-text');
      const loading = button.querySelector('.loading');
      text.classList.add('d-none');
      loading.classList.remove('d-none');
      button.disabled = true;
    });
  }

  const scrollBtn = document.createElement('button');
  scrollBtn.id = 'scrollTopBtn';
  scrollBtn.className = 'btn btn-primary rounded-circle';
  scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
  document.body.appendChild(scrollBtn);
  scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener('scroll', () => {
    scrollBtn.style.display = window.scrollY > 300 ? 'block' : 'none';
  });

  const typedText = document.querySelector('[data-typing]');
  if (typedText) {
    const words = typedText.dataset.typing.split(',');
    let index = 0;
    let charIndex = 0;
    const type = () => {
      typedText.textContent = words[index].slice(0, charIndex++);
      if (charIndex <= words[index].length) setTimeout(type, 80);
      else setTimeout(() => {
        charIndex = 0;
        index = (index + 1) % words.length;
        type();
      }, 1200);
    };
    type();
  }
});
