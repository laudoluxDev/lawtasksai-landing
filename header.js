/**
 * LawTasksAI — Shared Site Header
 * Injected into every page via:
 *   <div id="site-header"></div>
 *   <script src="/header.js"></script>
 *
 * CSS lives in shared.css — no styles injected here.
 */
(function () {

  /* ── Active link detection ── */
  function getActivePath() {
    var p = window.location.pathname.replace(/\/$/, '');
    if (!p || p === '/index.html') return '/';
    return p;
  }

  var active = getActivePath();

  function navLink(href, label) {
    var isCurrent = (href === '/' ? active === '/' || active === '/index.html' : active.indexOf(href.replace('.html','')) > -1);
    return '<a href="' + href + '"' + (isCurrent ? ' class="active" aria-current="page"' : '') + '>' + label + '</a>';
  }

  /* ── HTML ── */
  var html = [
    '<header>',
    '  <div class="container">',
    '    <div class="header-inner">',
    '      <a href="/index.html" class="logo">LawTasks<span>AI</span></a>',
    '      <nav class="nav-links" id="navLinks">',
    '        ' + navLink('/', 'Home'),
    '        ' + navLink('/task-library.html', 'Task Library'),
    '        ' + navLink('/install.html', 'Install'),
    '        ' + navLink('/getting-started.html', 'Getting Started'),
    '        <div class="dropdown">',
    '          <span class="dropdown-toggle">Support</span>',
    '          <div class="dropdown-menu">',
    '            <a href="/security.html">ABA Rule 1.6 &amp; Security</a>',
    '            <a href="/download.html">Legacy Download</a>',
    '            <a href="/verified_safe.html">&#128737;&#65039; Verified Safe</a>',
    '            <a href="/terms.html">Terms of Service</a>',
    '            <a href="/privacy.html">Privacy Policy</a>',
    '            <a href="mailto:hello@lawtasksai.com">Contact Us</a>',
    '          </div>',
    '        </div>',
    '        <a href="/signup" class="header-cta">Get Free Credits</a>',
    '      </nav>',
    '      <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false">',
    '        <span></span><span></span><span></span>',
    '      </button>',
    '      <div class="mobile-overlay" id="overlay"></div>',
    '    </div>',
    '  </div>',
    '</header>'
  ].join('\n');

  var el = document.getElementById('site-header');
  if (el) el.innerHTML = html;

  /* ── Hamburger + dropdown JS ── */
  document.addEventListener('DOMContentLoaded', function () {
    var hamburger = document.getElementById('hamburger');
    var navLinks  = document.getElementById('navLinks');
    var overlay   = document.getElementById('overlay');
    if (!hamburger || !navLinks) return;

    function openNav() {
      hamburger.classList.add('active');
      navLinks.classList.add('active');
      overlay.classList.add('active');
      hamburger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }
    function closeNav() {
      hamburger.classList.remove('active');
      navLinks.classList.remove('active');
      overlay.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
    function toggleNav() {
      navLinks.classList.contains('active') ? closeNav() : openNav();
    }

    hamburger.addEventListener('click', toggleNav);
    overlay.addEventListener('click', closeNav);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { if (navLinks.classList.contains('active')) closeNav(); });
    });

    /* Mobile dropdown tap */
    document.querySelectorAll('.dropdown-toggle').forEach(function (t) {
      t.addEventListener('click', function () {
        var menu = t.nextElementSibling;
        var isOpen = menu.style.display === 'block';
        document.querySelectorAll('.dropdown-menu').forEach(function (m) { m.style.display = ''; });
        menu.style.display = isOpen ? '' : 'block';
      });
    });

    /* Desktop dropdown hover */
    document.querySelectorAll('.dropdown').forEach(function (d) {
      d.addEventListener('mouseenter', function () { d.querySelector('.dropdown-menu').style.display = 'block'; });
      d.addEventListener('mouseleave', function () { d.querySelector('.dropdown-menu').style.display = ''; });
    });
  });

})();
