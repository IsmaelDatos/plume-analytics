// battle_groups.js
document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let currentPage = 1;
    const itemsPerPage = 10;
    let isLoading = false;

    // Elementos del DOM
    const searchInput = document.getElementById('bg-search');
    const resultsContainer = document.getElementById('bg-results');
    const loadingIndicator = document.getElementById('bg-loading');
    const loadMoreIndicator = document.getElementById('loading-more');
    const noResultsAlert = document.getElementById('bg-no-results');
    const shownGroupsCounter = document.getElementById('shown-groups');
    const totalGroupsCounter = document.getElementById('total-groups');

    // Carga inicial en segundo plano
    loadingIndicator.style.display = 'block';
    fetch('/load_all_battle_groups/')
        .then(response => response.json())
        .then(data => {
            sessionStorage.setItem('allBattleGroups', JSON.stringify(data.groups));
            totalGroupsCounter.textContent = Object.keys(data.groups).length;
            loadingIndicator.style.display = 'none';
        });

    // Scroll infinito
    window.addEventListener('scroll', () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
            loadMoreGroups();
        }
    });

    async function loadMoreGroups() {
        if (isLoading) return;
        isLoading = true;
        loadMoreIndicator.style.display = 'block';

        try {
            const response = await fetch(`/api/battle_groups/?page=${currentPage}`);
            const data = await response.json();
            if (data.groups?.length) {
                data.groups.forEach(group => {
                    resultsContainer.appendChild(createGroupCard(group));
                });
                currentPage++;
            }
        } finally {
            loadMoreIndicator.style.display = 'none';
            isLoading = false;
        }
    }

    function createGroupCard(group) {
        const colDiv = document.createElement('div');
        colDiv.className = 'col-md-6 mb-4 group-card';
        colDiv.innerHTML = `
            <div class="card h-100">
                <div class="card-header bg-primary text-white d-flex justify-content-between">
                    <h4>Battle Group #${group.num}</h4>
                    <span class="badge bg-light text-dark">${group.wallets.length} wallets</span>
                </div>
                <div class="card-body">
                    <div class="table-responsive battle-group-table">
                        <table class="table table-sm table-hover">
                            ${generateTableRows(group.wallets)}
                        </table>
                    </div>
                </div>
            </div>
        `;
        return colDiv;
    }

    function generateTableRows(wallets) {
        return wallets.sort((a, b) => a.xpRank - b.xpRank)
            .map(wallet => `
                <tr>
                    <td>${wallet.xpRank}</td>
                    <td class="wallet-address">
                        <a href="/wallet/${wallet.walletAddress}/">
                            ${wallet.walletAddress.substring(0, 12)}...
                        </a>
                    </td>
                    <td>${wallet.totalXp}</td>
                </tr>
            `).join('');
    }
});