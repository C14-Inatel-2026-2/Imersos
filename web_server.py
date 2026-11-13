
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class ImersosHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/health"):
            self.send_error(404, "Rota nao encontrada")
            return

        resposta = {
            "aplicacao": "Biblioteca Imersos",
            "status": "online",
            "ambiente": "Render"
        }

        conteudo = json.dumps(resposta).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", "10000"))
    servidor = ThreadingHTTPServer(
        ("0.0.0.0", porta),
        ImersosHandler
    )
    print(f"Imersos iniciado na porta {porta}", flush=True)
    servidor.serve_forever()
