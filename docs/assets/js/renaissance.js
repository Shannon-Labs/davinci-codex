/**
 * Renaissance Theme JavaScript
 * Interactive behaviors for the da Vinci Codex website
 */

class RenaissanceTheme {
  constructor() {
    this.init();
  }

  init() {
    this.setupScrollAnimations();
    this.setupInteractiveElements();
    this.setupNavigation();
    this.setupThemeToggle();
    this.setupParallax();
    this.setupTypewriter();
    
    console.log('Renaissance theme initialized');
  }

  /**
   * Scroll-based animations using Intersection Observer
   */
  setupScrollAnimations() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          
          // Add staggered delays for grouped elements
          if (entry.target.closest('.methodology-stages') || 
              entry.target.closest('.paths-grid') ||
              entry.target.closest('.categories-grid')) {
            const siblings = Array.from(entry.target.parentElement.children);
            const index = siblings.indexOf(entry.target);
            entry.target.style.transitionDelay = `${index * 0.1}s`;
          }
        }
      });
    }, observerOptions);

    // Observe animation elements when DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
      this.observeAnimationElements(observer);
    });
  }

  observeAnimationElements(observer) {
    const selectors = [
      '.fade-in',
      '.slide-in-left', 
      '.slide-in-right',
      '.category-card',
      '.stage-card',
      '.path-card',
      '.contact-card',
      '.invention-card'
    ];

    selectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(el => {
        observer.observe(el);
      });
    });
  }

  /**
   * Interactive element behaviors
   */
  setupInteractiveElements() {
    // Hover effects for invention cards
    this.setupInventionCards();
    
    // Button ripple effects
    this.setupButtonEffects();
    
    // Floating action buttons
    this.setupFloatingActions();
  }

  setupInventionCards() {
    document.querySelectorAll('.invention-card').forEach(card => {
      card.addEventListener('mouseenter', (e) => {
        // Add glow effect
        e.target.style.boxShadow = '0 8px 32px rgba(139, 69, 19, 0.3)';
        
        // Animate stats
        const stats = e.target.querySelectorAll('.invention-stat');
        stats.forEach((stat, index) => {
          stat.style.transitionDelay = `${index * 0.05}s`;
          stat.classList.add('animate-pulse');
        });
      });

      card.addEventListener('mouseleave', (e) => {
        e.target.style.boxShadow = '';
        
        // Remove animation classes
        const stats = e.target.querySelectorAll('.invention-stat');
        stats.forEach(stat => {
          stat.classList.remove('animate-pulse');
        });
      });
    });
  }

  setupButtonEffects() {
    document.querySelectorAll('.button').forEach(button => {
      button.addEventListener('click', (e) => {
        // Create ripple effect
        const ripple = document.createElement('div');
        ripple.className = 'ripple';
        
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
          position: absolute;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.6);
          transform: scale(0);
          animation: ripple 0.6s linear;
          width: ${size}px;
          height: ${size}px;
          left: ${x}px;
          top: ${y}px;
          pointer-events: none;
        `;
        
        button.appendChild(ripple);
        
        setTimeout(() => {
          ripple.remove();
        }, 600);
      });
    });

    // Add ripple animation CSS if not already present
    if (!document.querySelector('#ripple-styles')) {
      const style = document.createElement('style');
      style.id = 'ripple-styles';
      style.textContent = `
        @keyframes ripple {
          to {
            transform: scale(4);
            opacity: 0;
          }
        }
        .animate-pulse {
          animation: pulse 1s ease-in-out;
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
      `;
      document.head.appendChild(style);
    }
  }

  setupFloatingActions() {
    // Scroll to top button
    const scrollTopBtn = this.createFloatingButton('\u2191', 'Scroll to top');
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Show/hide based on scroll position
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        scrollTopBtn.style.opacity = '1';
        scrollTopBtn.style.pointerEvents = 'auto';
      } else {
        scrollTopBtn.style.opacity = '0';
        scrollTopBtn.style.pointerEvents = 'none';
      }
    });
  }

  createFloatingButton(content, title) {
    const button = document.createElement('button');
    button.innerHTML = content;
    button.title = title;
    button.className = 'floating-action-btn';
    
    button.style.cssText = `
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      width: 3rem;
      height: 3rem;
      border-radius: 50%;
      border: none;
      background: var(--renaissance-brown, #8B4513);
      color: white;
      font-size: 1.2rem;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
      transition: all 0.3s ease;
      opacity: 0;
      pointer-events: none;
      z-index: 1000;
    `;
    
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.1)';
    });
    
    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1)';
    });
    
    document.body.appendChild(button);
    return button;
  }

  /**
   * Enhanced navigation behaviors
   */
  setupNavigation() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });

    // Progress indicator for long pages
    this.setupProgressIndicator();
  }

  setupProgressIndicator() {
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 0%;
      height: 3px;
      background: linear-gradient(90deg, #8B4513, #DAA520);
      z-index: 9999;
      transition: width 0.3s ease;
    `;
    
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = (scrollTop / docHeight) * 100;
      progressBar.style.width = scrollPercent + '%';
    });
  }

  /**
   * Theme toggle functionality
   */
  setupThemeToggle() {
    const toggleButton = document.createElement('button');
    toggleButton.innerHTML = '\u263D';
    toggleButton.title = 'Toggle dark mode';
    toggleButton.className = 'theme-toggle';
    
    toggleButton.style.cssText = `
      position: fixed;
      top: 1rem;
      right: 1rem;
      width: 2.5rem;
      height: 2.5rem;
      border-radius: 50%;
      border: 1px solid var(--border, rgba(139, 69, 19, 0.2));
      background: var(--surface, white);
      cursor: pointer;
      font-size: 1.2rem;
      transition: all 0.3s ease;
      z-index: 1001;
    `;

    toggleButton.addEventListener('click', () => {
      document.body.classList.toggle('dark-theme');
      toggleButton.innerHTML = document.body.classList.contains('dark-theme') ? '\u2609' : '\u263D';
      
      // Store preference
      localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      document.body.classList.add('dark-theme');
      toggleButton.innerHTML = '\u2609';
    }

    document.body.appendChild(toggleButton);
  }

  /**
   * Parallax scrolling effects
   */
  setupParallax() {
    const parallaxElements = document.querySelectorAll('.hero');
    
    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY;
      
      parallaxElements.forEach(element => {
        const rate = scrolled * -0.5;
        element.style.transform = `translateY(${rate}px)`;
      });
    });
  }

  /**
   * Typewriter effect for hero text
   */
  setupTypewriter() {
    const heroTitle = document.querySelector('.hero h1');
    if (heroTitle && heroTitle.textContent) {
      const text = heroTitle.textContent;
      heroTitle.textContent = '';
      heroTitle.style.borderRight = '2px solid var(--accent, #CD853F)';
      
      let index = 0;
      const typeWriter = () => {
        if (index < text.length) {
          heroTitle.textContent += text.charAt(index);
          index++;
          setTimeout(typeWriter, 100);
        } else {
          // Remove cursor after typing complete
          setTimeout(() => {
            heroTitle.style.borderRight = 'none';
          }, 1000);
        }
      };
      
      // Start typing after a short delay
      setTimeout(typeWriter, 1000);
    }
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new RenaissanceTheme();
});

// Export for use in other scripts
window.RenaissanceTheme = RenaissanceTheme;