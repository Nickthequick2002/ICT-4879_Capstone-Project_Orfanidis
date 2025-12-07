/** This script keeps the navigation bar and the navigation links sin sync
with the user's current position */

(function () {

  // All navigation links inside the main navbar
  const links = document.querySelectorAll('.navbar-nav .nav-link');


  // Sets a specific link as the active one and clears the previous active state
  function setActive(link) {
    links.forEach(l => {
      l.classList.remove('active');
      l.removeAttribute('aria-current');
    });
    if (link) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  }

  // Normalize a pathname (treat / and /index.html as the same)
  const norm = p => p.replace(/\/(index\.html?)?$/, '/');

  // Syncs nav highlight with the current URL 
  function syncWithURL() {
    const { pathname, hash } = window.location;

    // If we're using on-page sections (bmi, programs)
    if (hash) {
      const link = document.querySelector(`.navbar-nav .nav-link[href="${hash}"]`);
      if (link) { setActive(link); return; }
    }

    // If we're on separate pages, this function matches the filename or the path
    const current = norm(pathname || '/');
    let match = null;
    links.forEach(l => {

      // Converts hrefs that are relative to absolute paths for easier comparison
      const url = new URL(l.getAttribute('href'), window.location.origin);
      if (!url.hash && norm(url.pathname) === current) match = l;
    });
    setActive(match);
  }

  // Initial sync when the page loads
  syncWithURL();

  // For internal pages, makes the navigation feel instant
  links.forEach(l => {
    l.addEventListener('click', () => {
      const href = l.getAttribute('href') || '';
      if (href.startsWith('#')) setActive(l);
    });
  });

  // Updates the nav state when using browser back or forward arrows
  window.addEventListener('popstate', syncWithURL);

  // Highlighting based on scroll for internal pages
  // Uses IntersectionObserver to detect when the sections are visisble
  const sectionLinks = [...links].filter(l => (l.getAttribute('href') || '').startsWith('#'));
  const sections = sectionLinks
    .map(l => document.querySelector(l.getAttribute('href')))
    .filter(Boolean);

  if (sections.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const id = '#' + e.target.id;
          const link = document.querySelector(`.navbar-nav .nav-link[href="${id}"]`);
          if (link) setActive(link);
        }
      });
    }, { threshold: 0.5 }); // Highlights section only when it is 50% visible

    // Starts observing sections
    sections.forEach(s => io.observe(s));
  }
})();