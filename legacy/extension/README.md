# Development workflow for chat-participants extension

## Quick Development Cycle

### Option 1: Run from Source (Recommended for Development)
Press `F5` in VS Code while in the extension directory to launch Extension Development Host. Changes to `chat_participants.js` will reload automatically.

**Pros:**
- Instant feedback
- No need to rebuild/reinstall
- Just reload the development window (Ctrl+R)

**Cons:**
- Only works in development host window

### Option 2: Rebuild and Install (For Testing in Main VS Code)
```powershell
.\rebuild.ps1
```

Then reload VS Code window (Ctrl+R or Cmd+R).

## Files

- `chat_participants.js` - Main extension code
- `package.json` - Extension manifest
- `rebuild.ps1` - Script to package and install
- `.vscodeignore` - Files to exclude from package (if needed)

## Testing

1. Make changes to `chat_participants.js`
2. For dev testing: Press F5, wait for new window
3. For production testing: Run `.\rebuild.ps1`, reload main window
4. Test @agilebot and @storybot in chat

## Tips

- Use `console.log()` for debugging (shows in Debug Console when running F5)
- Check "Output" panel → "Extension Host" for runtime errors
- VS Code caches extensions - use `--force` flag when reinstalling
- The rebuild script already includes `--force`
