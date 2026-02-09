'use strict';

const { test, describe } = require('node:test');
const assert = require('node:assert');
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

const repoRoot = path.join(__dirname, '..', '..', '..');
const srcPath = path.join(repoRoot, 'src');
const runJsScannerPath = path.join(repoRoot, 'test', 'helpers', 'run_js_scanner.py');

function runJsScanner(scannerName, filePath) {
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  const result = spawnSync(
    pythonCmd,
    [runJsScannerPath, '--file', filePath, '--scanner', scannerName],
    {
      encoding: 'utf8',
      env: { ...process.env, PYTHONPATH: srcPath },
      cwd: repoRoot,
      maxBuffer: 1024 * 1024,
    }
  );
  if (result.stderr) {
    try {
      const err = JSON.parse(result.stderr);
      return { error: err, status: result.status };
    } catch (_) {
      return { error: result.stderr, status: result.status };
    }
  }
  try {
    const out = JSON.parse(result.stdout || '[]');
    return { violations: Array.isArray(out) ? out : [], status: result.status };
  } catch (e) {
    return { error: result.stdout || e.message, status: result.status };
  }
}

describe('JavaScript code scanners', () => {
  test('ascii_only: reports violation when JS file contains non-ASCII', () => {
    const tmpDir = path.join(repoRoot, 'test', 'invoke_bot', 'perform_action', 'fixtures');
    fs.mkdirSync(tmpDir, { recursive: true });
    const jsFile = path.join(tmpDir, 'has_unicode.js');
    fs.writeFileSync(jsFile, "// comment with unicode: \u2014 dash and \u00a9\nconst x = 1;\n", 'utf8');
    const { violations, status, error } = runJsScanner('ascii_only', jsFile);
    if (error) {
      assert.fail('Scanner failed: ' + (typeof error === 'string' ? error : JSON.stringify(error)));
    }
    assert.strictEqual(status, 0, 'Scanner should exit 0');
    assert.ok(Array.isArray(violations), 'Should return array of violations');
    assert.ok(violations.length >= 1, 'Should report at least one violation for non-ASCII');
    const hasAsciiMsg = violations.some(
      (v) => v.violation_message && v.violation_message.includes('Unicode')
    );
    assert.ok(hasAsciiMsg, 'Violation message should mention Unicode');
    try { fs.unlinkSync(jsFile); } catch (_) {}
  });

  test('ascii_only: no violation when JS file is ASCII-only', () => {
    const tmpDir = path.join(repoRoot, 'test', 'invoke_bot', 'perform_action', 'fixtures');
    fs.mkdirSync(tmpDir, { recursive: true });
    const jsFile = path.join(tmpDir, 'ascii_only.js');
    fs.writeFileSync(jsFile, 'const x = 1; // ASCII only [PASS]\n', 'utf8');
    const { violations, status, error } = runJsScanner('ascii_only', jsFile);
    if (error) {
      assert.fail('Scanner failed: ' + (typeof error === 'string' ? error : JSON.stringify(error)));
    }
    assert.strictEqual(status, 0);
    assert.ok(Array.isArray(violations));
    assert.strictEqual(violations.length, 0, 'ASCII-only file should have no violations');
    try { fs.unlinkSync(jsFile); } catch (_) {}
  });

  test('import_placement: reports violation when require appears after code', () => {
    const tmpDir = path.join(repoRoot, 'test', 'invoke_bot', 'perform_action', 'fixtures');
    fs.mkdirSync(tmpDir, { recursive: true });
    const jsFile = path.join(tmpDir, 'late_import.js');
    fs.writeFileSync(
      jsFile,
      "const a = 1;\nconst b = require('fs');\n",
      'utf8'
    );
    const { violations, status, error } = runJsScanner('import_placement', jsFile);
    if (error) {
      assert.fail('Scanner failed: ' + (typeof error === 'string' ? error : JSON.stringify(error)));
    }
    assert.strictEqual(status, 0);
    assert.ok(Array.isArray(violations));
    assert.ok(violations.length >= 1, 'Should report import after non-import code');
    const hasImportMsg = violations.some(
      (v) => v.violation_message && v.violation_message.toLowerCase().includes('import')
    );
    assert.ok(hasImportMsg, 'Violation message should mention import');
    try { fs.unlinkSync(jsFile); } catch (_) {}
  });

  test('import_placement: no violation when imports are at top', () => {
    const tmpDir = path.join(repoRoot, 'test', 'invoke_bot', 'perform_action', 'fixtures');
    fs.mkdirSync(tmpDir, { recursive: true });
    const jsFile = path.join(tmpDir, 'top_import.js');
    fs.writeFileSync(
      jsFile,
      "const fs = require('fs');\nconst path = require('path');\nconst x = 1;\n",
      'utf8'
    );
    const { violations, status, error } = runJsScanner('import_placement', jsFile);
    if (error) {
      assert.fail('Scanner failed: ' + (typeof error === 'string' ? error : JSON.stringify(error)));
    }
    assert.strictEqual(status, 0);
    assert.ok(Array.isArray(violations));
    assert.strictEqual(violations.length, 0, 'Imports at top should have no violations');
    try { fs.unlinkSync(jsFile); } catch (_) {}
  });
});
