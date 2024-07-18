// static/main.js

document.addEventListener('DOMContentLoaded', (event) => {
    const acc = document.querySelectorAll('.vertical-accordion-title');
    acc.forEach(title => {
        title.addEventListener('click', function() {
            const content = this.nextElementSibling;
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
        });
    });

    document.querySelectorAll('.tool').forEach(tool => {
        const toolName = tool.textContent.trim().toLowerCase();
        tool.classList.add(toolName);
    });
});

document.getElementById('btnregister').onclick = function() {
    window.location.href = '/signup';
};