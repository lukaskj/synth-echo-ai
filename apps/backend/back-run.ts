import {$} from "bun";

// await $`apps/backend/.venv/Scripts/python.exe apps/backend/app.py || apps/backend/.venv/bin/python apps/backend/app.py`

console.log(process.cwd())

$.cwd("apps/backend/");

await $`.venv/Scripts/python.exe app.py || .venv/bin/python app.py`;
// const proc = Bun.spawn(
//   ["apps/backend/.venv/bin/python", "apps/backend/app.py", "||", "apps/backend/.venv/Scripts/python.exe", "apps/backend/app.py"],
//   {
//     stdio: ["inherit", "inherit", "inherit"],
//   },
// );

// await proc.exited;
