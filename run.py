from app import app
import ssl
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #ssl_context.load_cert_chain(certfile=os.getenv('SSL_CERT'), keyfile=os.getenv('SSL_KEY'), password=os.getenv('SSL_PW'))
    ssl_context.load_cert_chain(certfile='Key/myserver.crt', keyfile='Key/myserver.key', password=os.getenv('SSL_PW'))
    app.run(ssl_context=ssl_context, host='0.0.0.0', port=5000, debug=True)