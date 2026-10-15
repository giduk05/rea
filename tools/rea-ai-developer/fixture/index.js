import { normalize, countWords } from './passage.js';
export function processPassage(text) { const clean = normalize(text); return { clean, words: countWords(clean) }; }
