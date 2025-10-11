document.addEventListener('DOMContentLoaded', () => {
  // Mobile nav toggle
  const toggles = document.querySelectorAll('[data-toggle="nav"]');
  const navTarget = document.querySelector('[data-target="nav"]');
  
  toggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      if (navTarget) {
        navTarget.classList.toggle('is-open');
      }
    });
  });

  // Auto-close mobile nav when link is clicked
  if (navTarget) {
    const navLinks = navTarget.querySelectorAll('a');
    navLinks.forEach((link) => {
      link.addEventListener('click', () => {
        navTarget.classList.remove('is-open');
      });
    });
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Scroll-to-top button
  const scrollTopBtn = document.getElementById('scroll-to-top');
  if (scrollTopBtn) {
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 400) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    });

    // Scroll to top when clicked
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
});

