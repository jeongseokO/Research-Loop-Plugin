#!/usr/bin/env node
// Copies the code lines a report_implementation call points at, exactly as git holds them, so an
// AI never retypes code from memory. Read-only: it runs git show, diff and ls-files, nothing else.
//
//   node code-excerpt.mjs [--repo DIR] [--base COMMIT] [--head COMMIT] FILE:LINE[:START-END] ...
//
// Prints JSON: "code" for the report (repository, the commits before and after, every changed file
// with its line counts) and one location per FILE:LINE, ready for an intent's or an unrequested
// change's "location". Uncommitted changes report head "working-tree".
import { execFileSync } from 'node:child_process';
import { readFileSync, realpathSync } from 'node:fs';
import { basename, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

class ExcerptError extends Error {}
const LIMITS = { lines: 12, chars: 2400, removed: 6, removedChars: 300 };

function git(cwd, args) {
  try { return execFileSync('git', args, { cwd, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'pipe'] }); }
  catch (error) { throw new ExcerptError(`git ${args[0]} failed: ${String(error.stderr || error.message).trim().split('\n')[0]}`); }
}

/** The repository's name as a reader recognizes it: github.com/owner/name, or its folder. */
export function repositoryName(remote, folder) {
  const url = (remote ?? '').trim();
  const ssh = /^[\w.-]+@([\w.-]+):(.+?)(?:\.git)?\/?$/.exec(url);
  if (ssh) return `${ssh[1]}/${ssh[2]}`;
  try {
    const parsed = new URL(url);
    if (['https:', 'http:', 'ssh:', 'git:'].includes(parsed.protocol) && parsed.hostname) {
      return `${parsed.hostname}${parsed.pathname.replace(/\.git\/?$/, '').replace(/\/$/, '')}`;
    }
  } catch { /* not a URL: use the folder */ }
  return basename(folder);
}

/** Parses `git diff -U0` for one file: added head lines and removed lines placed before a head line. */
export function diffLines(diff) {
  const added = new Set(); const removed = [];
  let at = 0; let next = 0; let inHunk = false;
  for (const line of diff.split('\n')) {
    const hunk = /^@@ -\d+(?:,(\d+))? \+(\d+)(?:,(\d+))? @@/.exec(line);
    if (hunk) {
      const count = hunk[3] === undefined ? 1 : Number(hunk[3]);
      next = Number(hunk[2]);
      // Removed lines stand where the hunk's head lines begin, or after its line when it only removed.
      at = count > 0 ? next : next + 1;
      inHunk = true;
      continue;
    }
    if (!inHunk) continue;
    if (line.startsWith('+')) added.add(next++);
    else if (line.startsWith('-')) removed.push({ at, text: line.slice(1) });
  }
  return { added, removed };
}

/** Lines start..end around a marked line: at most 12, the mark kept inside, wider where the file allows. */
export function window(mark, total, start, end) {
  if (start !== undefined) {
    if (!(start <= mark && mark <= end && end - start + 1 <= LIMITS.lines && start >= 1 && end <= total)) {
      throw new ExcerptError(`Lines ${start}-${end} must hold line ${mark}, lie inside the file (${total} lines) and span at most ${LIMITS.lines}.`);
    }
    return [start, end];
  }
  let first = Math.max(1, mark - 5); let last = Math.min(total, first + LIMITS.lines - 1);
  first = Math.max(1, last - LIMITS.lines + 1);
  return [first, last];
}

function parseTarget(argument) {
  const match = /^(.+?):(\d+)(?::(\d+)-(\d+))?$/.exec(argument);
  if (!match) throw new ExcerptError(`"${argument}" is not FILE:LINE or FILE:LINE:START-END.`);
  const file = match[1].replace(/^\.\//, '');
  if (file.startsWith('/') || file.split('/').includes('..')) throw new ExcerptError(`"${file}" must be a path inside the repository.`);
  return { file, mark: Number(match[2]), start: match[3] ? Number(match[3]) : undefined, end: match[4] ? Number(match[4]) : undefined, key: argument };
}

export function excerpt({ repo = '.', base, head, targets }) {
  const root = git(resolve(repo), ['rev-parse', '--show-toplevel']).trim();
  const dirty = git(root, ['status', '--porcelain', '--untracked-files=all']).trim() !== '';
  const workingTree = head === undefined ? dirty : head === 'working-tree';
  const headRef = workingTree ? 'working-tree' : git(root, ['rev-parse', '--short=12', head ?? 'HEAD']).trim();
  const baseRef = git(root, ['rev-parse', '--short=12', base ?? (workingTree ? 'HEAD' : `${headRef}~1`)]).trim();
  const range = workingTree ? [baseRef] : [baseRef, headRef];
  const untracked = workingTree ? git(root, ['ls-files', '--others', '--exclude-standard']).split('\n').filter(Boolean) : [];
  const read = (file) => workingTree ? readFileSync(resolve(root, file), 'utf8') : git(root, ['show', `${headRef}:${file}`]);
  const files = git(root, ['diff', '--numstat', '--no-renames', ...range]).split('\n').filter(Boolean).map((line) => {
    const [added, removed, ...path] = line.split('\t');
    return { path: path.join('\t'), added: Number(added) || 0, removed: Number(removed) || 0 };
  });
  for (const file of untracked) files.push({ path: file, added: read(file).split('\n').length - (read(file).endsWith('\n') ? 1 : 0), removed: 0 });
  let remote = '';
  try { remote = git(root, ['remote', 'get-url', 'origin']); } catch { /* no remote */ }

  const locations = {};
  for (const target of targets.map(parseTarget)) {
    let text;
    try { text = read(target.file); } catch { throw new ExcerptError(`${target.file} is not in ${headRef === 'working-tree' ? 'the working tree' : headRef}.`); }
    const all = text.replace(/\r\n?/g, '\n').replace(/\n$/, '').split('\n');
    if (target.mark < 1 || target.mark > all.length) throw new ExcerptError(`${target.file} has ${all.length} lines; line ${target.mark} is not one of them.`);
    let [start, end] = window(target.mark, all.length, target.start, target.end);
    // Long lines: narrow around the mark until the excerpt fits.
    while (all.slice(start - 1, end).join('\n').length > LIMITS.chars && end > start) {
      if (target.mark - start >= end - target.mark) start++; else end--;
    }
    const body = all.slice(start - 1, end).join('\n');
    if (body.length > LIMITS.chars) throw new ExcerptError(`${target.file}:${target.mark} is longer than ${LIMITS.chars} characters on its own.`);
    const diff = untracked.includes(target.file)
      ? { added: new Set(all.map((_, index) => index + 1)), removed: [] }
      : diffLines(git(root, ['diff', '-U0', '--no-renames', ...range, '--', target.file]));
    const added = [...diff.added].filter((line) => line >= start && line <= end).sort((a, b) => a - b);
    const removed = diff.removed.filter((line) => line.at >= start && line.at <= end + 1).slice(0, LIMITS.removed)
      .map((line) => ({ at: line.at, text: line.text.length > LIMITS.removedChars ? `${line.text.slice(0, LIMITS.removedChars - 1)}…` : line.text }));
    locations[target.key] = { file: target.file, start, end, mark: target.mark, excerpt: body,
      ...(added.length ? { added } : {}), ...(removed.length ? { removed } : {}) };
  }
  return { code: { repo: repositoryName(remote, root), base: baseRef, head: headRef, files }, locations };
}

function main(args) {
  const options = { targets: [] };
  for (let index = 0; index < args.length; index++) {
    const flag = args[index];
    if (['--repo', '--base', '--head'].includes(flag)) {
      if (!args[index + 1]) throw new ExcerptError(`${flag} needs a value.`);
      options[flag.slice(2)] = args[++index];
    } else options.targets.push(flag);
  }
  if (!options.targets.length) throw new ExcerptError('Usage: node code-excerpt.mjs [--repo DIR] [--base COMMIT] [--head COMMIT] FILE:LINE[:START-END] ...');
  process.stdout.write(`${JSON.stringify(excerpt(options), null, 1)}\n`);
}

// Compared as real paths: started through a symlinked plugin folder, or with another case on a
// case-insensitive disk, the helper must still run rather than exit 0 having done nothing.
const realPath = (file) => { try { return realpathSync.native(file); } catch { return resolve(file); } };
function startedDirectly() {
  if (!process.argv[1]) return false;
  const started = realPath(resolve(process.argv[1])), self = realPath(fileURLToPath(import.meta.url));
  return started === self || ((process.platform === 'darwin' || process.platform === 'win32') && started.toLowerCase() === self.toLowerCase());
}

if (startedDirectly()) {
  try { main(process.argv.slice(2)); }
  catch (error) {
    process.stderr.write(`${error instanceof ExcerptError ? error.message : 'Could not read the code; check the repository and the commits.'}\n`);
    process.exitCode = 1;
  }
}
