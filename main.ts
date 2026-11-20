// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is the X post itself: the house reads POST.json from this
// repository, fetches the post from X, and hands its first picture plus
// its text to the judge. This program does nothing but carry POST.json
// from the repository root into the grader's output directory, so the
// gate can read it there. No network, no clock, no files outside the repo.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(botDir, 'POST.json');
const target = join(outDir, 'POST.json');

mkdirSync(outDir, { recursive: true });

let post: string;
try {
  post = readFileSync(source, 'utf8');
} catch (err) {
  console.error(`cannot read ${source}: ${(err as Error).message}`);
  process.exit(1);
}

// The gate wants a JSON object with a url field; fail loudly if it is not.
const parsed: unknown = JSON.parse(post);
if (typeof parsed !== 'object' || parsed === null || !('url' in parsed)) {
  console.error('POST.json must be a JSON object with a "url" field');
  process.exit(1);
}
const url = (parsed as { url: unknown }).url;
if (typeof url !== 'string' || !/^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\//.test(url)) {
  console.error('POST.json "url" must be an X post address (https://x.com/<handle>/status/<id>)');
  process.exit(1);
}

writeFileSync(target, post);
