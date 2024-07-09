# Reverse Proxy with FastAPI and ngrok

This repository contains a simple reverse proxy setup using FastAPI for handling API requests and ngrok for creating a public tunnel to the local server.

## Contents

- `api.py`: A FastAPI application with CORS middleware and a custom header middleware.
- `proxy_server.py`: A script to start an ngrok tunnel and redirect traffic to the FastAPI server.

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- ngrok

## Setup

### Install Dependencies

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/reverse-proxy.git
    cd reverse-proxy
    ```

2. Install the required packages:

    ```bash
    pip install fastapi uvicorn requests
    ```

3. Ensure you have ngrok installed. If not, download it from [ngrok's official website](https://ngrok.com/download) and follow the installation instructions.

4. Set up your ngrok auth token:

    ```bash
    ngrok authtoken YOUR_NGROK_AUTH_TOKEN
    ```

### Configuration

- Update the `NGROK_AUTH_TOKEN` in `proxy_server.py` with your ngrok auth token.

### Running the Server

1. Start the FastAPI server:

    ```bash
    python api.py
    ```

2. In another terminal, start the ngrok tunnel using the provided script:

    ```bash
    python proxy_server.py
    ```

The script will start ngrok and redirect traffic to the FastAPI server running on port 3000. It will also log the public ngrok URL.

## Endpoints

### FastAPI Server

- **GET /**: Returns a simple JSON message with the client's IP and request path.

## Middleware

The FastAPI application includes the following middleware:

- **CORS Middleware**: Allows all origins for testing purposes.
- **Custom Header Middleware**: Adds a custom header to bypass local tunnel restrictions.

## Logging

Both `api.py` and `proxy_server.py` are configured with basic logging to track incoming requests and ngrok tunnel status.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [ngrok](https://ngrok.com/)

---

Feel free to modify the configurations and endpoints as per your requirements. Contributions and suggestions are welcome!

