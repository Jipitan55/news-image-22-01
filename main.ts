// news-image-22-01: copy the pre-rendered entry image to the output path.
// The image (entry.png) is drawn by draw.py and committed in this repo;
// this program only copies it, so both runs write identical bytes.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// An empty MAKEFUN_OUTPUT_DIR must not silently mean "current directory".
const rawOut = process.env.MAKEFUN_OUTPUT_DIR;
const outDir = rawOut && rawOut.trim() !== "" ? rawOut : "/output";
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);

// Fail loudly instead of silently leaving a partial or missing file.
if (statSync(dest).size !== statSync(src).size) {
  throw new Error(`entry.png copy incomplete: ${dest}`);
}
