# Azure Event Grid Viewer

A web application for viewing and monitoring Azure Event Grid events. This application provides an intuitive interface that enables you to monitor and analyze Event Grid events in real-time.

## Features

- Real-time monitoring of Azure Event Grid events
- Visualization of event data and properties
- Event filtering and search capabilities
- Responsive web interface for desktop and mobile devices
- WebSocket-based real-time updates without page refresh

## Stack

- FastAPI - High-performance Python web framework
- Uvicorn - ASGI server
- WebSockets - For real-time communication
- Azure Event Grid SDK - For handling Azure events
- Jinja2 - Template engine
- Docker - For containerized deployment

## Event Caching

The application maintains an in-memory cache of events with the following characteristics:

- Maximum of 100 most recent events are stored
- Events are stored in memory only (not persisted to disk)
- Oldest events are automatically removed when the limit is reached
- Cache is cleared when:
  - The number of events exceeds 100 (oldest events are removed)
  - User clicks the "Clear Events" button
  - Application restarts

## Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)

### Running with Python

1）Clone the repository
```bash
git clone https://github.com/HeyJiqingCode/AzureEventGridViewer.git
cd AzureEventGridViewer
```

2）Install dependencies
```bash
pip install -r requirements.txt
```

3）Start the application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 80
```

### Running with Docker

1）Build the Docker image
```bash
docker build -t azure-event-grid-viewer .
```

2）Run the Docker container
```bash
docker run -p 80:80 azure-event-grid-viewer
```

3）Access the application

Open `http://localhost` in your browser to access the application interface

## Testing

Run the test suite:

```bash
pytest
```

With coverage report:

```bash
pytest --cov=app tests/
```
