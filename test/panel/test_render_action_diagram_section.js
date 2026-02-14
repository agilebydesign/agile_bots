const { test, describe, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert');
const { JSDOM } = require('jsdom');

const DiagramSectionView = require('../../src/panel/diagram_section_view');

describe('TestRenderActionDiagramSection', () => {

    let dom, document;

    beforeEach(() => {
        dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
        document = dom.window.document;
    });

    afterEach(() => {
        dom.window.close();
    });

    test('render button always shown for existing diagram', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        assert.ok(renderButton);
        assert.strictEqual(renderButton.textContent, 'Render Diagram');
        assert.ok(renderButton.getAttribute('onclick').includes('renderDiagram'));
    });

    test('save layout button always shown for existing diagram', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const saveLayoutButton = document.querySelector('.save-layout-button');
        assert.ok(saveLayoutButton);
        assert.strictEqual(saveLayoutButton.textContent, 'Save Layout');
        assert.ok(saveLayoutButton.getAttribute('onclick').includes('saveDiagramLayout'));
    });

    test('render button shown even when diagram file does not exist', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: false }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        assert.ok(renderButton);

        assert.strictEqual(document.querySelector('.save-layout-button'), null);
        assert.strictEqual(document.querySelector('.generate-report-button'), null);
        assert.strictEqual(document.querySelector('.update-button'), null);
    });

    test('generate report button always shown for stale diagram', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const generateButton = document.querySelector('.generate-report-button');
        assert.ok(generateButton);
        assert.strictEqual(generateButton.textContent, 'Generate Report');
    });

    test('generate report button always shown for never-synced diagram', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: null, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const generateButton = document.querySelector('.generate-report-button');
        assert.ok(generateButton);
    });

    test('update graph button shown when report exists', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: 'update-report.json' }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const updateButton = document.querySelector('.update-button');
        assert.ok(updateButton);
        assert.strictEqual(updateButton.textContent, 'Update Graph');
        assert.ok(updateButton.getAttribute('onclick').includes('updateFromDiagram'));
    });

    test('update graph button not shown when no report exists', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: null }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        assert.strictEqual(document.querySelector('.update-button'), null);
    });

    test('diagram link and report link use openFile', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: '/workspace/report.json' }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramLink = document.querySelector('.diagram-link');
        assert.ok(diagramLink.getAttribute('onclick').includes('openFile'));

        const reportLink = document.querySelector('.report-link');
        assert.ok(reportLink.getAttribute('onclick').includes('openFile'));
    });

    test('diagram file does not exist shows missing indicator', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: false }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const missingIndicator = document.querySelector('.missing-indicator');
        assert.ok(missingIndicator);

        assert.strictEqual(document.querySelector('.generate-report-button'), null);
        assert.strictEqual(document.querySelector('.update-button'), null);
    });

    test('empty diagrams list renders nothing', () => {
        const view = new DiagramSectionView([]);
        assert.strictEqual(view.renderSection(), '');
    });

    // --- Scoped Diagram Operations ---
    // Scope is read dynamically from window.diagramScope at click time,
    // not baked into the onclick string.  The onclick always contains
    // the expression (window.diagramScope || '').

    test('render button onclick references window.diagramScope', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        const onclick = renderButton.getAttribute('onclick');
        assert.ok(onclick.includes('window.diagramScope'),
            `Expected window.diagramScope reference in onclick, got: ${onclick}`);
    });

    test('generate report button onclick references window.diagramScope', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const reportButton = document.querySelector('.generate-report-button');
        const onclick = reportButton.getAttribute('onclick');
        assert.ok(onclick.includes('window.diagramScope'),
            `Expected window.diagramScope reference in onclick, got: ${onclick}`);
    });

    test('update graph button onclick references window.diagramScope', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: 'update-report.json' }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const updateButton = document.querySelector('.update-button');
        const onclick = updateButton.getAttribute('onclick');
        assert.ok(onclick.includes('window.diagramScope'),
            `Expected window.diagramScope reference in onclick, got: ${onclick}`);
    });

    test('missing diagram render button onclick references window.diagramScope', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map-explored.drawio', exists: false }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        const onclick = renderButton.getAttribute('onclick');
        assert.ok(onclick.includes('window.diagramScope'),
            `Expected window.diagramScope reference in missing diagram render button, got: ${onclick}`);
    });

    test('onclick preserves Windows backslash paths without mangling', () => {
        const view = new DiagramSectionView([
            { file_path: 'C:\\dev\\agile_bots\\docs\\story.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        const onclick = renderButton.getAttribute('onclick');
        // The path should be properly escaped for JS (doubled backslashes)
        assert.ok(onclick.includes('C:\\\\dev\\\\agile_bots'),
            `Expected properly escaped backslash path, got: ${onclick}`);
    });

    // --- Tests for updateContextualButtons diagram button updates ---
    // These simulate the DOM manipulation that happens in bot_panel.js
    // when a node is selected in the story map tree.
    // The webview code sets window.diagramScope and updates button labels
    // but does NOT rewrite onclick attributes (those read scope dynamically).

    /**
     * Helper: simulates what updateContextualButtons does in the webview.
     * Sets window.diagramScope and updates button labels only.
     */
    function simulateNodeSelection(win, doc, selectedNodeName) {
        const dScope = selectedNodeName || '';
        win.diagramScope = dScope;

        doc.querySelectorAll('.render-button').forEach(btn => {
            btn.textContent = dScope
                ? 'Render Diagram for "' + dScope + '"'
                : 'Render Diagram';
        });
        doc.querySelectorAll('.generate-report-button').forEach(btn => {
            btn.textContent = dScope
                ? 'Generate Report for "' + dScope + '"'
                : 'Generate Report';
        });
        doc.querySelectorAll('.update-button').forEach(btn => {
            btn.textContent = dScope
                ? 'Update Graph for "' + dScope + '"'
                : 'Update Graph';
        });
    }

    test('selecting node updates render button text to include node name', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);
        document.body.innerHTML = view.renderSection();

        // Before selection: default label
        assert.strictEqual(
            document.querySelector('.render-button').textContent,
            'Render Diagram');

        // Simulate selecting "Trace Code"
        simulateNodeSelection(dom.window, document, 'Trace Code');

        assert.strictEqual(
            document.querySelector('.render-button').textContent,
            'Render Diagram for "Trace Code"');
    });

    test('selecting node updates generate report button text', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);
        document.body.innerHTML = view.renderSection();

        simulateNodeSelection(dom.window, document, 'Initialize Bot');

        assert.strictEqual(
            document.querySelector('.generate-report-button').textContent,
            'Generate Report for "Initialize Bot"');
    });

    test('selecting node updates update graph button text', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: 'report.json' }
        ]);
        document.body.innerHTML = view.renderSection();

        simulateNodeSelection(dom.window, document, 'Trace Code');

        assert.strictEqual(
            document.querySelector('.update-button').textContent,
            'Update Graph for "Trace Code"');
    });

    test('selecting node sets window.diagramScope', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);
        document.body.innerHTML = view.renderSection();

        simulateNodeSelection(dom.window, document, 'Trace Code');

        assert.strictEqual(dom.window.diagramScope, 'Trace Code');
        // onclick still references window.diagramScope (unchanged)
        const onclick = document.querySelector('.render-button').getAttribute('onclick');
        assert.ok(onclick.includes('window.diagramScope'),
            `onclick should still reference window.diagramScope, got: ${onclick}`);
    });

    test('deselecting node reverts buttons to default and clears diagramScope', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: 'report.json' }
        ]);
        document.body.innerHTML = view.renderSection();

        // Select then deselect
        simulateNodeSelection(dom.window, document, 'Trace Code');
        assert.strictEqual(
            document.querySelector('.render-button').textContent,
            'Render Diagram for "Trace Code"');

        simulateNodeSelection(dom.window, document, '');

        assert.strictEqual(
            document.querySelector('.render-button').textContent,
            'Render Diagram');
        assert.strictEqual(
            document.querySelector('.generate-report-button').textContent,
            'Generate Report');
        assert.strictEqual(
            document.querySelector('.update-button').textContent,
            'Update Graph');
        assert.strictEqual(dom.window.diagramScope, '');
    });

    test('switching selected node updates buttons to new node name', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);
        document.body.innerHTML = view.renderSection();

        simulateNodeSelection(dom.window, document, 'Trace Code');
        assert.strictEqual(
            document.querySelector('.render-button').textContent,
            'Render Diagram for "Trace Code"');

        simulateNodeSelection(dom.window, document, 'Trace Story');
        assert.strictEqual(
            document.querySelector('.render-button').textContent,
            'Render Diagram for "Trace Story"');
        assert.strictEqual(dom.window.diagramScope, 'Trace Story');
    });
});
