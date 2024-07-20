// static/main.js

// Dropdown home page
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

// Buttons
document.getElementById('btnregister').onclick = function() {
    window.location.href = '/signup';
};

document.getElementById('btnlogin').onclick = function() {
    window.location.href = '/login';
}

document.getElementById('btnPTdemo').onclick = function() {
    window.location.href = '/'; // change once implemented
}