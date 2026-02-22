/**
 * Mock vscode module for panel tests
 */

module.exports = {
    env: {
        uriScheme: 'vscode',
        clipboard: {
            writeText: (text) => Promise.resolve()
        }
    },
    ProgressLocation: {
        Notification: 15,
        Window: 10,
        SourceControl: 1
    },
    Uri: {
        file: (path) => ({ fsPath: path, toString: () => path }),
        joinPath: (base, ...paths) => {
            const path = require('path');
            let result = base.fsPath || base.toString() || '';
            for (const p of paths) {
                result = path.join(result, p);
            }
            return { fsPath: result, toString: () => result };
        }
    },
    ViewColumn: {
        One: 1,
        Two: 2
    },
    Range: class Range {
        constructor(startLine, startChar, endLine, endChar) {
            this.start = { line: startLine, character: startChar };
            this.end = { line: endLine, character: endChar };
        }
    },
    window: {
        showErrorMessage: () => Promise.resolve(),
        showInformationMessage: () => Promise.resolve(),
        showWarningMessage: () => Promise.resolve(),
        showTextDocument: () => Promise.resolve(),
        showOpenDialog: () => Promise.resolve([]),
        showInputBox: () => Promise.resolve(undefined),
        withProgress: (options, task) => task(),
        createOutputChannel: () => ({
            appendLine: () => {},
            show: () => {}
        }),
        createWebviewPanel: () => ({
            webview: {
                asWebviewUri: (uri) => uri,
                postMessage: () => {}
            },
            onDidDispose: () => ({ dispose: () => {} }),
            reveal: () => {}
        })
    },
    workspace: {
        workspaceFolders: [],
        openTextDocument: () => Promise.resolve({
            getText: () => '',
            lineCount: 0
        }),
        getConfiguration: () => ({
            get: (key, defaultValue) => defaultValue !== undefined ? defaultValue : undefined,
            has: () => false,
            inspect: () => undefined,
            update: () => Promise.resolve()
        })
    },
    commands: {
        registerCommand: () => ({ dispose: () => {} }),
        executeCommand: () => Promise.resolve()
    }
};
