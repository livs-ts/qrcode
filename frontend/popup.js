const endpoint = "https://qr-code-api-priq.onrender.com/api/save";

document.getElementById('generate-btn').addEventListener('click', (e) => {
  e.preventDefault();

  const asn = document.getElementById('asn').value.trim();
  if (!asn) {
    alert("Please enter the ASN link.");
    return;
  }

  const { clientShortName, affiliateShortName } = extractNamesFromASNUrl(asn);

  if (!clientShortName || !affiliateShortName) {
    alert("Failed to extract affiliate or client from the ASN link.");
    return;
  }

  console.log("Sending to backend:", { asn, affiliate: affiliateShortName, client: clientShortName });

  fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ asn, affiliate: affiliateShortName, client: clientShortName })
  })
    .then(res => res.json())
    .then(data => console.log("✅ Saved to backend:", data))
    .catch(err => {
      console.error("❌ Save error:", err);
      alert("Failed to save");
    });

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
  container.innerHTML = "";
  setTimeout(() => {
    qr.append(container);
    console.log("✅ QR code appended to container");
  
    window.currentQRCode = qr;
    window.lastFileName = affiliateShortName.replace(/\s+/g, "-").toLowerCase();
    document.getElementById("download-btn").style.display = "block"; // Show after QR is loaded
    
    document.getElementById('asn').value = ""; // ✅ Clear the input

    document.getElementById('asn').focus();
  }, 0);
});

document.getElementById('download-btn').addEventListener('click', () => {
  if (window.currentQRCode) {
    const filename = window.lastFileName || "qr-code";
    window.currentQRCode.download({ name: filename, extension: "png" });

    const successMsg = document.getElementById('success-message');
    successMsg.style.display = "block";

    setTimeout(() => {
      successMsg.style.display = "none";
    }, 3000); // hide after 3 seconds
    
    const asn = document.getElementById('asn').value.trim();
  }
});


function extractNamesFromASNUrl(url) {
  try {
    const parsedUrl = new URL(url);
    const pathSegments = parsedUrl.pathname.split('/');
    const clientShortName = pathSegments[3]; // /embeds/book/{client}/...
    const affiliateShortName = parsedUrl.searchParams.get('asn'); // full value like 'charischang-gbp'
    return { clientShortName, affiliateShortName };
  } catch (e) {
    console.error('Invalid URL format', e);
    return { clientShortName: null, affiliateShortName: null };
  }
}

