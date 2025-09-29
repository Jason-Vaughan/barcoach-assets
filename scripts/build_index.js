#!/usr/bin/env node
/**
 * Build figures_index.json from /images and optional /data/metadata.csv
 * Usage examples:
 *   node scripts/build_index.js --base https://<user>.github.io/barcoach-assets
 *   node scripts/build_index.js --base https://<cdn>/barcoach --csv data/metadata.csv
 */
const fs = require('fs');
const path = require('path');

function parseCSV(csv) {
  const lines = csv.trim().split(/\r?\n/);
  const header = lines.shift();
  const cols = header.split(',').map(s => s.trim());
  return lines.map(line => {
    const vals = line.split(',').map(s => s.trim());
    const obj = {};
    cols.forEach((c, i) => obj[c] = vals[i] || '');
    if (obj.keywords) obj.keywords = obj.keywords.split('|').map(s => s.trim()).filter(Boolean);
    return obj;
  });
}

function main() {
  const args = process.argv.slice(2);
  const baseIdx = args.indexOf('--base');
  if (baseIdx === -1) {
    console.error('ERROR: missing --base https://<host>/<repo>');
    process.exit(1);
  }
  const base = args[baseIdx + 1].replace(/\/+$/, '');

  const csvIdx = args.indexOf('--csv');
  const csvPath = csvIdx !== -1 ? args[csvIdx + 1] : null;

  const imagesDir = path.join(process.cwd(), 'images');
  if (!fs.existsSync(imagesDir)) {
    console.error('ERROR: images/ directory not found');
    process.exit(1);
  }

  // Optional metadata
  let metaByFile = new Map();
  if (csvPath && fs.existsSync(csvPath)) {
    const csv = fs.readFileSync(csvPath, 'utf8');
    for (const row of parseCSV(csv)) metaByFile.set(row.file, row);
  }

  const files = fs.readdirSync(imagesDir)
    .filter(f => /\.(png|jpe?g|webp|gif|svg)$/i.test(f))
    .sort();

  const out = files.map(file => {
    const m = metaByFile.get(file) || {};
    return {
      file,
      figure_label: m.figure_label || '',
      caption: m.caption || '',
      section_title: m.section_title || '',
      source_html: m.source_html || '',
      keywords: Array.isArray(m.keywords) ? m.keywords : [],
      rev: m.rev || 'Devices Guide Rev14',
      public_url: `${base}/images/${encodeURIComponent(file)}`
    };
  });

  fs.writeFileSync('figures_index.json', JSON.stringify(out, null, 2));
  console.log(`Wrote figures_index.json with ${out.length} entries.`);
}

main();
