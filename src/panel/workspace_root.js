/**
 * Resolves which workspace folder should drive the Bot Panel (branding, bots/, conf/).
 *
 * Using only workspaceFolders[0] breaks multi-root windows: branding is read from
 * <repoRoot>/conf/config.json, so we pick the folder that is actually this repo.
 */

const fs = require('fs');
const path = require('path');

/**
 * @param {import('vscode')} vscode
 * @returns {string | null} Absolute path, or null if no folders open
 */
function getPanelWorkspaceRoot(vscode) {
    const folders = vscode.workspace?.workspaceFolders;
    if (!folders || folders.length === 0) {
        return null;
    }

    const roots = folders.map((f) => f.uri.fsPath);

    const looksLikeAgileBotsRepo = (root) =>
        fs.existsSync(path.join(root, 'conf', 'config.json')) &&
        fs.existsSync(path.join(root, 'bots', 'story_bot'));

    for (const root of roots) {
        if (looksLikeAgileBotsRepo(root)) {
            return root;
        }
    }

    for (const root of roots) {
        if (fs.existsSync(path.join(root, 'conf', 'config.json'))) {
            return root;
        }
    }

    return roots[0];
}

module.exports = { getPanelWorkspaceRoot };
