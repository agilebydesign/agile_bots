const { test, describe, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert');
const { JSDOM } = require('jsdom');

const DiagramSectionView = require('../../../src/panel/diagram_section_view');

describe('TestRenderActionDiagramSection', () => {

    let dom, document, postedMessages;

    beforeEach(() => {
        dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
        document = dom.window.document;
        postedMessages = [];
        // Mock vscode.postMessage so button clicks are captured
        dom.window.vscode = {
            postMessage: (msg) => { postedMessages.push(msg); }
        };
        // Mock openFile function used by diagram and report links
        dom.window.openFile = (path, event) => {
            postedMessages.push({ command: 'openFile', filePath: path });
        };
    });

    afterEach(() => {
        dom.window.close();
    });

    // --- Render Diagram button ---

    test('render button always shown for existing diagram', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        assert.ok(renderButton, 'Render button should be present');
        assert.strictEqual(renderButton.textContent, 'Render Diagram');
        assert.ok(renderButton.getAttribute('onclick').includes('renderDiagram'));
    });

    test('render button shown even when diagram file does not exist', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: false }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        assert.ok(renderButton, 'Render button should show for missing diagram');
        // Missing diagram should show missing indicator
        const missingIndicator = document.querySelector('.missing-indicator');
        assert.ok(missingIndicator, 'Missing indicator should be shown');
    });

    test('render button onclick sends renderDiagram command without path', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/docs/story-map-outline.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        const onclick = renderButton.getAttribute('onclick');
        // Command should not include path - render action resolves paths internally
        assert.ok(onclick.includes("command: 'renderDiagram'"), 'Should send renderDiagram command');
        assert.ok(!onclick.includes("path:"), 'Should NOT include path argument');
    });

    // --- Generate Report button ---

    test('generate report button shown when diagram changed since last sync', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const staleIndicator = document.querySelector('.stale-indicator');
        assert.ok(staleIndicator, 'Stale indicator should be shown');
        assert.ok(staleIndicator.textContent.includes('Changed since last sync'));

        const generateButton = document.querySelector('.generate-report-button');
        assert.ok(generateButton, 'Generate report button should be shown');
        assert.strictEqual(generateButton.textContent, 'Generate Report');
        assert.ok(generateButton.getAttribute('onclick').includes('generateDiagramReport'));
    });

    test('generate report button shown when diagram never synced', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: null, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const generateButton = document.querySelector('.generate-report-button');
        assert.ok(generateButton, 'Generate report button should be shown for never-synced diagram');

        const pendingIndicator = document.querySelector('.pending-indicator');
        assert.ok(pendingIndicator, 'Pending indicator should be shown');
        assert.ok(pendingIndicator.textContent.includes('Not yet synced'));
    });

    test('generate report button NOT shown when diagram is in sync', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const generateButton = document.querySelector('.generate-report-button');
        assert.strictEqual(generateButton, null,
            'Generate report button should NOT be shown when diagram is in sync');
    });

    test('generate report button onclick sends generateDiagramReport command without path', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/docs/story-map-outline.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const generateButton = document.querySelector('.generate-report-button');
        const onclick = generateButton.getAttribute('onclick');
        assert.ok(onclick.includes("command: 'generateDiagramReport'"),
            'Should send generateDiagramReport command');
        assert.ok(!onclick.includes("path:"), 'Should NOT include path argument');
    });

    // --- Generate Report button NOT shown for missing diagram ---

    test('generate report and update buttons not shown for missing diagram', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: false }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        assert.strictEqual(document.querySelector('.generate-report-button'), null,
            'Generate report button should not show for missing diagram');
        assert.strictEqual(document.querySelector('.update-button'), null,
            'Update button should not show for missing diagram');
    });

    // --- Update Graph button ---

    test('update graph button shown when report exists', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: 'update-report.json' }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const updateButton = document.querySelector('.update-button');
        assert.ok(updateButton, 'Update Graph button should be shown when report exists');
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

        assert.strictEqual(document.querySelector('.update-button'), null,
            'Update button should not show when no report');
    });

    test('update graph button onclick sends updateFromDiagram without paths', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/docs/story-map-outline.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: '/workspace/docs/story-map-outline-update-report.json' }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const updateButton = document.querySelector('.update-button');
        const onclick = updateButton.getAttribute('onclick');
        assert.ok(onclick.includes("command: 'updateFromDiagram'"),
            'Should send updateFromDiagram command');
        // Paths no longer sent - render action resolves them internally
        assert.ok(!onclick.includes("path:"), 'Should NOT include path argument');
        assert.ok(!onclick.includes("report:"), 'Should NOT include report argument');
    });

    // --- Links ---

    test('diagram link and report link use openFile', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: '/workspace/report.json' }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramLink = document.querySelector('.diagram-link');
        assert.ok(diagramLink, 'Diagram link should be present');
        assert.ok(diagramLink.getAttribute('onclick').includes('openFile'),
            'Diagram link should use openFile');

        const reportLink = document.querySelector('.report-link');
        assert.ok(reportLink, 'Report link should be present');
        assert.ok(reportLink.getAttribute('onclick').includes('openFile'),
            'Report link should use openFile');
    });

    test('report link not shown when no report exists', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: null }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        assert.strictEqual(document.querySelector('.report-link'), null,
            'Report link should not be shown when no report');
    });

    // --- Edge cases ---

    test('empty diagrams list renders nothing', () => {
        const view = new DiagramSectionView([]);
        assert.strictEqual(view.renderSection(), '');
    });

    test('multiple diagrams each get their own section with correct paths', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map-outline.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 },
            { file_path: '/workspace/story-map-increments.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramItems = document.querySelectorAll('.diagram-item');
        assert.strictEqual(diagramItems.length, 2, 'Should render two diagram items');

        const renderButtons = document.querySelectorAll('.render-button');
        assert.strictEqual(renderButtons.length, 2, 'Each diagram should have a render button');

        // Second diagram is stale, should have generate report button
        const generateButtons = document.querySelectorAll('.generate-report-button');
        assert.strictEqual(generateButtons.length, 1,
            'Only stale diagram should have generate report button');
    });

    test('windows paths with backslashes are properly escaped in diagram link onclick', () => {
        const view = new DiagramSectionView([
            { file_path: 'C:\\dev\\workspace\\docs\\story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        // Diagram link (openFile) still uses paths - verify escaping there
        const diagramLink = document.querySelector('.diagram-link');
        const onclick = diagramLink.getAttribute('onclick');
        // Backslashes should be escaped for JavaScript string
        assert.ok(onclick.includes('C:\\\\dev\\\\workspace\\\\docs\\\\story-map.drawio'),
            'Windows paths should have backslashes escaped in openFile link');
    });

    test('stale diagram shows both stale indicator and pending changes indicator', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const staleIndicator = document.querySelector('.stale-indicator');
        assert.ok(staleIndicator, 'Stale indicator should be shown');

        const pendingIndicator = document.querySelector('.pending-indicator');
        assert.ok(pendingIndicator, 'Pending changes indicator should be shown');
        assert.ok(pendingIndicator.textContent.includes('Pending changes'));
    });

    test('diagram data-path attribute matches file path for test verification', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        assert.strictEqual(renderButton.getAttribute('data-path'),
            '/workspace/story-map.drawio',
            'data-path attribute should match file_path for testing');
    });
});
