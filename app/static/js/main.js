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
    
    eventDiv.innerHTML = `
        <div class="card-body">
            <div class="event-header">
                <strong>${eventType}</strong>
                <span class="event-time">${eventTime}</span>
            </div>
            <div class="text-muted">${subject}</div>
            <button class="toggle-btn" onclick="toggleEventData(this)">显示详情 ▼</button>
            <pre class="event-data mt-2 collapsed">${JSON.stringify(eventData, null, 2)}</pre>
        </div>
    `;
    
    return eventDiv;
}

function toggleEventData(button) {
    const eventData = button.nextElementSibling;
    const isCollapsed = eventData.classList.contains('collapsed');
    
    if (isCollapsed) {
        eventData.classList.remove('collapsed');
        button.textContent = '隐藏详情 ▲';
    } else {
        eventData.classList.add('collapsed');
        button.textContent = '显示详情 ▼';
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
        console.error('清除事件时出错:', error);
        connectionStatus.textContent = '清除事件失败';
        connectionStatus.className = 'alert alert-danger';
        setTimeout(() => {
            connectionStatus.textContent = '已连接到服务器';
            connectionStatus.className = 'alert alert-success';
        }, 3000);
    }
}

// 启动WebSocket连接
connectWebSocket();