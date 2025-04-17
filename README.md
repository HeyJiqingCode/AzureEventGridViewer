# Azure Event Grid Viewer

A web application for viewing and monitoring Azure Event Grid events. This application provides an intuitive interface that enables you to monitor and analyze Event Grid events in real-time.

## Features

- Real-time monitoring of Azure Event Grid events
- Visualization of event data and properties
- Event filtering and search capabilities
- Responsive web interface for desktop and mobile devices
- WebSocket-based real-time updates without page refresh

## Technology Stack

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

## Endpoints

### Health Check

Returns the health status of the application.

```http
GET /api/health
```

### Receive Events

Handles incoming Event Grid events. Supports both single events and event arrays.

```http
POST /api/events
```

### Clear Events

Clears all stored events from the viewer.

```http
POST /api/events/clear
```

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

1）Pull the Docker image
```bash
docker pull heyjiqing.azurecr.io/eventgridviewer:1.0.0
```

2）Run the Docker container
```bash
docker run -itd -p 80:80 heyjiqing.azurecr.io/eventgridviewer:1.0.0
```

3）Access the application

Open `http://localhost` in your browser to access the application interface

### Running with Azure App Service

1）Type **app services** in the search. Under **Services**, select **App Services**.

2）In the **App Services** page, select **Create** > **Web App**.

3）In the **Basics** tab, under **Project details**, select the correct subscription. Select **Create new** resource group. Type *myResourceGroup* for the name.

4）Under **Instance details**:

- Enter a globally unique name for your web app.
- Select **Container**.
- For the Operating System, select **Linux**.
- Select a **Region** that you want to serve your app from.

5）Under **App Service Plan**, select **Create new** App Service Plan. Enter *myAppServicePlan* for the name. To change pricing plans, select **Explore pricing plans**, in the **Dev/Test** section, select **Basic B1**. Select **Select**.

6）At the top of the page, select the **Container** tab.

7）In the **Container** tab, for **Image Source**, select **Other container registries**. Under **Other container registries** options, set the following values:

- Access Type: `Public`
- Registry server URL: `https://heyjiqing.azurecr.io`.
- Image and tag: `eventgridviewer:1.0.0`

8）Select **Review + create** at the bottom of the page.

9）After validation runs, select **Create**.