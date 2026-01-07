// Unified Batch Prediction Logic with Manual and Paste Support

document.addEventListener('DOMContentLoaded', () => {
    const tableContainer = document.getElementById('data-table-container');
    const TABLE_ID = 'unified-input-table';
    const BODY_ID = 'table-body';

    // Config
    const headers = [
        'Gender', 'Age', 'Driving_License', 'Region_Code', 'Previously_Insured',
        'Annual_Premium', 'Policy_Sales_Channel', 'Vintage',
        'Vehicle_Age', 'Vehicle_Damage'
    ];

    // Initial Render
    renderTableStructure();

    // Global Paste Listener (Capture paste anywhere on the page, or scoped to table)
    document.addEventListener('paste', handlePaste);

    // Button Listeners
    const addRowBtn = document.getElementById('add-row-btn');
    if (addRowBtn) addRowBtn.addEventListener('click', () => addRow());

    const predictBtn = document.getElementById('predict-btn');
    if (predictBtn) predictBtn.addEventListener('click', () => handlePredict(predictBtn));

    // --- Core Functions ---

    function renderTableStructure() {
        if (!tableContainer) return;

        const table = document.createElement('table');
        table.className = 'preview-table';
        table.id = TABLE_ID;

        // Header
        const thead = document.createElement('thead');
        const trh = document.createElement('tr');
        headers.forEach(h => {
            const th = document.createElement('th');
            th.textContent = h.replace(/_/g, ' ');
            trh.appendChild(th);
        });

        // Prediction Column
        const thPred = document.createElement('th');
        thPred.textContent = 'Prediction';
        thPred.style.color = 'var(--accent-2)';
        trh.appendChild(thPred);

        // Action Column
        const thAction = document.createElement('th');
        trh.appendChild(thAction);

        thead.appendChild(trh);
        table.appendChild(thead);

        // Body
        const tbody = document.createElement('tbody');
        tbody.id = BODY_ID;
        table.appendChild(tbody);
        tableContainer.innerHTML = '';
        tableContainer.appendChild(table);

        // Add initial empty row
        addRow();
    }

    function addRow(data = null) {
        const tbody = document.getElementById(BODY_ID);
        const tr = document.createElement('tr');

        headers.forEach((h, i) => {
            const td = document.createElement('td');
            // Make cell editable
            td.contentEditable = 'true';
            td.spellcheck = false;

            // Set data if provided, else empty
            td.textContent = (data && data[i] !== undefined) ? data[i] : '';

            // Basic styling on blur/focus
            td.addEventListener('blur', () => {
                if (td.textContent.trim() !== '') td.style.background = 'rgba(255,255,255,0.05)';
                else td.style.background = '';
            });

            td.addEventListener('focus', () => {
                td.style.background = 'var(--accent-soft)';
            });

            tr.appendChild(td);
        });

        // Prediction Cell (Read-only)
        const predTd = document.createElement('td');
        predTd.className = 'pred-cell';
        predTd.style.fontWeight = 'bold';
        tr.appendChild(predTd);

        // Remove Button
        const actionTd = document.createElement('td');
        actionTd.style.textAlign = 'center';
        const delBtn = document.createElement('button');
        delBtn.innerHTML = '&times;';
        delBtn.title = 'Remove Row';
        delBtn.style.background = 'transparent';
        delBtn.style.border = 'none';
        delBtn.style.color = 'rgba(255,255,255,0.4)';
        delBtn.style.fontSize = '1.2rem';
        delBtn.style.cursor = 'pointer';
        delBtn.onclick = () => {
            if (tbody.children.length > 1) tr.remove();
            else {
                // If it's the last row, just clear content
                Array.from(tr.querySelectorAll('td[contenteditable]')).forEach(td => td.textContent = '');
                tr.querySelector('.pred-cell').textContent = '';
                tr.querySelector('.pred-cell').className = 'pred-cell';
            }
        };
        actionTd.appendChild(delBtn);
        tr.appendChild(actionTd);

        tbody.appendChild(tr);
    }

    function handlePaste(e) {
        // Prevent default paste behavior if we are inside the table or body
        const clipboardData = (e.clipboardData || window.clipboardData).getData('text');
        if (!clipboardData) return;

        // Parse data
        const { rows } = parseCSV(clipboardData);
        if (rows.length === 0) return;

        e.preventDefault();

        const selection = window.getSelection();
        let targetRow = null;
        let targetCellIndex = 0;

        if (selection.rangeCount > 0) {
            const anchor = selection.anchorNode;
            const cell = anchor.nodeType === 3 ? anchor.parentElement : anchor;
            if (cell.tagName === 'TD' && cell.closest('table').id === TABLE_ID) {
                targetRow = cell.parentElement;
                targetCellIndex = Array.from(targetRow.children).indexOf(cell);
            }
        }

        const tbody = document.getElementById(BODY_ID);
        let currentRow = targetRow;

        if (!currentRow) {
            const allRows = Array.from(tbody.children);
            const isFirstRowEmpty = allRows.length === 1 && isEmptyRow(allRows[0]);

            if (isFirstRowEmpty) {
                tbody.innerHTML = '';
            }
        }

        rows.forEach((rowData, rIdx) => {
            if (currentRow) {
                const cells = currentRow.querySelectorAll('td[contenteditable]');
                rowData.forEach((val, cIdx) => {
                    const effectiveIdx = targetCellIndex + cIdx;
                    if (effectiveIdx < cells.length) {
                        cells[effectiveIdx].textContent = val;
                    }
                });
                currentRow = currentRow.nextElementSibling;
            } else {
                addRow(rowData);
            }
        });
    }

    function parseCSV(text) {
        const lines = text.trim().split(/\r?\n/).filter(l => l.trim().length > 0);
        if (lines.length === 0) return { rows: [] };

        const firstLine = lines[0];
        const delim = (firstLine.indexOf('\t') !== -1) ? '\t' : ',';

        const dataRows = lines.map(line => {
            return line.split(delim).map(c => c.trim().replace(/^"|"$/g, ''));
        });

        return { rows: dataRows };
    }

    function isEmptyRow(tr) {
        return Array.from(tr.querySelectorAll('td[contenteditable]')).every(td => td.textContent.trim() === '');
    }

    async function handlePredict(btn) {
        btn.disabled = true;
        const originalText = btn.textContent;
        btn.textContent = 'Processing...';

        const tbody = document.getElementById(BODY_ID);
        const rows = Array.from(tbody.querySelectorAll('tr'));

        const dataPayload = [];
        const validRowsIndices = [];

        rows.forEach((tr, idx) => {
            if (isEmptyRow(tr)) return;

            const cells = tr.querySelectorAll('td[contenteditable]');
            const rowObj = {};

            headers.forEach((h, i) => {
                rowObj[h] = cells[i].textContent.trim();
            });

            dataPayload.push(rowObj);
            validRowsIndices.push(idx);
        });

        if (dataPayload.length === 0) {
            alert('Please enter data into the table first.');
            btn.disabled = false;
            btn.textContent = originalText;
            return;
        }

        try {
            const resp = await fetch('/predict_batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rows: dataPayload })
            });

            const result = await resp.json();

            if (result.error) {
                throw new Error(result.error);
            }

            const predictions = result.predictions || [];

            // Update UI
            validRowsIndices.forEach((rowIndex, i) => {
                const tr = rows[rowIndex];
                const p = predictions[i];
                const pCell = tr.querySelector('.pred-cell');

                pCell.textContent = p;

                // Clear previous classes
                pCell.classList.remove('prediction-yes', 'prediction-no');

                if (p === 'Yes') {
                    pCell.classList.add('prediction-yes');
                } else if (p === 'No') {
                    pCell.classList.add('prediction-no');
                }

                pCell.classList.add('updated');
                setTimeout(() => pCell.classList.remove('updated'), 1000);
            });

            const dlBtn = document.getElementById('download-btn');
            if (dlBtn) {
                dlBtn.style.display = 'inline-block';
                dlBtn.onclick = () => downloadCSV(headers, rows);
            }

        } catch (err) {
            console.error(err);
            alert('Prediction failed: ' + err.message);
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    }

    function downloadCSV(headers, rows) {
        const csvContent = [];
        csvContent.push([...headers, 'Prediction'].join(','));

        rows.forEach(tr => {
            if (isEmptyRow(tr)) return;

            const rowData = [];
            const cells = tr.querySelectorAll('td[contenteditable]');
            cells.forEach(td => rowData.push(`"${td.textContent.replace(/"/g, '""')}"`));

            const pCell = tr.querySelector('.pred-cell');
            rowData.push(`"${pCell.textContent}"`);

            csvContent.push(rowData.join(','));
        });

        const blob = new Blob([csvContent.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', 'vehicle_insurance_predictions.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});

// Admin/Demo Training Modal Logic
const trainModelBtn = document.getElementById('train-model-btn');
if (trainModelBtn) {
    trainModelBtn.addEventListener('click', () => {
        const modal = document.getElementById('training-modal');
        if (modal) {
            modal.classList.add('show');
            startDemoTraining();
        }
    });
}

function startDemoTraining() {
    const logsDiv = document.getElementById('training-logs');
    if (!logsDiv) return;
    logsDiv.innerHTML = '<div class="log-entry">$ python demo.py</div>';

    let eventSource = new EventSource('/run-demo');
    eventSource.onmessage = function (event) {
        try {
            const data = JSON.parse(event.data);
            const line = document.createElement('div');
            line.className = 'log-entry';

            if (data.type === 'log') line.textContent = data.message;
            else if (data.type === 'complete') line.textContent = `[${data.status.toUpperCase()}] ${data.message}`;
            else if (data.type === 'error') line.textContent = `Error: ${data.message}`;

            logsDiv.appendChild(line);
            logsDiv.scrollTop = logsDiv.scrollHeight;

            if (data.type === 'complete' || data.type === 'error') {
                eventSource.close();
            }
        } catch (e) { }
    };
}

const closeBtn = document.getElementById('close-modal-btn');
if (closeBtn) closeBtn.onclick = () => document.getElementById('training-modal').classList.remove('show');
