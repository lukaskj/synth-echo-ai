import { $ } from "bun";
import { existsSync } from "node:fs";

const baseDir = "apps/backend";

const python = existsSync(`${baseDir}/.venv/Scripts/python.exe`)
  ? ".venv/Scripts/python.exe"
  : existsSync(`${baseDir}/.venv/bin/python`)
    ? ".venv/bin/python"
    : null;

if (!python) {
  throw new Error("Python executable not found in virtual environment.");
}

await $`${python} app.py`.cwd(baseDir);
