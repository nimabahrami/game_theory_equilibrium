const cases = [
    'case1', 'case2', 'case3', 'case4', 'case5', 'case6', 'case7', 'case8'
];

document.addEventListener('DOMContentLoaded', () => {
    initializeTable('p1');
    initializeTable('p2');

    // Add event listeners for strategy inputs to update row labels
    const strategyInputs = [
        'nature-s1', 'nature-s2',
        'p1-strategies',
        'p2-strategies'
    ];

    strategyInputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', updateRowLabels);
        }
    });

    // Initial update
    updateRowLabels();
});

function updateRowLabels() {
    const n_s1 = document.getElementById('nature-s1').value || 'State 1';
    const n_s2 = document.getElementById('nature-s2').value || 'State 2';

    // Parse strategies from comma-separated string
    const p1_strats_raw = document.getElementById('p1-strategies').value || 'Action 1, Action 2';
    const p1_strats = p1_strats_raw.split(',').map(s => s.trim());
    const p1_s1 = p1_strats[0] || 'Action 1';
    const p1_s2 = p1_strats[1] || 'Action 2';

    const p2_strats_raw = document.getElementById('p2-strategies').value || 'Action 1, Action 2';
    const p2_strats = p2_strats_raw.split(',').map(s => s.trim());
    const p2_s1 = p2_strats[0] || 'Action 1';
    const p2_s2 = p2_strats[1] || 'Action 2';

    const caseDescriptions = {
        'case1': `${n_s2}, ${p1_s1}, ${p2_s1}`,
        'case2': `${n_s2}, ${p1_s2}, ${p2_s1}`,
        'case3': `${n_s1}, ${p1_s1}, ${p2_s1}`,
        'case4': `${n_s1}, ${p1_s2}, ${p2_s1}`,
        'case5': `${n_s2}, ${p1_s1}, ${p2_s2}`,
        'case6': `${n_s2}, ${p1_s2}, ${p2_s2}`,
        'case7': `${n_s1}, ${p1_s1}, ${p2_s2}`,
        'case8': `${n_s1}, ${p1_s2}, ${p2_s2}`
    };

    ['p1', 'p2'].forEach(player => {
        const tbody = document.querySelector(`#${player}-table tbody`);
        const rows = tbody.querySelectorAll('tr');
        rows.forEach(row => {
            const caseName = row.dataset.case;
            const labelCell = row.querySelector('td:first-child');
            if (labelCell) {
                labelCell.textContent = caseDescriptions[caseName];
                labelCell.style.fontSize = '0.8em';
            }
        });
    });
}

function initializeTable(player) {
    const tbody = document.querySelector(`#${player}-table tbody`);
    tbody.innerHTML = ''; // Clear existing

    cases.forEach(caseName => {
        const tr = document.createElement('tr');
        tr.dataset.case = caseName;

        // Case Label Cell
        const tdLabel = document.createElement('td');
        // Text content will be set by updateRowLabels
        tr.appendChild(tdLabel);

        tbody.appendChild(tr);
    });
    updateRowLabels();
}

function showAddForm(player) {
    document.getElementById(`add-form-${player}`).classList.remove('hidden');
    document.getElementById(`add-btn-${player}`).classList.add('hidden');
    document.getElementById(`new-var-${player}`).focus();
}

function hideAddForm(player) {
    document.getElementById(`add-form-${player}`).classList.add('hidden');
    document.getElementById(`add-btn-${player}`).classList.remove('hidden');
    document.getElementById(`new-var-${player}`).value = ''; // Clear input
}

function confirmAddVariable(player) {
    const input = document.getElementById(`new-var-${player}`);
    const varName = input.value.trim();

    if (!varName) {
        alert("Please enter a variable name.");
        return;
    }

    addVariableToTable(player, varName);
    hideAddForm(player);
}

function addVariableToTable(player, varName) {
    const table = document.querySelector(`#${player}-table`);
    const theadRow = table.querySelector('thead tr');
    const tbodyRows = table.querySelectorAll('tbody tr');

    // Add Header
    const th = document.createElement('th');
    th.textContent = varName;
    th.dataset.var = varName; // Store initial variable name
    th.contentEditable = "true"; // Make editable
    th.classList.add('editable-header');

    // Update dataset when edited
    th.addEventListener('blur', function () {
        const newName = this.textContent.trim();
        if (newName) {
            this.dataset.var = newName;
        } else {
            this.textContent = this.dataset.var; // Revert if empty
        }
    });

    theadRow.appendChild(th);

    // Add Input Cells
    tbodyRows.forEach(tr => {
        const td = document.createElement('td');
        const input = document.createElement('input');
        input.type = 'number';
        input.step = 'any';
        input.value = 0; // Default value
        input.dataset.player = player;
        // input.dataset.var = varName; // We will rely on column index now
        input.dataset.case = tr.dataset.case;
        td.appendChild(input);
        tr.appendChild(td);
    });
}

async function calculateEquilibrium() {
    const p1Name = document.getElementById('p1-name').value;
    const p2Name = document.getElementById('p2-name').value;

    // Strategies
    const natureStrategies = [
        document.getElementById('nature-s1').value,
        document.getElementById('nature-s2').value
    ];

    const p1Strategies = document.getElementById('p1-strategies').value.split(',').map(s => s.trim()).filter(s => s);
    const p2Strategies = document.getElementById('p2-strategies').value.split(',').map(s => s.trim()).filter(s => s);

    // Payoff Functions
    const p1Function = document.getElementById('p1-function').value.trim();
    const p2Function = document.getElementById('p2-function').value.trim();

    const payoffData = {
        'p1': collectPlayerData('p1'),
        'p2': collectPlayerData('p2')
    };

    // Validation: Check if any variables exist
    if (Object.keys(payoffData.p1).length === 0 || Object.keys(payoffData.p2).length === 0) {
        alert("Please add at least one payoff variable for each player before calculating.");
        return;
    }

    const payload = {
        'p1_name': p1Name,
        'p2_name': p2Name,
        'nature_strategies': natureStrategies,
        'p1_strategies': p1Strategies,
        'p2_strategies': p2Strategies,
        'payoff_data': payoffData,
        'p1_payoff_function': p1Function,
        'p2_payoff_function': p2Function
    };

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.status === 'success') {
            displayResults(result.equilibria);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while calculating equilibrium.');
    }
}

function collectPlayerData(player) {
    const data = {};
    const table = document.querySelector(`#${player}-table`);
    const headers = table.querySelectorAll('thead th');
    const rows = table.querySelectorAll('tbody tr');

    // Skip first header (Case label)
    for (let i = 1; i < headers.length; i++) {
        const varName = headers[i].textContent.trim(); // Use text content as key
        data[varName] = {};

        rows.forEach(row => {
            const caseName = row.dataset.case;
            // Get the cell at the same index
            const cell = row.children[i];
            const input = cell.querySelector('input');
            if (input) {
                data[varName][caseName] = parseFloat(input.value) || 0;
            }
        });
    }
    return data;
}

function displayResults(equilibria) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');

    resultsContent.innerHTML = ''; // Clear previous
    resultsSection.classList.remove('hidden');

    if (equilibria.length === 0) {
        resultsContent.innerHTML = '<p>No Nash Equilibria found.</p>';
        return;
    }

    const p1Name = document.getElementById('p1-name').value;
    const p2Name = document.getElementById('p2-name').value;

    equilibria.forEach((eq, index) => {
        const div = document.createElement('div');
        div.className = 'result-item';

        // Format strategies
        const p1Strat = JSON.stringify(eq.p1_strategy, null, 2);
        const p2Strat = JSON.stringify(eq.p2_strategy, null, 2);

        div.innerHTML = `
            <h3>Equilibrium ${index + 1}</h3>
            <p><strong>${p1Name} Strategy:</strong> <pre>${p1Strat}</pre></p>
            <p><strong>${p2Name} Strategy:</strong> <pre>${p2Strat}</pre></p>
            <p><strong>Valid Range (ro):</strong> ${eq.ro_range}</p>
        `;
        resultsContent.appendChild(div);
    });
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}
