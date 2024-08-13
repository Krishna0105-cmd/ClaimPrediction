document.addEventListener('DOMContentLoaded', function () {
    let layers = document.querySelectorAll('.layer');
    window.addEventListener('scroll', function () {
      let scrollPosition = window.pageYOffset;
      layers.forEach(function (layer) {
        let speed = layer.getAttribute('data-speed');
        layer.style.transform = `translateY(${scrollPosition * speed}px)`;
      });
    });
  });
  