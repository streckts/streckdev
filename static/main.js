// static/main.js

document.addEventListener('DOMContentLoaded', (event) => {
    const acc = document.querySelectorAll('.vertical-accordion-title');
    acc.forEach(title => {
        title.addEventListener('click', function() {
            const content = this.nextElementSibling;
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
        });
    });
});

const toolColors = {
    'HTML': 'blue',
    'CSS': 'green',
    'JavaScript': 'gold',
    'Python': 'yellowgreen',
    'React': 'skyblue',
    'Django': 'darkgreen'
    // Add more tools and their corresponding colors here
};

document.querySelectorAll('.tool').forEach(tool => {
    const toolName = tool.textContent.trim();
    if (toolColors[toolName]) {
        tool.style.backgroundColor = toolColors[toolName];
    }
});
