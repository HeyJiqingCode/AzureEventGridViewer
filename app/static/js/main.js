let ws;
const eventsContainer = document.getElementById('events-container');
const connectionStatus = document.getElementById('connection-status');
const maxEvents = 100;

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        connectionStatus.textContent = 'Connected to server';
        connectionStatus.className = 'alert alert-success';
    };

    ws.onmessage = (event) => {
        const eventData = JSON.parse(event.data);
        if (eventData.type === 'clear_events') {
            eventsContainer.innerHTML = '';
            return;
        }
        addEventToDisplay(eventData);
    };

    ws.onclose = () => {
        connectionStatus.textContent = 'Connection lost, reconnecting...';
        connectionStatus.className = 'alert alert-warning';
        // 自动重连
        setTimeout(connectWebSocket, 1000);
    };

    ws.onerror = () => {
        connectionStatus.textContent = 'Connection error';
        connectionStatus.className = 'alert alert-danger';
    };
}

// 对 HTML 特殊字符进行处理
function escapeHTML(str) {
    if (str === null || str === undefined) {
        return '';
    }
    return str.toString()
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}

function addEventToDisplay(eventData) {
    const eventElement = createEventElement(eventData);
    eventsContainer.insertBefore(eventElement, eventsContainer.firstChild);
    
    // 限制显示事件的数量
    while (eventsContainer.children.length > maxEvents) {
        eventsContainer.removeChild(eventsContainer.lastChild);
    }
}

function createEventElement(eventData) {
    const eventDiv = document.createElement('div');
    eventDiv.className = 'event-card card';
    
    const eventTime = new Date(eventData.eventTime || eventData.time).toLocaleString();
    const eventType = eventData.eventType || eventData.type;
    const subject = eventData.subject || eventData.source;

    // Stringify the event data first
    const rawJsonString = JSON.stringify(eventData, null, 2);
    // Escape the resulting string for safe HTML display
    const escapedJsonString = escapeHTML(rawJsonString);
    
    eventDiv.innerHTML = `
        <div class="card-body">
            <div class="event-header">
                <strong>${escapeHTML(eventType)}</strong> 
                <span class="event-time">${escapeHTML(eventTime)}</span>
            </div>
            <div class="text-muted">${escapeHTML(subject)}</div>
            <button class="toggle-btn" onclick="toggleEventData(this)">Show Details ▼</button>
            <pre class="event-data mt-2 collapsed">${escapedJsonString}</pre> 
        </div>
    `;
    
    return eventDiv;
}

function toggleEventData(button) {
    const eventData = button.nextElementSibling;
    const isCollapsed = eventData.classList.contains('collapsed');
    
    if (isCollapsed) {
        eventData.classList.remove('collapsed');
        button.textContent = 'Hide Details ▲';
    } else {
        eventData.classList.add('collapsed');
        button.textContent = 'Show Details ▼';
    }
}

async function clearEvents() {
    try {
        const response = await fetch('/api/events/clear', {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error('Failed to clear events');
        }
    } catch (error) {
        console.error('Error clearing events:', error);
        connectionStatus.textContent = 'Failed to clear events';
        connectionStatus.className = 'alert alert-danger';
        setTimeout(() => {
            connectionStatus.textContent = 'Connected to server';
            connectionStatus.className = 'alert alert-success';
        }, 3000);
    }
}

// 启动WebSocket连接
connectWebSocket();