from app import app
import ssl
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem', password=os.getenv('SSL_PW'))
    app.run(ssl_context=ssl_context, host='0.0.0.0', port=5000, debug=True)