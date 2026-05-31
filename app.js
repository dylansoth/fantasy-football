// ==============================================================================
// Client-Side Logic - Leaderboard Engine (app.js)
// ==============================================================================

// Core Skill: Global State
// We store the original fetched list of players globally so that when the user
// searches, we can filter it without making repeated network requests.
let punterData = [];

// DOM Elements - Grab handles to the HTML tags so we can read/modify them
const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error-message');
const tableEl = document.getElementById('leaderboard-table');
const tbodyEl = document.getElementById('leaderboard-body');
const searchInput = document.getElementById('search-input');

/**
 * Renders the leaderboard table body dynamically based on the provided array.
 * @param {Array} players - List of punter objects
 */
function renderTable(players) {
    // Clear any existing content in the table
    tbodyEl.innerHTML = '';
    
    if (players.length === 0) {
        // If search results are empty, display a friendly notice inside the table
        tbodyEl.innerHTML = `
            <tr>
                <td colspan="10" style="text-align: center; color: var(--text-muted); padding: 40px 0;">
                    🔍 No punters found matching that search.
                </td>
            </tr>
        `;
        return;
    }
    
    // Core Skill: Loop & Template Injection
    // Iterate through the players list and build HTML strings for each row
    players.forEach((player, index) => {
        // Calculate Rank (1-indexed)
        const rank = index + 1;
        
        // CSS class targeting for Gold/Silver/Bronze effects
        let rankClass = '';
        if (rank === 1) rankClass = 'rank-1';
        else if (rank === 2) rankClass = 'rank-2';
        else if (rank === 3) rankClass = 'rank-3';
        
        // Create table row element
        const tr = document.createElement('tr');
        if (rankClass) tr.classList.add(rankClass);
        
        // Set row structure with stats formatting
        tr.innerHTML = `
            <td class="col-rank">
                <span class="rank-badge">${rank}</span>
            </td>
            <td class="col-name">${player.name}</td>
            <td class="col-team">${player.team}</td>
            <td class="col-num">${player.punts}</td>
            <td class="col-num">${player.punt_yards}</td>
            <td class="col-num">${player.inside_20}</td>
            <td class="col-num">${player.inside_10}</td>
            <td class="col-num">${player.touchbacks}</td>
            <td class="col-num">${player.blocked}</td>
            <td class="col-score">${player.fantasy_score}</td>
        `;
        
        // Inject row into tbody
        tbodyEl.appendChild(tr);
    });
}

/**
 * Fetch stats from generated JSON database (Fetch API Lifecycle)
 */
async function loadLeaderboardData() {
    try {
        // Core Skill: Async Fetch Network Request
        // We request the local punter_scores.json file.
        // Once this is on GitHub, it fetches from the repo storage on Pages!
        const response = await fetch('./punter_scores.json');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        punterData = await response.json();
        
        // Core Skill: Transition States
        // Hide loader spinner, show table, and display the parsed data
        loadingEl.classList.add('hidden');
        tableEl.classList.remove('hidden');
        
        renderTable(punterData);
        
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        
        // Display Error State to User
        loadingEl.classList.add('hidden');
        errorEl.classList.remove('hidden');
    }
}

// --- Interactive Events & Event Listeners ---

// Core Skill: Event Handlers
// Read what the user types in real-time, filter the list, and re-render
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    
    // Filter out rows that do not match the query (checks name and team)
    const filteredPlayers = punterData.filter(player => {
        const nameMatches = player.name.toLowerCase().includes(query);
        const teamMatches = player.team.toLowerCase().includes(query);
        return nameMatches || teamMatches;
    });
    
    // Redraw the table with only matched players
    renderTable(filteredPlayers);
});

// Initialize fetching once the script loads
loadLeaderboardData();
