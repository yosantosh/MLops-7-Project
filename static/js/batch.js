// Batch paste, preview table, send to /predict_batch and download CSV

function detectDelimiter(line){
    if(line.indexOf('\t') !== -1) return '\t';
    if(line.indexOf(',') !== -1) return ',';
    return '\t';
}

function parseClipboardText(text){
    const lines = text.trim().split(/\r?\n/).filter(l=>l.trim().length>0);
    if(lines.length === 0) return {headers:[], rows:[]};

    const delim = detectDelimiter(lines[0]);
    const first = lines[0].split(delim).map(h=>h.trim());

    // Heuristic: treat first row as header when any cell contains non-numeric or matches known feature names
    const known = ['Gender','Age','Driving_License','Region_Code','Previously_Insured','Annual_Premium','Policy_Sales_Channel','Vintage','Vehicle_Age_lt_1_Year','Vehicle_Age_gt_2_Years','Vehicle_Damage_Yes'];
    const firstIsHeader = first.some(h => isNaN(h)) || first.some(h=> known.includes(h));

    let headers = [];
    let dataLines = [];
    if(firstIsHeader){
        headers = first;
        dataLines = lines.slice(1);
    } else {
        // generate headers
        const cols = first.length;
        headers = Array.from({length:cols},(_,i)=>`Col_${i+1}`);
        dataLines = lines;
    }

    const rows = dataLines.map(line => line.split(delim).map(cell=>cell.trim()));
    return {headers, rows};
}

function renderPreview(headers, rows){
    const container = document.getElementById('paste-preview');
    container.innerHTML = '';
    const table = document.createElement('table');
    table.className = 'preview-table';
    const thead = document.createElement('thead');
    const trh = document.createElement('tr');
    headers.forEach(h=>{
        const th = document.createElement('th'); th.textContent = h; trh.appendChild(th);
    });
    trh.appendChild(document.createElement('th')).textContent = 'Prediction';
    thead.appendChild(trh);
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    rows.forEach(r=>{
        const tr = document.createElement('tr');
        headers.forEach((_,i)=>{
            const td = document.createElement('td');
            td.contentEditable = 'true';
            td.textContent = r[i] !== undefined ? r[i] : '';
            tr.appendChild(td);
        });
        const predTd = document.createElement('td'); predTd.textContent = ''; tr.appendChild(predTd);
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    container.appendChild(table);

    const actions = document.createElement('div'); actions.className = 'preview-actions';
    const predictBtn = document.createElement('button'); predictBtn.textContent = 'Predict All'; predictBtn.className='submit-btn';
    const downloadBtn = document.createElement('button'); downloadBtn.textContent = 'Download CSV'; downloadBtn.className='submit-btn'; downloadBtn.style.marginLeft='10px'; downloadBtn.style.display='none';
    actions.appendChild(predictBtn); actions.appendChild(downloadBtn);
    container.appendChild(actions);

    predictBtn.addEventListener('click', async ()=>{
        predictBtn.disabled = true; predictBtn.textContent = 'Predicting...';
        const tableRows = Array.from(tbody.querySelectorAll('tr'));
        const objects = tableRows.map(tr=>{
            const cols = Array.from(tr.querySelectorAll('td'));
            const obj = {};
            headers.forEach((h,i)=>{
                let v = cols[i].textContent.trim();
                // try convert numeric
                if(v!=='' && !isNaN(v)) v = Number(v);
                obj[h] = v;
            });
            return obj;
        });

        try{
            const resp = await fetch('/predict_batch',{
                method:'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({rows: objects})
            });
            const data = await resp.json();
            if(data.error){ alert('Error: '+data.error); predictBtn.disabled=false; predictBtn.textContent='Predict All'; return; }
            const preds = data.predictions || [];
            tableRows.forEach((tr,idx)=>{
                const predCell = tr.querySelectorAll('td')[headers.length];
                predCell.textContent = preds[idx] || '';
                predCell.style.color = preds[idx] === 'Response-Yes' ? '#ffb0d9' : '#ff7aa0';
            });
            downloadBtn.style.display = 'inline-block';
            predictBtn.textContent = 'Done';
        }catch(err){ alert('Error: '+err.message); }
        finally{ predictBtn.disabled = false; }
    });

    downloadBtn.addEventListener('click', ()=>{
        // compose CSV from table
        const rowsOut = [];
        const headerRow = headers.concat(['Prediction']);
        rowsOut.push(headerRow.join(','));
        const tableRows = Array.from(tbody.querySelectorAll('tr'));
        tableRows.forEach(tr=>{
            const cols = Array.from(tr.querySelectorAll('td')).map(td=> '"'+td.textContent.replace(/"/g,'""')+'"');
            rowsOut.push(cols.join(','));
        });
        const csv = rowsOut.join('\n');
        const blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a'); a.href = url; a.download = 'predictions.csv'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    });
}

// Hook paste textarea
document.addEventListener('DOMContentLoaded', ()=>{
    const pasteArea = document.getElementById('paste-area');
    if(pasteArea){
        pasteArea.addEventListener('paste', (e)=>{
            const text = (e.clipboardData || window.clipboardData).getData('text');
            if(!text) return;
            e.preventDefault();
            const {headers, rows} = parseClipboardText(text);
            renderPreview(headers, rows);
        });
    }

    // also include existing single-form handler if present
    const form = document.getElementById('prediction-form');
    if(form){
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams(data),
                });
                const result = await response.json();
                if (result.prediction) {
                    const resultText = document.getElementById('result-text');
                    if(resultText) resultText.textContent = result.prediction;
                    const resEl = document.getElementById('result'); if(resEl) resEl.style.display='block';
                } else if (result.error) {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    }
});
