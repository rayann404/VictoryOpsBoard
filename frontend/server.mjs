import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";
import { Socket } from "node:net";

const __dirname = fileURLToPath(new URL(".", import.meta.url));
const publicDir = join(__dirname, "src");
const port = Number(process.env.PORT || 5173);
const backendUrl = process.env.API_URL || "http://backend:8000";
const wsBackendUrl = process.env.WS_BACKEND_URL || "ws://backend:8000";

const contentTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml"
};

function send(res, status, body, headers = {}) {
  res.writeHead(status, headers);
  res.end(body);
}

async function proxyApi(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const upstream = new URL(url.pathname.replace(/^\/api/, "") + url.search, backendUrl);
  const headers = new Headers(req.headers);
  headers.delete("host");
  headers.delete("connection");

  try {
    const response = await fetch(upstream, {
      method: req.method,
      headers,
      body: ["GET", "HEAD"].includes(req.method || "GET") ? undefined : req,
      duplex: "half"
    });

    const responseHeaders = Object.fromEntries(response.headers.entries());
    delete responseHeaders["connection"];
    delete responseHeaders["transfer-encoding"];
    send(res, response.status, Buffer.from(await response.arrayBuffer()), responseHeaders);
  } catch (error) {
    send(
      res,
      502,
      JSON.stringify({
        detail: `Cannot reach backend at ${backendUrl}`,
        error: error instanceof Error ? error.message : String(error)
      }),
      { "content-type": "application/json; charset=utf-8" }
    );
  }
}

async function serveStatic(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const requestedPath = url.pathname === "/" ? "/index.html" : url.pathname;
  const filePath = normalize(join(publicDir, requestedPath));

  if (!filePath.startsWith(publicDir)) {
    send(res, 403, "Forbidden", { "content-type": "text/plain; charset=utf-8" });
    return;
  }

  try {
    const file = await readFile(filePath);
    send(res, 200, file, {
      "content-type": contentTypes[extname(filePath)] || "application/octet-stream"
    });
  } catch {
    const index = await readFile(join(publicDir, "index.html"));
    send(res, 200, index, { "content-type": contentTypes[".html"] });
  }
}

const server = createServer((req, res) => {
  if (req.url?.startsWith("/api")) {
    void proxyApi(req, res);
    return;
  }

  void serveStatic(req, res);
});

// WebSocket proxy: upgrade /api/ws → backend /ws
server.on("upgrade", (req, socket, head) => {
  if (!req.url?.startsWith("/api/ws")) {
    socket.destroy();
    return;
  }

  const backendWsUrl = new URL("/ws", wsBackendUrl);
  const targetPort = Number(backendWsUrl.port) || 80;
  const targetHost = backendWsUrl.hostname;

  const upstream = new Socket();

  upstream.on("error", (err) => {
    console.error("WS proxy upstream error:", err.message);
    socket.destroy();
  });

  socket.on("error", (err) => {
    console.error("WS proxy client error:", err.message);
    upstream.destroy();
  });

  upstream.connect(targetPort, targetHost, () => {
    // Forward the original HTTP upgrade request to backend
    const path = "/ws";
    const headers = { ...req.headers };
    headers.host = `${targetHost}:${targetPort}`;

    let upgradeRequest = `${req.method} ${path} HTTP/${req.httpVersion}\r\n`;
    for (const [key, value] of Object.entries(headers)) {
      if (value !== undefined) {
        upgradeRequest += `${key}: ${value}\r\n`;
      }
    }
    upgradeRequest += "\r\n";

    upstream.write(upgradeRequest);
    if (head.length > 0) {
      upstream.write(head);
    }

    // Pipe data bidirectionally
    upstream.pipe(socket);
    socket.pipe(upstream);
  });
});

server.listen(port, "0.0.0.0", () => {
  console.log(`Frontend: http://localhost:${port}`);
  console.log(`API proxy: /api -> ${backendUrl}`);
  console.log(`WS proxy: /api/ws -> ${wsBackendUrl}/ws`);
});
