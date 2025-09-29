#!/usr/bin/env node
/**
 * Validate that every public_url in figures_index.json returns HTTP 200.
 * Usage:
 *   node scripts/validate_urls.js
 */
const fs = require('fs');
const https = require('https');

const data = JSON.parse(fs.readFileSync('figures_index.json', 'utf8'));

function check(url) {
  return new Promise(resolve => {
    https.get(url, res => {
      resolve({ url, status: res.statusCode });
      res.resume();
    }).on('error', () => resolve({ url, status: 0 }));
  });
}

(async () => {
  let bad = [];
  for (const rec of data) {
    const { url, status } = await check(rec.public_url);
    if (status !== 200) bad.push({ file: rec.file, url, status });
  }
  if (bad.length) {
    console.error('Bad URLs:', bad);
    process.exit(2);
  } else {
    console.log('All URLs OK');
  }
})();
