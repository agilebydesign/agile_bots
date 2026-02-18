/**
 * IncrementView - Testable view model for increment display and edit.
 * Used by Panel for Increment view mode. Supports read-only display and
 * (when edit mode enabled) Add, Delete, inline edit, drag operations.
 */
class IncrementView {

    constructor(storyGraph, options = {}) {
        this._storyGraph = storyGraph || { epics: [], increments: [] };
        this._editMode = options.editMode === true;
        this.currentView = options.initialView || 'Hierarchy';
    }

    toggleView() {
        const newView = this.currentView === 'Hierarchy' ? 'Increment' : 'Hierarchy';
        this.currentView = newView;
        const toggleLabel = newView === 'Increment' ? 'Hierarchy' : 'Increment';
        const tooltip = newView === 'Increment' ? 'Display Hierarchy view' : 'Display Increment view';
        return {
            current_view: newView,
            toggle_label: toggleLabel,
            tooltip
        };
    }

    renderIncrementColumns() {
        const increments = this._storyGraph.increments || [];
        const columns = increments.map(inc => {
            const stories = (inc.stories || []).slice().sort((a, b) =>
                (a.sequential_order || 0) - (b.sequential_order || 0)
            );
            const column = {
                name: inc.name,
                stories: stories.map(s => typeof s === 'string' ? { name: s, sequential_order: 0 } : s),
                read_only: !this._editMode
            };
            if (stories.length === 0) {
                column.empty_message = '(no stories)';
            }
            return column;
        });
        return {
            columns,
            controls_visible: this._editMode
        };
    }

    setEditMode(enabled) {
        this._editMode = enabled === true;
    }
}

module.exports = IncrementView;
