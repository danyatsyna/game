// Reads recent Instagram videos (Reels) and merges them into data/videos.json.
// The app adds every new entry to the current season's video count.
import fs from 'node:fs';
const token = process.env.IG_TOKEN;
if (!token) { console.error('IG_TOKEN is empty'); process.exit(1); }
const uid = process.env.IG_USER_ID;
const fields = 'id,caption,media_type,media_product_type,timestamp,permalink';
const base = uid ? `https://graph.facebook.com/v21.0/${uid}/media` : 'https://graph.instagram.com/me/media';
const r = await fetch(`${base}?fields=${fields}&limit=50&access_token=${token}`);
const j = await r.json();
if (!r.ok || !Array.isArray(j.data)) { console.error('Instagram API error:', JSON.stringify(j)); process.exit(1); }

// What counts as a "video" for the rank: Reels and other video posts.
// Photos and carousels are skipped. Change this line to count something else.
const counts = m => m.media_type === 'VIDEO';

const kyiv = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Kyiv' });
const file = 'data/videos.json';
const arr = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : [];
let added = 0;
for (const m of j.data.filter(counts)) {
  const date = kyiv.format(new Date(m.timestamp));
  const title = (m.caption || '').split('\n')[0].trim().slice(0, 80);
  const i = arr.findIndex(x => x.id === m.id);
  const rec = { id: m.id, date, title, url: m.permalink };
  if (i >= 0) arr[i] = rec; else { arr.push(rec); added++; }
}
arr.sort((a, b) => a.date < b.date ? -1 : a.date > b.date ? 1 : 0);
fs.writeFileSync(file, JSON.stringify(arr, null, 1) + '\n');
console.log(`videos: ${j.data.length} posts checked, ${added} new, ${arr.length} in file`);
