import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { diffLines, excerpt, repositoryName, window } from './code-excerpt.mjs';

const helper = fileURLToPath(new URL('./code-excerpt.mjs', import.meta.url));
const numbered = (count, change = {}) => Array.from({ length: count }, (_, index) => change[index + 1] ?? `line ${index + 1}`).join('\n') + '\n';

function repository() {
  const dir = mkdtempSync(join(tmpdir(), 'code-excerpt-'));
  const run = (...args) => execFileSync('git', args, { cwd: dir, encoding: 'utf8' });
  run('init', '-q'); run('config', 'user.email', 'fixture@example.test'); run('config', 'user.name', 'Fixture');
  writeFileSync(join(dir, 'model.py'), numbered(30));
  run('add', '.'); run('commit', '-qm', 'before');
  const base = run('rev-parse', '--short=12', 'HEAD').trim();
  // Line 10 changes, line 20 goes, a line is added after 25.
  const lines = numbered(30, { 10: 'cutoff = 16' }).split('\n');
  lines.splice(19, 1);
  lines.splice(24, 0, 'skip_long = True');
  writeFileSync(join(dir, 'model.py'), lines.join('\n'));
  run('add', '.'); run('commit', '-qm', 'after');
  return { dir, run, base, head: run('rev-parse', '--short=12', 'HEAD').trim() };
}

test('names a repository the way a reader recognizes it, never with credentials', () => {
  assert.equal(repositoryName('git@github.com:lab/llopa.git', '/x/llopa'), 'github.com/lab/llopa');
  assert.equal(repositoryName('https://token-secret@github.com/lab/llopa.git', '/x/llopa'), 'github.com/lab/llopa');
  assert.equal(repositoryName('https://gitlab.example.edu/group/llopa', '/x/llopa'), 'gitlab.example.edu/group/llopa');
  assert.equal(repositoryName('', '/home/me/llopa'), 'llopa');
});

test('keeps twelve lines around the marked one, inside the file', () => {
  assert.deepEqual(window(10, 30), [5, 16]);
  assert.deepEqual(window(2, 30), [1, 12]);
  assert.deepEqual(window(29, 30), [19, 30]);
  assert.deepEqual(window(3, 5), [1, 5]);
  assert.deepEqual(window(10, 30, 9, 11), [9, 11]);
  assert.throws(() => window(10, 30, 1, 13), /span at most 12/);
});

test('reads added and removed lines from a zero-context diff', () => {
  const { added, removed } = diffLines('diff --git a/m b/m\n--- a/m\n+++ b/m\n@@ -10 +10 @@\n-line 10\n+cutoff = 16\n@@ -20 +19,0 @@\n-line 20\n@@ -25,0 +25 @@\n+skip_long = True\n');
  assert.deepEqual([...added], [10, 25]);
  assert.deepEqual(removed, [{ at: 10, text: 'line 10' }, { at: 20, text: 'line 20' }]);
});

test('copies the lines of a commit with what the change added and removed', () => {
  const { dir, base, head } = repository();
  try {
    const result = excerpt({ repo: dir, base, targets: ['model.py:10', 'model.py:25:24-26'] });
    assert.deepEqual(result.code, { repo: result.code.repo, base, head, files: [{ path: 'model.py', added: 2, removed: 2 }] });
    assert.deepEqual(result.locations['model.py:10'], { file: 'model.py', start: 5, end: 16, mark: 10,
      excerpt: ['line 5', 'line 6', 'line 7', 'line 8', 'line 9', 'cutoff = 16', 'line 11', 'line 12', 'line 13', 'line 14', 'line 15', 'line 16'].join('\n'),
      added: [10], removed: [{ at: 10, text: 'line 10' }] });
    assert.deepEqual(result.locations['model.py:25:24-26'], { file: 'model.py', start: 24, end: 26, mark: 25, excerpt: 'line 25\nskip_long = True\nline 26', added: [25] });
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('reports uncommitted changes, new files included, as the working tree', () => {
  const { dir, head } = repository();
  try {
    writeFileSync(join(dir, 'model.py'), numbered(29, { 3: 'cutoff = 24' }));
    writeFileSync(join(dir, 'test_model.py'), 'def test_cutoff():\n    assert cutoff == 24\n');
    const result = excerpt({ repo: dir, targets: ['test_model.py:2'] });
    assert.equal(result.code.head, 'working-tree');
    assert.equal(result.code.base, head);
    assert.deepEqual(result.code.files.find((file) => file.path === 'test_model.py'), { path: 'test_model.py', added: 2, removed: 0 });
    assert.deepEqual(result.locations['test_model.py:2'], { file: 'test_model.py', start: 1, end: 2, mark: 2, excerpt: 'def test_cutoff():\n    assert cutoff == 24', added: [1, 2] });
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('refuses paths outside the repository and lines outside the file, and runs through a symlinked folder', () => {
  const { dir, base } = repository();
  const link = join(tmpdir(), `code-excerpt-link-${process.pid}`);
  try {
    assert.throws(() => excerpt({ repo: dir, base, targets: ['../secret.py:1'] }), /inside the repository/);
    assert.throws(() => excerpt({ repo: dir, base, targets: ['model.py:99'] }), /line 99 is not one of them/);
    symlinkSync(join(fileURLToPath(new URL('.', import.meta.url))), link);
    const result = spawnSync(process.execPath, [join(link, 'code-excerpt.mjs'), '--repo', dir, '--base', base, 'model.py:10'], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(result.stdout).locations['model.py:10'].mark, 10);
    const missing = spawnSync(process.execPath, [helper, '--repo', dir], { encoding: 'utf8' });
    assert.equal(missing.status, 1);
    assert.match(missing.stderr, /^Usage: node code-excerpt\.mjs/);
  } finally { rmSync(dir, { recursive: true, force: true }); rmSync(link, { force: true }); }
});

test('rejects Windows absolute, drive-relative and traversal paths on every platform', () => {
  const { dir, base } = repository();
  try {
    for (const file of ['C:\\private\\secret.py', 'C:secret.py', '\\\\server\\share\\secret.py', '..\\secret.py', 'src\\..\\secret.py', '/private/secret.py']) {
      assert.throws(() => excerpt({ repo: dir, base, head: 'working-tree', targets: [`${file}:1`] }), /inside the repository/, file);
    }
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('rejects a tracked outside-file symlink in a dirty tree but preserves git-show commit reads', () => {
  const { dir, run } = repository();
  const outside = mkdtempSync(join(tmpdir(), 'code-excerpt-outside-'));
  try {
    const secret = join(outside, 'private.py');
    writeFileSync(secret, 'synthetic outside content must not be disclosed\n');
    symlinkSync(secret, join(dir, 'linked.py'));
    run('add', 'linked.py'); run('commit', '-qm', 'link fixture');
    writeFileSync(join(dir, 'model.py'), 'changed\n');
    const result = spawnSync(process.execPath, [helper, '--repo', dir, 'linked.py:1'], { encoding: 'utf8', timeout: 5000 });
    assert.equal(result.error, undefined);
    assert.equal(result.status, 1);
    assert.equal(result.stdout, '');
    assert.match(result.stderr, /symbolic link/);
    const committed = excerpt({ repo: dir, head: 'HEAD', targets: ['linked.py:1'] });
    assert.equal(committed.locations['linked.py:1'].excerpt, secret);
  } finally { rmSync(dir, { recursive: true, force: true }); rmSync(outside, { recursive: true, force: true }); }
});

test('rejects outside-directory symlinks in a selected file path', () => {
  const { dir, run } = repository();
  const outside = mkdtempSync(join(tmpdir(), 'code-excerpt-outside-'));
  try {
    writeFileSync(join(outside, 'private.py'), 'synthetic outside content\n');
    symlinkSync(outside, join(dir, 'linked-dir'), 'dir');
    run('add', 'linked-dir');
    assert.throws(() => excerpt({ repo: dir, head: 'working-tree', targets: ['linked-dir/private.py:1'] }), /symbolic link/);
  } finally { rmSync(dir, { recursive: true, force: true }); rmSync(outside, { recursive: true, force: true }); }
});

test('counts an untracked link it was not asked for as git stores it, never reading what it points at', () => {
  const { dir } = repository();
  const outside = mkdtempSync(join(tmpdir(), 'code-excerpt-outside-'));
  try {
    writeFileSync(join(outside, 'private.py'), 'synthetic outside content\nsecond\nthird\n');
    symlinkSync(join(outside, 'private.py'), join(dir, 'untracked.py'));
    symlinkSync(outside, join(dir, 'data'), 'dir');
    // A checkpoint or dataset link beside the code must not stop an excerpt of the code.
    const result = excerpt({ repo: dir, targets: ['model.py:1'] });
    assert.deepEqual(result.code.files, [
      { path: 'data', added: 1, removed: 0 },
      { path: 'untracked.py', added: 1, removed: 0 },
    ]);
    assert.doesNotMatch(JSON.stringify(result), /synthetic outside content/);
    assert.throws(() => excerpt({ repo: dir, targets: ['untracked.py:1'] }), /untracked\.py uses a symbolic link/);
  } finally { rmSync(dir, { recursive: true, force: true }); rmSync(outside, { recursive: true, force: true }); }
});

test('reads file names as they are, Korean included, not as git quotes them', () => {
  const { dir, run } = repository();
  try {
    writeFileSync(join(dir, '실험 결과.py'), 'loss = 1\n');
    run('add', '실험 결과.py'); run('commit', '-qm', 'results');
    writeFileSync(join(dir, '실험 결과.py'), 'loss = 2\n');
    writeFileSync(join(dir, '새 노트.md'), '메모\n');
    const result = excerpt({ repo: dir, targets: ['실험 결과.py:1'] });
    assert.deepEqual(result.code.files, [
      { path: '실험 결과.py', added: 1, removed: 1 },
      { path: '새 노트.md', added: 1, removed: 0 },
    ]);
    assert.equal(result.locations['실험 결과.py:1'].excerpt, 'loss = 2');
    assert.deepEqual(result.locations['실험 결과.py:1'].added, [1]);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('counts a nested repository it was not asked for as a changed path with no lines', () => {
  const { dir } = repository();
  try {
    const nested = join(dir, 'vendor', 'lib');
    mkdirSync(nested, { recursive: true });
    execFileSync('git', ['init', '-q'], { cwd: nested });
    writeFileSync(join(nested, 'lib.py'), 'x = 1\n');
    const result = excerpt({ repo: dir, targets: ['model.py:1'] });
    assert.deepEqual(result.code.files, [{ path: 'vendor/lib/', added: 0, removed: 0 }]);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('counts ordinary untracked files and excerpts a nested file without a trailing newline', () => {
  const { dir } = repository();
  try {
    mkdirSync(join(dir, 'src'));
    writeFileSync(join(dir, 'src', 'new.py'), 'first\nsecond');
    writeFileSync(join(dir, 'other.py'), 'ordinary\n');
    const result = excerpt({ repo: dir, targets: ['src/new.py:2'] });
    assert.deepEqual(result.code.files, [
      { path: 'other.py', added: 1, removed: 0 },
      { path: 'src/new.py', added: 2, removed: 0 },
    ]);
    assert.equal(result.locations['src/new.py:2'].excerpt, 'first\nsecond');
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('rejects a directory as a working-tree file', () => {
  const { dir } = repository();
  try {
    mkdirSync(join(dir, 'directory'));
    assert.throws(() => excerpt({ repo: dir, head: 'working-tree', targets: ['directory:1'] }), /regular file/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('rejects a named pipe without blocking', { skip: process.platform === 'win32' }, (t) => {
  const { dir } = repository();
  try {
    const created = spawnSync('mkfifo', [join(dir, 'pipe')], { encoding: 'utf8' });
    if (created.error?.code === 'ENOENT') { t.skip('mkfifo is unavailable'); return; }
    assert.equal(created.status, 0, created.stderr);
    const result = spawnSync(process.execPath, [helper, '--repo', dir, '--head', 'working-tree', 'pipe:1'], { encoding: 'utf8', timeout: 5000 });
    assert.equal(result.error, undefined);
    assert.equal(result.status, 1);
    assert.equal(result.stdout, '');
    assert.match(result.stderr, /regular file/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('refuses to excerpt a tracked or untracked working-tree file over the size limit', () => {
  const { dir } = repository();
  try {
    writeFileSync(join(dir, 'model.py'), Buffer.alloc(5 * 1024 * 1024 + 1, 'x'));
    assert.throws(() => excerpt({ repo: dir, targets: ['model.py:1'] }), /5242880-byte working-tree file limit/);
    writeFileSync(join(dir, 'model.py'), 'ordinary\n');
    writeFileSync(join(dir, 'large.py'), Buffer.alloc(5 * 1024 * 1024 + 1, 'x'));
    assert.throws(() => excerpt({ repo: dir, targets: ['large.py:1'] }), /large\.py exceeds the 5242880-byte working-tree file limit/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test('counts large, binary and empty untracked files it was not asked for, as git does', () => {
  const { dir } = repository();
  try {
    const row = 'step,loss\n';
    const rows = Math.ceil((5 * 1024 * 1024 + 1) / row.length);
    writeFileSync(join(dir, 'results.csv'), row.repeat(rows));
    // A NUL near the start makes a file binary to git, which counts no lines for it.
    writeFileSync(join(dir, 'weights.bin'), Buffer.concat([Buffer.from([0, 1, 2]), Buffer.alloc(64, '\n')]));
    writeFileSync(join(dir, 'empty.txt'), '');
    const result = excerpt({ repo: dir, targets: ['model.py:1'] });
    assert.deepEqual(result.code.files, [
      { path: 'empty.txt', added: 0, removed: 0 },
      { path: 'results.csv', added: rows, removed: 0 },
      { path: 'weights.bin', added: 0, removed: 0 },
    ]);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
