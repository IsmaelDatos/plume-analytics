console.log('Plume Analytics initialized');
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar spinner cuando se hace clic en el enlace de Battle Groups
    const battleGroupsLink = document.querySelector('a[href*="battle-groups"]');
    if (battleGroupsLink) {
        battleGroupsLink.addEventListener('click', function() {
            const spinner = document.createElement('div');
            spinner.className = 'spinner-overlay';
            spinner.innerHTML = `
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Loading Battle Groups...</p>
            `;
            document.body.appendChild(spinner);
        });
    }
});