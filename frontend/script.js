const endpoint = "http://localhost:5050/api/save";

document.getElementById('generate-btn').addEventListener('click', (e) => {
  e.preventDefault();

  const asn = document.getElementById('asn').value.trim();
  const affiliate = document.getElementById('affiliate').value.trim();
  const client = document.getElementById('client').value.trim();

  if (!asn || !affiliate || !client) {
    alert("Please fill in all fields.");
    return;
  }

  console.log("Sending to backend:", { asn, affiliate, client });

  // Send data to backend
  fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ asn, affiliate, client })
  })
    .then(res => res.json())
    .then(data => console.log("✅ Saved to backend:", data))
    .catch(err => {
      console.error("❌ Save error:", err);
      alert("Failed to save");
    });

  // Generate QR code
  const qr = new QRCodeStyling({
    width: 300,
    height: 300,
    data: asn,
    type: "canvas",
    dotsOptions: {
      color: "#000",
      type: "rounded"
    },
    backgroundOptions: {
      color: "#fff"
    }
  });

  const container = document.getElementById("qr-container");
  container.innerHTML = ""; // Clear previous

  // Append with a slight delay to avoid rendering issues
  setTimeout(() => {
    qr.append(container);
    console.log("✅ QR code appended to container");
  }, 0);

  // Store reference globally for download
  window.currentQRCode = qr;
  document.getElementById("download-btn").style.display = "block";
});

document.getElementById('download-btn').addEventListener('click', () => {
  const affiliate = document.getElementById('affiliate').value.trim() || "qr-code";
  const filename = affiliate.replace(/\s+/g, "-").toLowerCase();

  if (window.currentQRCode) {
    window.currentQRCode.download({ name: filename, extension: "png" });
  }
});
