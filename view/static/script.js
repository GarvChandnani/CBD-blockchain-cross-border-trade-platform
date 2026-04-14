async function fetchBlockchain() {
    try {
        const response = await fetch('/blockchain');
        const data = await response.json();
        renderBlockchain(data.chain);
        updateShipmentDropdown(data.chain);
    } catch (error) {
        console.error('Error fetching blockchain:', error);
    }
}

function renderBlockchain(chain) {
    const container = document.getElementById('blockchainLogs');
    container.innerHTML = '';

    // reverse for newest first
    [...chain].reverse().forEach(block => {
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        
        let txDetails = '';
        block.transactions.forEach(tx => {
            txDetails += `
                <div>ID: ${tx.shipment_id} | Status: ${tx.status}</div>
                ${tx.payment_released ? '<div style="color: #10b981;">[SMART CONTRACT] Payment Released!</div>' : ''}
            `;
        });

        entry.innerHTML = `
            <div><strong>Block #${block.index}</strong> [${new Date(block.timestamp * 1000).toLocaleTimeString()}]</div>
            <div class="log-hash">Hash: ${block.hash}</div>
            <div style="margin-top: 0.5rem;">${txDetails || 'Genesis Block'}</div>
        `;
        container.appendChild(entry);
    });
}

function updateShipmentDropdown(chain) {
    const dropdown = document.getElementById('updateShipmentId');
    const existingVal = dropdown.value;
    dropdown.innerHTML = '<option value="">Select Shipment...</option>';
    
    const uniqueIds = new Set();
    chain.forEach(block => {
        block.transactions.forEach(tx => {
            uniqueIds.add(tx.shipment_id);
        });
    });

    uniqueIds.forEach(id => {
        const opt = document.createElement('option');
        opt.value = id;
        opt.textContent = id;
        dropdown.appendChild(opt);
    });

    if (uniqueIds.has(existingVal)) {
        dropdown.value = existingVal;
    }
}

async function createShipment() {
    const payload = {
        shipment_id: document.getElementById('shipmentId').value,
        exporter: document.getElementById('exporter').value,
        importer: document.getElementById('importer').value,
        carrier: document.getElementById('carrier').value,
        amount: document.getElementById('amount').value
    };

    if (!payload.shipment_id || !payload.exporter) {
        alert("Please fill in basic shipment details.");
        return;
    }

    try {
        const response = await fetch('/create_shipment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        alert(data.message);
        fetchBlockchain();
        // Reset form
        document.getElementById('shipmentId').value = '';
        document.getElementById('exporter').value = '';
    } catch (error) {
        console.error('Error:', error);
    }
}

async function updateStatus() {
    const payload = {
        shipment_id: document.getElementById('updateShipmentId').value,
        status: document.getElementById('newStatus').value
    };

    if (!payload.shipment_id) {
        alert("Select a shipment first.");
        return;
    }

    try {
        const response = await fetch('/update_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        
        let msg = data.message;
        if (data.contract_executed) {
            msg += "\n\n🚀 " + data.contract_message;
        }
        alert(msg);
        
        fetchBlockchain();
        if (payload.shipment_id === document.getElementById('trackSearch').value) {
            trackShipment();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function trackShipment() {
    const shipmentId = document.getElementById('trackSearch').value;
    if (!shipmentId) return;

    try {
        const response = await fetch(`/track_shipment/${shipmentId}`);
        const data = await response.json();
        
        const timeline = document.getElementById('logisticsTimeline');
        const info = document.getElementById('trackingInfo');
        const placeholder = document.getElementById('trackingPlaceholder');

        if (data.history.length === 0) {
            placeholder.style.display = 'block';
            info.style.display = 'none';
            return;
        }

        placeholder.style.display = 'none';
        info.style.display = 'block';
        timeline.innerHTML = '';

        data.history.forEach(state => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            
            const statusClass = state.status.toLowerCase().replace(' ', '');
            
            item.innerHTML = `
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                    <h4>${state.status}</h4>
                    <p>${new Date(state.timestamp * 1000).toLocaleString()}</p>
                    <div class="status-badge status-${statusClass}">${state.status}</div>
                    ${state.payment_released ? '<div class="status-badge" style="background: rgba(16, 185, 129, 0.4); color: white; border: 1px solid var(--success);">Payment Released</div>' : ''}
                    <p style="font-size: 0.75rem; margin-top: 0.5rem;">Carrier: ${state.carrier}</p>
                </div>
            `;
            timeline.appendChild(item);
        });
    } catch (error) {
        console.error('Error tracking:', error);
    }
}

// Initial Load
fetchBlockchain();
setInterval(fetchBlockchain, 10000); // Poll every 10s
