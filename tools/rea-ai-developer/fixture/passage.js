export function normalize(t) { return String(t ?? '').replace(/\s+/g,' ').trim(); }
export function countWords(t) { return t.trim() ? t.trim().split(/\s+/).length : 0; }
