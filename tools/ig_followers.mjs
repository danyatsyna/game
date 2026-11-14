// Daily job: reads followers_count from the Instagram API and appends it to data/followers.json
import fs from 'node:fs';
const token = process.env.IG_TOKEN;
if (!token) { console.error('IG_TOKEN is empty'); process.exit(1); }
const r = await fetch(`https://graph.instagram.com/me?fields=followers_count,username&access_token=${token}`);
const j = await r.json();
if (!r.ok || typeof j.followers_count !== 'number') { console.error('Instagram API error:', JSON.stringify(j)); process.exit(1); }
const file = 'data/followers.json';
const arr = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : [];
// Kyiv date, so the day matches the app
const date = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Kyiv' }).format(new Date());
const i = arr.findIndex(x => x.date === date);
if (i >= 0) arr[i].count = j.followers_count; else arr.push({ date, count: j.followers_count });
arr.sort((a, b) => a.date < b.date ? -1 : 1);
fs.writeFileSync(file, JSON.stringify(arr, null, 1) + '\n');
console.log(`@${j.username}: ${j.followers_count} on ${date}`);
// keep the long-lived token alive (resets its 60-day expiry); failure here is not fatal
try {
  const rr = await fetch(`https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${token}`);
  console.log('token refresh:', rr.status);
} catch (e) { console.log('token refresh skipped'); }
