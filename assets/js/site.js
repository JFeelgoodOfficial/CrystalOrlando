/* Crystal Orlando — progressive enhancement only. The site is complete without this file. */
(function () {
  'use strict';
  var d = document, header = d.querySelector('.site-header');

  // Sticky header hairline
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 8); };
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Scroll reveals
  var reveals = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Safety net: never leave content hidden
  setTimeout(function () { reveals.forEach(function (el) { el.classList.add('is-in'); }); }, 2500);

  // Mark the current nav item
  var path = location.pathname.replace(/index\.html$/, '');
  d.querySelectorAll('.site-nav a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href && href !== '/' && path.indexOf(href) === 0) a.setAttribute('aria-current', 'page');
    if (href === '/' && (path === '/' || path === '')) a.setAttribute('aria-current', 'page');
  });
})();
