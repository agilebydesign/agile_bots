/**
 * Branding utility for Panel
 * 
 * Centralizes branding logic - reads from conf/config.json
 * and provides helpers for image paths, text, colors.
 */

const fs = require('fs');
const path = require('path');

// Cache the config
let _config = null;
let _repoRoot = null;

// Default brand settings
const DEFAULT_BRANDS = {
    ABD: {
        path: '',
        title: 'Agile Bots',
        color: '#FF8C00',
        background: '#000000',
        textColor: '#FFFFFF',
        textColorFaded: '#999999',
        fontWeight: '400'
    },
    Scotia: {
        path: 'scotia',
        title: 'Scotia Bots',
        color: '#EC111A',
        background: '#FFFFFF',
        textColor: '#000000',
        textColorFaded: '#E88A8E',
        fontWeight: '600'
    }
};

/**
 * Set the repo root path (should be called once during panel init)
 * @param {string} repoRoot - Path to repo root (parent of bots/)
 */
function setRepoRoot(repoRoot) {
    if (repoRoot && repoRoot !== _repoRoot) {
        _repoRoot = repoRoot;
        _config = null; // Clear cache to reload with new path
        console.log(`[Branding] Repo root set to: ${_repoRoot}`);
    }
}

/**
 * Load branding config from conf/config.json
 * @returns {Object} Config object with branding property
 */
function loadConfig() {
    if (_config) {
        return _config;
    }
    
    if (!_repoRoot) {
        console.warn('[Branding] Repo root not set, using defaults');
        _config = { branding: 'ABD', brands: DEFAULT_BRANDS };
        return _config;
    }
    
    const configPath = path.join(_repoRoot, 'conf', 'config.json');
    
    try {
        if (fs.existsSync(configPath)) {
            const content = fs.readFileSync(configPath, 'utf8');
            _config = JSON.parse(content);
            console.log(`[Branding] Loaded config from ${configPath}: branding=${_config.branding}`);
        } else {
            console.warn(`[Branding] Config not found at ${configPath}, using defaults`);
            _config = { branding: 'ABD', brands: DEFAULT_BRANDS };
        }
    } catch (err) {
        console.error(`[Branding] Error loading config: ${err.message}`);
        _config = { branding: 'ABD', brands: DEFAULT_BRANDS };
    }
    
    // Merge with defaults to ensure all properties exist
    _config.brands = { ...DEFAULT_BRANDS, ...(_config.brands || {}) };
    
    return _config;
}

/**
 * Get current branding mode
 * @returns {string} 'ABD' or 'Scotia'
 */
function getBranding() {
    const config = loadConfig();
    return config.branding || 'ABD';
}

/**
 * Get current brand settings
 * @returns {Object} {path, title, color}
 */
function getBrandSettings() {
    const config = loadConfig();
    const brandName = config.branding || 'ABD';
    return config.brands[brandName] || DEFAULT_BRANDS.ABD;
}

/**
 * Check if Scotia branding is active
 * @returns {boolean}
 */
function isScotia() {
    return getBranding() === 'Scotia';
}

/**
 * Get the image subdirectory for current branding
 * @returns {string} '' for ABD, 'scotia' for Scotia
 */
function getImageSubdir() {
    return getBrandSettings().path;
}

/**
 * Get branded image path
 * @param {string} imageName - Image filename (e.g., 'gear.png')
 * @returns {string} Path relative to img/ (e.g., 'scotia/gear.png' or 'gear.png')
 */
function getImagePath(imageName) {
    const subdir = getImageSubdir();
    if (subdir) {
        return `${subdir}/${imageName}`;
    }
    return imageName;
}

/**
 * Get branded product name/title
 * @returns {string} 'Agile Bots' or 'Scotia Bots'
 */
function getProductName() {
    return getBrandSettings().title;
}

/**
 * Get branded title/accent color (for HTML/CSS)
 * @returns {string} CSS color value
 */
function getTitleColor() {
    return getBrandSettings().color;
}

/**
 * Get branded background color
 * @returns {string} CSS color value
 */
function getBackgroundColor() {
    return getBrandSettings().background || '#000000';
}

/**
 * Get branded text color
 * @returns {string} CSS color value
 */
function getTextColor() {
    return getBrandSettings().textColor || '#FFFFFF';
}

/**
 * Get branded font weight for body text
 * @returns {string} CSS font-weight value
 */
function getFontWeight() {
    return getBrandSettings().fontWeight || '400';
}

/**
 * Get branded faded/secondary text color
 * @returns {string} CSS color value
 */
function getTextColorFaded() {
    return getBrandSettings().textColorFaded || '#999999';
}

/**
 * Get branded title style attribute
 * @returns {string} style attribute value
 */
function getTitleStyle() {
    const color = getTitleColor();
    return `style="color: ${color};"`;
}

/**
 * Build webview URI for an image
 * @param {Object} webview - VS Code webview instance
 * @param {Object} extensionUri - Extension URI
 * @param {string} imageName - Image filename (e.g., 'gear.png')
 * @returns {string} Webview URI string, or simple path if no webview
 */
function getImageUri(webview, extensionUri, imageName) {
    const vscode = require('vscode');
    const imagePath = getImagePath(imageName);
    
    if (webview && extensionUri) {
        try {
            // Split path into parts for Uri.joinPath
            const parts = imagePath.split('/').filter(p => p);
            const imageUri = vscode.Uri.joinPath(extensionUri, 'img', ...parts);
            return webview.asWebviewUri(imageUri).toString();
        } catch (err) {
            console.error(`[Branding] Error creating URI for ${imageName}: ${err.message}`);
        }
    }
    
    // Fallback for tests or when webview not available
    return `img/${imagePath}`;
}

/**
 * Clear cached config (useful for tests or hot-reload)
 */
function clearCache() {
    _config = null;
}

module.exports = {
    setRepoRoot,
    loadConfig,
    getBranding,
    getBrandSettings,
    isScotia,
    getImageSubdir,
    getImagePath,
    getProductName,
    getTitleColor,
    getBackgroundColor,
    getTextColor,
    getTextColorFaded,
    getFontWeight,
    getTitleStyle,
    getImageUri,
    clearCache
};
