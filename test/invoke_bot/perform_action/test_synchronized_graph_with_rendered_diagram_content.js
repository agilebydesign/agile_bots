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
        dom.window.vscode = {
            postMessage: (msg) => { postedMessages.push(msg); }
        };
        dom.window.openFile = (path, event) => {
            postedMessages.push({ command: 'openFile', filePath: path });
        };
    });

    afterEach(() => {
        dom.window.close();
    });

    test('diagram link uses openFile for existing diagram', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramLink = document.querySelector('.diagram-link');
        assert.ok(diagramLink, 'Diagram link should be present');
        assert.ok(diagramLink.getAttribute('onclick').includes('openFile'));
    });

    test('diagram and report links use openFile when both exist', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000,
              report_path: '/workspace/report.json' }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramLink = document.querySelector('.diagram-link');
        assert.ok(diagramLink);
        assert.ok(diagramLink.getAttribute('onclick').includes('openFile'));

        const reportLink = document.querySelector('.report-link');
        assert.ok(reportLink);
        assert.ok(reportLink.getAttribute('onclick').includes('openFile'));
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

    test('diagram file does not exist shows not found message', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: false }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        assert.ok(html.includes('Not found:'));
        assert.ok(html.includes('story-map.drawio'));
    });

    test('empty diagrams list renders nothing', () => {
        const view = new DiagramSectionView([]);
        assert.strictEqual(view.renderSection(), '');
    });

    test('multiple diagrams each get their own diagram item', () => {
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

        const diagramLinks = document.querySelectorAll('.diagram-link');
        assert.strictEqual(diagramLinks.length, 2, 'Each diagram should have a diagram link');
    });

    test('windows paths with backslashes are properly escaped in diagram link onclick', () => {
        const view = new DiagramSectionView([
            { file_path: 'C:\\dev\\workspace\\docs\\story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramLink = document.querySelector('.diagram-link');
        assert.ok(diagramLink);
        const onclick = diagramLink.getAttribute('onclick');
        assert.ok(onclick.includes('C:\\\\dev\\\\workspace\\\\docs\\\\story-map.drawio'),
            'Windows paths should have backslashes escaped in openFile link');
    });

    test('diagram section has diagram-item structure', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true,
              last_sync_time: 2000, file_modified_time: 1000 }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramSection = document.querySelector('#diagram-section');
        assert.ok(diagramSection);
        const items = document.querySelectorAll('.diagram-item');
        assert.strictEqual(items.length, 1);
    });
});
