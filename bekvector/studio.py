"""
BekVector Live Studio — Zero-Dependency Upnormal Web Playground.
Runs an embedded HTTP server providing an interactive visual workbench for procedural vectors.
"""

import http.server
import socketserver
import json
import urllib.parse
from .core import BekVector
from .dataviz import DataViz
from .svg_animator import generate_animated_weather_svg
from .exporter import to_react_component
from examples.bekbek_duck import create_duck
from examples.cyber_seal import create_seal

STUDIO_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BekVector Studio — Live Procedural Vector Workbench</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-stage: #0A0B0E;
      --surface-card: rgba(18, 21, 29, 0.75);
      --border-hairline: rgba(255, 255, 255, 0.08);
      --text-ink: #EDEDED;
      --text-muted: #8E9AA8;
      --accent-ember: #FA5D29;
      --accent-cyan: #49B3FC;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg-stage);
      color: var(--text-ink);
      font-family: 'Inter Tight', -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }
    header {
      padding: 24px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-hairline);
      backdrop-filter: blur(16px);
      background: rgba(10, 11, 14, 0.8);
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .brand-title {
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      color: var(--accent-ember);
      border: 1px solid rgba(250, 93, 41, 0.3);
      padding: 3px 8px;
      border-radius: 999px;
      letter-spacing: 1.5px;
    }
    main {
      flex: 1;
      padding: 32px;
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 32px;
      max-width: 1440px;
      margin: 0 auto;
      width: 100%;
    }
    @media (max-width: 900px) {
      main { grid-template-columns: 1fr; }
    }
    .panel {
      background: var(--surface-card);
      border: 1px solid var(--border-hairline);
      border-radius: 20px;
      padding: 24px;
      backdrop-filter: blur(20px);
    }
    .panel-title {
      font-size: 13px;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-muted);
      letter-spacing: 1.5px;
      margin-bottom: 20px;
      text-transform: uppercase;
    }
    .nav-btn {
      display: flex;
      align-items: center;
      width: 100%;
      padding: 14px 18px;
      margin-bottom: 10px;
      background: transparent;
      border: 1px solid var(--border-hairline);
      border-radius: 12px;
      color: var(--text-ink);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .nav-btn:hover, .nav-btn.active {
      background: rgba(255, 255, 255, 0.05);
      border-color: var(--accent-ember);
      color: #FFF;
      transform: translateX(4px);
    }
    .nav-btn.active {
      border-color: var(--accent-ember);
      box-shadow: 0 0 16px rgba(250, 93, 41, 0.15);
    }
    .viewport {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 520px;
      background: radial-gradient(circle at center, rgba(30, 35, 48, 0.4) 0%, rgba(10, 11, 14, 0.95) 75%);
      border: 1px solid var(--border-hairline);
      border-radius: 24px;
      position: relative;
      overflow: hidden;
      padding: 40px;
    }
    .canvas-container {
      max-width: 100%;
      max-height: 480px;
      display: flex;
      align-items: center;
      justify-content: center;
      filter: drop-shadow(0 20px 40px rgba(0,0,0,0.6));
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .canvas-container svg {
      max-width: 100%;
      height: auto;
    }
    .actions-bar {
      margin-top: 24px;
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    .action-btn {
      padding: 10px 20px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
      cursor: pointer;
      transition: all 0.2s ease;
      background: #1A1D27;
      color: var(--text-ink);
      border: 1px solid var(--border-hairline);
    }
    .action-btn:hover {
      background: #252A38;
      border-color: var(--accent-cyan);
    }
    .action-btn.primary {
      background: var(--accent-ember);
      border-color: var(--accent-ember);
      color: #FFF;
    }
    .action-btn.primary:hover {
      background: #FF6E3D;
    }
  </style>
</head>
<body>
  <header>
    <div class="brand-title">
      <span>🦆 BEKVECTOR STUDIO</span>
      <span class="badge">PROD V1.0</span>
    </div>
    <div style="font-family: 'JetBrains Mono'; font-size: 11px; color: var(--text-muted);">
      DEVELOPED BY BAGAS CIHUY
    </div>
  </header>

  <main>
    <aside class="panel">
      <div class="panel-title">Asset Catalog</div>
      <button class="nav-btn active" onclick="loadAsset('duck')">🐥 Bekbek Mascot Duck</button>
      <button class="nav-btn" onclick="loadAsset('seal')">🛡️ Cybernetic System Seal</button>
      <button class="nav-btn" onclick="loadAsset('sky')">🌌 Procedural Animated Sky (SVG)</button>
      <button class="nav-btn" onclick="loadAsset('sparkline')">📈 Telemetry Sparkline Chart</button>
      <button class="nav-btn" onclick="loadAsset('radar')">🎯 Polar Spider Radar Chart</button>
    </aside>

    <section class="panel" style="display: flex; flex-direction: column;">
      <div class="panel-title">Live Vector Canvas Viewport</div>
      <div class="viewport">
        <div id="canvas-target" class="canvas-container">Loading vector...</div>
      </div>
      <div class="actions-bar">
        <button class="action-btn primary" onclick="downloadSVG()">Download .SVG</button>
        <button class="action-btn" onclick="copyReact()">Copy React (.jsx)</button>
      </div>
    </section>
  </main>

  <script>
    let currentSvg = '';
    let currentName = 'bekbek_duck';

    async function loadAsset(type) {
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      currentName = type;

      const res = await fetch('/api/asset?type=' + type);
      const data = await res.json();
      currentSvg = data.svg;
      document.getElementById('canvas-target').innerHTML = currentSvg;
    }

    function downloadSVG() {
      const blob = new Blob([currentSvg], { type: 'image/svg+xml' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = currentName + '.svg';
      a.click();
      URL.revokeObjectURL(url);
    }

    async function copyReact() {
      const res = await fetch('/api/react?type=' + currentName);
      const data = await res.json();
      navigator.clipboard.writeText(data.jsx);
      alert('React JSX Component copied to clipboard!');
    }

    // Initial load
    loadAsset('duck');
  </script>
</body>
</html>
"""

class StudioHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(STUDIO_HTML.encode("utf-8"))
        elif url.path == "/api/asset":
            qs = urllib.parse.parse_qs(url.query)
            asset_type = qs.get("type", ["duck"])[0]
            svg = self.get_svg_for_type(asset_type)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"svg": svg}).encode("utf-8"))
        elif url.path == "/api/react":
            qs = urllib.parse.parse_qs(url.query)
            asset_type = qs.get("type", ["duck"])[0]
            svg = self.get_svg_for_type(asset_type)
            jsx = to_react_component(svg, component_name=asset_type.capitalize() + "Vector")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"jsx": jsx}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def get_svg_for_type(self, asset_type):
        if asset_type == "duck":
            return create_duck().to_svg(bg="#0B0D13")
        elif asset_type == "seal":
            return create_seal().to_svg(bg="#0A0B0E")
        elif asset_type == "sky":
            return generate_animated_weather_svg("night_sky", 480, 280)
        elif asset_type == "sparkline":
            return DataViz.sparkline([12, 19, 15, 28, 35, 42, 38, 55, 68, 74], width=360, height=120)
        elif asset_type == "radar":
            return DataViz.radar_chart({"CPU": 45, "RAM": 44, "DISK": 70, "NET": 85, "ACC": 98}, radius=80)
        return create_duck().to_svg()

    def log_message(self, format, *args):
        # Silence console log noise
        pass

def run_studio(port: int = 3095):
    """Starts the BekVector Studio server."""
    with socketserver.TCPServer(("0.0.0.0", port), StudioHandler) as httpd:
        print(f"🦆 BekVector Live Studio running at http://127.0.0.1:{port}")
        httpd.serve_forever()
