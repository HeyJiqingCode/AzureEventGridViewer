let ws;
const eventsContainer = document.getElementById('events-container');
const connectionStatus = document.getElementById('connection-status');
const maxEvents = 100;

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        connectionStatus.textContent = '已连接到服务器';
        connectionStatus.className = 'alert alert-success';
    };

    ws.onmessage = (event) => {
        const eventData = JSON.parse(event.data);
        addEventToDisplay(eventData);
    };

    ws.onclose = () => {
        connectionStatus.textContent = '连接断开，正在重新连接...';
        connectionStatus.className = 'alert alert-warning';
        // 自动重连
        setTimeout(connectWebSocket, 1000);
    };

    ws.onerror = () => {
        connectionStatus.textContent = '连接错误';
        connectionStatus.className = 'alert alert-danger';
    };
}

function addEventToDisplay(eventData) {
    const eventElement = createEventElement(eventData);
    eventsContainer.insertBefore(eventElement, eventsContainer.firstChild);
    
    // 限制显示的事件数量
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
            <pre class="event-data mt-2">${JSON.stringify(eventData.data, null, 2)}</pre>
        </div>
    `;
    
    return eventDiv;
}

function clearEvents() {
    eventsContainer.innerHTML = '';
}

// 启动 WebSocket 连接
connectWebSocket();