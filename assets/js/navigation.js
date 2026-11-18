const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.navigation-links');
function closeNavigation() {
  navigation?.classList.remove('open');
  menuButton?.setAttribute('aria-expanded', 'false');
}
menuButton?.addEventListener('click', () => {
  const open = navigation.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation?.classList.contains('open')) {
    closeNavigation();
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-nav')) closeNavigation();
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) closeNavigation();
});
