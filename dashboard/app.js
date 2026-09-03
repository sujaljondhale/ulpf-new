document.addEventListener('DOMContentLoaded', () => {
  const btnProcess = document.getElementById('btn-process');
  const btnDetectOnly = document.getElementById('btn-detect-only');
  const rawInput = document.getElementById('raw-input');
  const resultBox = document.getElementById('result-box');
  const codeUlpf = document.getElementById('code-ulpf');
  const codeOcsf = document.getElementById('code-ocsf');
  const codeEcs = document.getElementById('code-ecs');
  const provTbody = document.getElementById('prov-tbody');
  const provHashBox = document.getElementById('prov-hash-box');

  const badgeFormat = document.getElementById('badge-format');
  const badgeConfidence = document.getElementById('badge-confidence');
  const badgeStatus = document.getElementById('badge-status');

  // Stats
  const statTotal = document.getElementById('stat-total');
  let eventCounter = 1284920;

  // Tabs
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.tab).classList.add('active');
    });
  });

  // Simulator Buttons (Infrastructure Generator)
  document.getElementById('btn-sim-web')?.addEventListener('click', () => {
    const ips = ['192.168.1.102', '10.0.5.21', '172.16.0.88', '192.168.10.45'];
    const randomIp = ips[Math.floor(Math.random() * ips.length)];
    const timeNow = new Date().toISOString();
    rawInput.value = `<134>1 ${timeNow} webstore-fe-01 nginx 4092 - - 127.0.0.1 - - [${new Date().toUTCString()}] "POST /api/v1/checkout HTTP/1.1" 200 4520 "https://mystore.com/cart" "Mozilla/5.0" client_ip="${randomIp}" status=200 response_time_ms=42`;
  });

  document.getElementById('btn-sim-fw')?.addEventListener('click', () => {
    const srcIp = `10.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254 + 1)}`;
    rawInput.value = `CEF:0|CheckPoint|VPN-1 & FireWall-1|R80.10|1000|Accept Connection|Low|src=${srcIp} dst=8.8.8.8 spt=${Math.floor(Math.random()*45000+1024)} dpt=443 proto=tcp act=allow shost=fw-perimeter-01`;
  });

  document.getElementById('btn-sim-waf')?.addEventListener('click', () => {
    const srcIp = `185.220.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254 + 1)}`;
    const timeNow = new Date().toISOString();
    rawInput.value = JSON.stringify({
      timestamp: timeNow,
      rule_id: "WAF_SQLi_Rule_942100",
      action: "BLOCK",
      client_ip: srcIp,
      dest_ip: "10.0.1.100",
      dest_port: 443,
      protocol: "https",
      uri: "/login?user=admin'OR'1'='1",
      user_agent: "sqlmap/1.6#stable",
      vendor: "AWS WAF Engine"
    }, null, 2);
  });

  document.getElementById('btn-sim-vpn')?.addEventListener('click', () => {
    const srcIp = `172.16.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 254 + 1)}`;
    rawInput.value = `LEEF:2.0|IBM|QRadar|7.3|VPN_LOGIN|^\tsrc=${srcIp}\tdst=10.0.0.5\tspt=54122\tdpt=1194\tproto=udp\tact=SUCCESS\tusr=alex.dev`;
  });

  document.getElementById('btn-sim-unknown')?.addEventListener('click', () => {
    const srcIp = `192.168.4.${Math.floor(Math.random() * 250 + 1)}`;
    rawInput.value = `device=BespokeGuard_V4 node=rack-09 src_ip=${srcIp} dst_ip=4.2.2.2 sport=${Math.floor(Math.random()*50000+1024)} dport=53 verdict=DROP policy_id=9881`;
  });

  // Preset Chips
  document.getElementById('btn-sample-cef')?.addEventListener('click', () => {
    rawInput.value = 'CEF:0|CheckPoint|VPN-1 & FireWall-1|R80.10|1000|Accept Connection|Low|src=10.10.1.5 dst=8.8.8.8 spt=51522 dpt=443 proto=tcp act=allow shost=fw-edge-01';
  });
  document.getElementById('btn-sample-leef')?.addEventListener('click', () => {
    rawInput.value = 'LEEF:2.0|Imperva|SecureSphere|4.0|HTTP_Alert|^\tsrc=192.168.1.50\tdst=10.0.0.10\tspt=54122\tdpt=80\tproto=tcp\tact=deny';
  });
  document.getElementById('btn-sample-syslog')?.addEventListener('click', () => {
    rawInput.value = '<134>Jan 10 14:32:01 edge-router-01 firewall[1234]: src=172.16.0.50 dst=10.0.0.1 spt=80 dpt=12345 action=drop proto=tcp';
  });
  document.getElementById('btn-sample-json')?.addEventListener('click', () => {
    rawInput.value = '{"timestamp": "2026-09-02T12:00:00Z", "source_ip": "10.0.0.55", "source_port": 60000, "dest_ip": "8.8.4.4", "dest_port": 53, "protocol": "udp", "action": "allow", "vendor": "AWS WAF"}';
  });
  document.getElementById('btn-sample-kv')?.addEventListener('click', () => {
    rawInput.value = 'src=192.168.1.10 dst=8.8.8.8 spt=45210 dpt=53 action=allow proto=udp vendor="SonicWall" rule="Rule-Perimeter-12"';
  });
  document.getElementById('btn-sample-csv')?.addEventListener('click', () => {
    rawInput.value = '2026-09-03T18:00:00Z,10.0.1.5,51234,8.8.8.8,443,tcp,allow,PaloAlto';
  });
  document.getElementById('btn-sample-xml')?.addEventListener('click', () => {
    rawInput.value = '<Event><System><TimeCreated SystemTime="2026-09-03T18:00:00Z"/><Provider Name="CiscoASA"/></System><EventData><Data Name="src">10.0.0.2</Data><Data Name="dst">1.1.1.1</Data><Data Name="spt">60001</Data><Data Name="dpt">80</Data><Data Name="action">block</Data></EventData></Event>';
  });

  // Detect Only Endpoint
  btnDetectOnly?.addEventListener('click', async () => {
    const logText = rawInput.value.trim();
    if (!logText) return;

    btnDetectOnly.innerText = 'Detecting...';
    try {
      const resp = await fetch('/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ log: logText }),
      });
      const data = await resp.json();
      alert(`Format Detected: ${data.format}\nConfidence Score: ${data.confidence}\nReason: ${data.reason}`);
    } catch (e) {
      alert('Error during format detection: ' + e.message);
    } finally {
      btnDetectOnly.innerText = '🔍 Format Detect Only';
    }
  });

  // Process Endpoint (Full Pipeline)
  btnProcess.addEventListener('click', async () => {
    const logText = rawInput.value.trim();
    if (!logText) return;

    btnProcess.innerText = '⚡ Processing Pipeline...';
    try {
      const resp = await fetch('/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ log: logText }),
      });
      const data = await resp.json();

      // Increment stats counter dynamically for demo effect
      eventCounter += 1;
      statTotal.innerText = eventCounter.toLocaleString();

      badgeFormat.innerText = `Format: ${data.detection.format}`;
      badgeConfidence.innerText = `Confidence: ${data.detection.confidence}`;
      badgeStatus.innerText = `Status: ${data.status.toUpperCase()}`;

      codeUlpf.textContent = JSON.stringify(data.canonical_event, null, 2);
      codeOcsf.textContent = JSON.stringify(data.ocsf_export, null, 2);
      codeEcs.textContent = JSON.stringify(data.ecs_export, null, 2);

      // Provenance Table Render
      provTbody.innerHTML = '';
      if (data.provenance && Object.keys(data.provenance).length > 0) {
        for (const [canonField, prov] of Object.entries(data.provenance)) {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td class="canon-key">${canonField}</td>
            <td class="orig-key">${prov.original_field}</td>
            <td class="val-col">"${prov.value}"</td>
            <td><span style="color:#94a3b8;">${prov.parser}</span> <span style="color:#64748b;">(${prov.rule})</span></td>
            <td><span style="color:#34d399;">${prov.confidence}</span></td>
          `;
          provTbody.appendChild(tr);
        }
      } else {
        provTbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#94a3b8;">No canonical fields mapped (Unparsed / Plaintext Fallback)</td></tr>';
      }

      provHashBox.innerHTML = `🔒 <strong>SHA-256 Raw Log Hash Integrity:</strong> <code>${data.raw_hash}</code>`;
      resultBox.style.display = 'block';
    } catch (e) {
      alert('Error connecting to ULPF API endpoint: ' + e.message);
    } finally {
      btnProcess.innerText = '⚡ Process Log (Full Pipeline)';
    }
  });

  // AI Onboarding Studio
  const btnAnalyzeAi = document.getElementById('btn-analyze-ai');
  const sampleUnparsed = document.getElementById('sample-unparsed');
  const aiResultsBox = document.getElementById('ai-results-box');
  const codeYamlSpec = document.getElementById('code-yaml-spec');
  const btnGenerateParser = document.getElementById('btn-generate-parser');
  const btnApproveParser = document.getElementById('btn-approve-parser');
  const aiStatusMsg = document.getElementById('ai-status-msg');

  let currentYamlSpec = '';
  let compiledParserId = '';

  btnAnalyzeAi.addEventListener('click', async () => {
    const text = sampleUnparsed.value.trim();
    if (!text) return;

    btnAnalyzeAi.innerText = '✨ Analyzing with Ollama Local SLM...';
    try {
      const resp = await fetch('/onboarding/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sample_logs: text.split('\n').filter(l => l.trim().length > 0) }),
      });
      const data = await resp.json();
      currentYamlSpec = data.yaml_spec;
      codeYamlSpec.textContent = currentYamlSpec;
      aiResultsBox.style.display = 'block';
      btnApproveParser.style.display = 'none';
      aiStatusMsg.innerText = `Analyzed by Local AI SLM. Calculated pattern confidence: ${data.confidence}`;
    } catch (e) {
      alert('Error during AI analysis: ' + e.message);
    } finally {
      btnAnalyzeAi.innerText = '✨ Analyze Unknown Format with Local AI Engine';
    }
  });

  btnGenerateParser.addEventListener('click', async () => {
    try {
      const resp = await fetch('/onboarding/generate-parser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ yaml_spec: currentYamlSpec }),
      });
      const data = await resp.json();
      compiledParserId = data.spec.id;
      aiStatusMsg.innerText = `Parser '${compiledParserId}' compiled into executable bytecode! Status: DRAFT`;
      btnApproveParser.style.display = 'inline-block';
    } catch (e) {
      alert('Compilation error: ' + e.message);
    }
  });

  btnApproveParser.addEventListener('click', async () => {
    try {
      const resp = await fetch('/onboarding/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parser_id: compiledParserId }),
      });
      const data = await resp.json();
      aiStatusMsg.innerText = `🎉 Parser '${compiledParserId}' APPROVED and promoted to ACTIVE in production parser registry!`;
    } catch (e) {
      alert('Approval error: ' + e.message);
    }
  });
});
