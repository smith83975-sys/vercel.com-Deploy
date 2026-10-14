// Newsletter signup -> MailerLite. Token comes only from env MAILERLITE_API_KEY.
const GROUP_ID = process.env.MAILERLITE_GROUP_ID || "201346253191120872";
const EMAIL_RE = /^[^\s@]{1,64}@[^\s@]{1,255}\.[a-z]{2,}$/i;
const hits = new Map(); // best-effort per-instance rate limit
module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.statusCode = 405; return res.end(JSON.stringify({ ok: false, error: "Use POST" })); }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  const now = Date.now(), list = (hits.get(ip) || []).filter(t => now - t < 60000);
  if (list.length >= 5) { res.statusCode = 429; return res.end(JSON.stringify({ ok: false, error: "Too many tries. Please wait a minute." })); }
  list.push(now); hits.set(ip, list);
  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};
  if (body.website) return res.end(JSON.stringify({ ok: true, message: "You're in!" })); // honeypot
  const email = String(body.email || "").trim().toLowerCase();
  if (!EMAIL_RE.test(email) || email.length > 254) { res.statusCode = 400; return res.end(JSON.stringify({ ok: false, error: "Please enter a valid email address." })); }
  const key = process.env.MAILERLITE_API_KEY;
  if (!key) { res.statusCode = 503; return res.end(JSON.stringify({ ok: false, error: "Signup is temporarily unavailable. Please try again later." })); }
  try {
    const r = await fetch("https://connect.mailerlite.com/api/subscribers", {
      method: "POST",
      headers: { Authorization: "Bearer " + key, "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ email, groups: [GROUP_ID] }),
    });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) { res.statusCode = r.status === 422 ? 400 : 502; return res.end(JSON.stringify({ ok: false, error: r.status === 422 ? "Please enter a valid email address." : "Signup failed. Please try again." })); }
    const pending = d.data && d.data.status === "unconfirmed";
    return res.end(JSON.stringify({ ok: true, message: pending ? "Check your inbox to confirm." : "You're in!" }));
  } catch (e) { res.statusCode = 502; return res.end(JSON.stringify({ ok: false, error: "Signup failed. Please try again." })); }
};
