class IncrementView {
    constructor(storyGraph) {
        this.storyGraph = storyGraph;
        this.currentView = 'Hierarchy';
    }

    toggleView() {
        const previousView = this.currentView;
        this.currentView = this.currentView === 'Hierarchy' ? 'Increment' : 'Hierarchy';
        return {
            current_view: this.currentView,
            toggle_label: previousView,
            tooltip: `Display ${previousView} view`
        };
    }

    renderIncrementColumns() {
        const increments = this.storyGraph.increments || [];
        const columns = increments.map(increment => {
            const stories = increment.stories || [];
            const sortedStories = [...stories].sort((a, b) => 
                (a.sequential_order || 0) - (b.sequential_order || 0)
            );
            const column = {
                name: increment.name,
                stories: sortedStories,
                read_only: true
            };
            if (stories.length === 0) {
                column.empty_message = "(no stories)";
            }
            return column;
        });
        return {
            columns: columns,
            controls_visible: false
        };
    }
}

module.exports = IncrementView;
