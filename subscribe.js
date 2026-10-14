document.querySelectorAll("form.vp-subscribe").forEach(f => f.addEventListener("submit", async e => {
  e.preventDefault();
  const msg = f.querySelector(".sub-msg"), btn = f.querySelector("button");
  btn.disabled = true; msg.textContent = "Subscribing…"; msg.style.color = "";
  try {
    const r = await fetch("/api/subscribe", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: f.email.value, website: f.website.value }) });
    const d = await r.json();
    msg.textContent = d.ok ? d.message : d.error; msg.style.color = d.ok ? "#3fb950" : "#f85149";
    if (d.ok) f.reset();
  } catch { msg.textContent = "Signup failed. Please try again."; msg.style.color = "#f85149"; }
  btn.disabled = false;
}));
