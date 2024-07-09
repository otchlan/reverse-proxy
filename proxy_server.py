#prox_server.py
import subprocess
import time
import signal
import os
import requests
import logging

PORT = 3000
NGROK_AUTH_TOKEN = "..."

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class Server:
    def __init__(self, port):
        self.port = port
        self.tunnel_process = None

    def start_tunnel(self):
        logger.info(f"Starting ngrok on port {self.port}")
        try:
            self.tunnel_process = subprocess.Popen(
                ["ngrok", "http", str(self.port), "--authtoken", NGROK_AUTH_TOKEN],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid
            )
            time.sleep(5)  # Wait a bit for the tunnel to initialize
            if self.tunnel_process.poll() is None:
                logger.info(f"Tunnel process started with PID: {self.tunnel_process.pid}")
                tunnel_url = self.get_tunnel_url()
                if tunnel_url:
                    logger.info(f"Tunnel URL: {tunnel_url}")
                else:
                    logger.error("Failed to retrieve tunnel URL")
                    self.cleanup()
            else:
                logger.error("Tunnel process failed to start")
                self.log_subprocess_output()
                self.cleanup()
        except Exception as e:
            logger.error(f"Failed to start tunnel process: {e}")
            self.cleanup()

    def get_tunnel_url(self):
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            if response.status_code == 200:
                data = response.json()
                tunnel_url = data['tunnels'][0]['public_url']
                return tunnel_url
            else:
                logger.error(f"Failed to fetch tunnel URL, status code: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching tunnel URL: {e}")
            return None

    def serve_forever(self):
        try:
            self.start_tunnel()
            logger.info("ngrok is running. Redirecting traffic to FastAPI server.")
            while True:
                time.sleep(1)  # Keep the main thread alive to maintain the tunnel
        except KeyboardInterrupt:
            logger.info("Server interrupted")
            self.cleanup()
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            self.cleanup()

    def log_subprocess_output(self):
        if self.tunnel_process:
            stdout, stderr = self.tunnel_process.communicate()
            if stdout:
                logger.error(f"ngrok stdout: {stdout}")
            if stderr:
                logger.error(f"ngrok stderr: {stderr}")

    def cleanup(self):
        logger.info("Cleaning up server and tunnel process")
        if self.tunnel_process:
            try:
                os.killpg(os.getpgid(self.tunnel_process.pid), signal.SIGTERM)
            except ProcessLookupError:
                logger.error("Process already terminated")

if __name__ == "__main__":
    server = Server(PORT)
    server.serve_forever()
