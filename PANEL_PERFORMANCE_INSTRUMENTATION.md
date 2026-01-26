# Panel Performance Instrumentation

## Overview

Performance instrumentation has been added throughout the panel code to help identify bottlenecks during startup and major operations.

## What Was Instrumented

### 1. Extension Activation (`src/panel/extension.js`)
- **Extension activation**: Total time to activate the extension
- **viewPanel command**: Time to execute the command when user opens the panel
- **BotPanel.createOrShow**: Time to create or show the panel

### 2. BotPanel Initialization (`src/panel/bot_panel.js`)
- **Constructor**: Total constructor execution time
  - Read panel version
  - PanelView creation
- **_update() method**: Total update time and breakdown:
  - BotView creation (if first time)
  - Data refresh (calling _botView.refresh())
  - HTML rendering (calling _botView.render())
  - HTML update (setting webview.html)

### 3. BotView Rendering (`src/panel/bot_view.js`)
- **render() method**: Total time and breakdown by section:
  - Header rendering
  - Behaviors rendering
  - Story map rendering
  - Instructions rendering
  - Final HTML assembly
- **refresh() method**: Time to execute 'status' command

### 4. StoryMapView Rendering (`src/panel/story_map_view.js`)
- **render() method**: Total time and breakdown:
  - execute('status') call
  - Content rendering
  - renderRootNode
  - renderStoryTree (with epic count)
  - HTML assembly

## How to Read the Performance Logs

### Log Format
All performance logs are prefixed with `[PERF]` and show duration in milliseconds:
```
[PERF] Operation name: 123.45ms
```

### Where to Find Logs

1. **Console Output**: All performance data is logged to console.log
   - Open VS Code Developer Tools: Help > Toggle Developer Tools
   - Look for `[PERF]` entries in the Console tab

2. **Output Channel**: Extension logs go to the "Bot Panel" output channel
   - View > Output > Select "Bot Panel" from dropdown

3. **Log File**: BotPanel logs are written to:
   - `{workspace}/panel-debug.log`
   - Location: `C:\dev\agile_bots\panel-debug.log`
   - Contains timestamped entries with `[PERF]` markers

## Typical Performance Breakdown

Here's what you should see when opening the panel:

```
[PERF] Extension activation: ~5-10ms
[PERF] viewPanel command: ~50-100ms
  [PERF] BotPanel.createOrShow: ~50-100ms
    [PERF] Constructor: ~30-60ms
      [PERF] Read panel version: ~1-5ms
      [PERF] PanelView creation: ~20-40ms
    [PERF] _update(): ~XXXms (this is where the real work happens)
      [PERF] BotView creation: ~10-30ms (first time only)
      [PERF] Data refresh: ~XXXms
        [PERF] refresh() (execute status): ~XXXms
      [PERF] HTML rendering: ~XXXms
        [PERF] Header render: ~10-50ms
        [PERF] Behaviors render: ~10-50ms
        [PERF] Story map render: ~XXXms (likely bottleneck)
          [PERF] execute('status'): ~XXXms
          [PERF] Content rendering: ~XXXms
            [PERF] renderRootNode: ~1-5ms
            [PERF] renderStoryTree (N epics): ~XXXms (scales with story count)
          [PERF] HTML assembly: ~1-5ms
        [PERF] Instructions render: ~10-50ms
        [PERF] Final HTML assembly: ~1-5ms
      [PERF] HTML update (set webview.html): ~10-50ms
```

## Identifying Bottlenecks

### Look for:

1. **Data Loading**: 
   - `execute('status')` calls - if > 100ms, the CLI/backend is slow
   - `Data refresh` - combines CLI execution and data processing

2. **Rendering**:
   - `renderStoryTree` - scales with number of epics/stories
   - If > 500ms with many stories, consider:
     - Lazy rendering (only render visible nodes)
     - Virtual scrolling
     - HTML template optimization

3. **HTML Update**:
   - `set webview.html` - if > 100ms, the HTML is too large
   - Consider chunking or progressive rendering

4. **Total Times**:
   - `TOTAL _update() duration` - complete panel refresh
   - Target: < 500ms for good UX
   - Acceptable: < 1000ms
   - Problematic: > 2000ms

## Using the Instrumentation

### During Development:
1. Open VS Code Developer Tools (Help > Toggle Developer Tools)
2. Run the "View Bot Panel" command
3. Watch Console tab for `[PERF]` entries
4. Compare times before/after optimizations

### For Bug Reports:
1. Reproduce the performance issue
2. Copy `panel-debug.log` contents
3. Look for `[PERF]` entries showing high durations
4. Include in bug report with context

## Example Investigation

If the panel takes 5 seconds to load:

1. Check `TOTAL _update() duration` - is it ~5000ms?
2. Look at breakdown:
   - If `Data refresh` is 4000ms → CLI/backend issue
   - If `HTML rendering` is 4000ms → check sub-components
     - If `Story map render` is 3500ms → story tree bottleneck
       - If `renderStoryTree` is 3000ms → too many stories or complex HTML
   - If `HTML update` is 2000ms → HTML too large for webview

## Next Steps

Based on bottlenecks identified:
- **Slow CLI**: Optimize Python backend, add caching
- **Slow tree render**: Virtual scrolling, lazy loading, HTML simplification
- **Large HTML**: Reduce HTML size, progressive rendering
- **Slow webview update**: Break into multiple smaller updates

## Notes

- Performance timing uses `performance.now()` for high-precision measurement
- Times are in milliseconds with 2 decimal places
- All major operations are timed end-to-end
- Nested operations show breakdown of parent operation
