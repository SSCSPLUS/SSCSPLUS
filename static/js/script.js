// SSCS+ Main Script

function showPopup(title, message) {
  var popup = document.getElementById('popup');
  if (!popup) return;
  var t = document.getElementById('popupTitle');
  var m = document.getElementById('popupMessage');
  if (t) t.textContent = title;
  if (m) m.textContent = message;
  popup.classList.add('show');
}

function closePopup() {
  var popup = document.getElementById('popup');
  if (popup) popup.classList.remove('show');
}

document.addEventListener('DOMContentLoaded', function() {

  // Close popup on overlay click
  var popup = document.getElementById('popup');
  if (popup) {
    popup.addEventListener('click', function(e) {
      if (e.target === this) closePopup();
    });
  }

  // Add decorative circles to admin login page
  var loginPage = document.querySelector('.login-page');
  if (loginPage) {
    loginPage.style.position = 'relative';
    var circles = [
      { styles: { width: '250px', height: '250px', top: '-100px', right: '-80px', background: 'rgba(255,255,255,0.06)', borderRadius: '50%', position: 'fixed', zIndex: '0', pointerEvents: 'none' } },
      { styles: { width: '200px', height: '200px', bottom: '-70px', left: '-60px', background: 'rgba(255,255,255,0.06)', borderRadius: '50%', position: 'fixed', zIndex: '0', pointerEvents: 'none' } },
      { styles: { width: '120px', height: '120px', top: '40%', right: '5%', background: 'rgba(255,255,255,0.04)', borderRadius: '50%', position: 'fixed', zIndex: '0', pointerEvents: 'none' } },
    ];
    circles.forEach(function(c) {
      var el = document.createElement('div');
      Object.keys(c.styles).forEach(function(prop) {
        el.style[prop] = c.styles[prop];
      });
      loginPage.appendChild(el);
    });
  }

  // Ripple effect on admin buttons
  var buttons = document.querySelectorAll('.btn:not(.action-btn)');
  buttons.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      var rect = this.getBoundingClientRect();
      var size = Math.max(rect.width, rect.height);
      var ripple = document.createElement('span');
      ripple.style.cssText = [
        'position:absolute',
        'border-radius:50%',
        'background:rgba(255,255,255,0.25)',
        'width:' + size + 'px',
        'height:' + size + 'px',
        'left:' + (e.clientX - rect.left - size / 2) + 'px',
        'top:' + (e.clientY - rect.top - size / 2) + 'px',
        'transform:scale(0)',
        'animation:rippleAnim 0.6s ease-out',
        'pointer-events:none',
      ].join(';');
      if (getComputedStyle(this).position === 'static') this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      setTimeout(function() { ripple.remove(); }, 600);
    });
  });

});

// Add ripple animation keyframes once
(function() {
  if (!document.getElementById('sscs-ripple-style')) {
    var s = document.createElement('style');
    s.id = 'sscs-ripple-style';
    s.textContent = '@keyframes rippleAnim { to { transform: scale(3); opacity: 0; } }';
    document.head.appendChild(s);
  }
})();

console.log('%c SSCS+ v1.0 ', 'background: #0a7a3a; color: white; font-size: 16px; padding: 8px 12px; border-radius: 8px; font-weight: bold;');
console.log('%c Secure Salary Credit System Plus', 'color: #0f9d58; font-size: 12px;');
