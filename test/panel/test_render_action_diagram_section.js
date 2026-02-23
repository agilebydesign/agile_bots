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

    test('diagram link uses openFile for existing diagram', () => {
        const view = new DiagramSectionView([
            { file_path: '/workspace/story-map.drawio', exists: true }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramLink = document.querySelector('.diagram-link');
        assert.ok(diagramLink);
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

    test('diagram section has diagram-item structure', () => {
        const view = new DiagramSectionView([
            { file_path: 'story-map.drawio', exists: true }
        ]);

        const html = view.renderSection();
        document.body.innerHTML = html;

        const diagramSection = document.querySelector('#diagram-section');
        assert.ok(diagramSection);
        const items = document.querySelectorAll('.diagram-item');
        assert.strictEqual(items.length, 1);
    });
});
