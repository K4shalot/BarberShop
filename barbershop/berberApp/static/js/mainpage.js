// mainpage.js
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach((button, index) => {
      button.addEventListener('click', function() {
        tabContents.forEach(content => content.style.display = 'none');
        tabButtons.forEach(btn => btn.classList.remove('active'));

        tabContents[index].style.display = 'block';
        button.classList.add('active');
      });
    });
  });