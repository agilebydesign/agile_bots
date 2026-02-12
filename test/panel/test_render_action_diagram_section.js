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

    test('render button shown even when diagram file does not exist', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: false }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const renderButton = document.querySelector('.render-button');
        assert.ok(renderButton, 'Render button should show for missing diagram');

        assert.strictEqual(document.querySelector('.generate-report-button'), null);
        assert.strictEqual(document.querySelector('.update-button'), null);
    });

    test('generate report button shown when diagram changed since last sync', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true,
              last_sync_time: 1000, file_modified_time: 2000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const staleIndicator = document.querySelector('.stale-indicator');
        assert.ok(staleIndicator);

        const generateButton = document.querySelector('.generate-report-button');
        assert.ok(generateButton);
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
        assert.ok(generateButton);

        const pendingIndicator = document.querySelector('.pending-indicator');
        assert.ok(pendingIndicator);
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

    test('empty diagrams list renders nothing', () => {
        const view = new DiagramSectionView([]);
        assert.strictEqual(view.renderSection(), '');
    });
});
