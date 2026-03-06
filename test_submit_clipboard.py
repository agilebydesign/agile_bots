#!/usr/bin/env python3
"""
Test script to verify clipboard + paste-to-Cursor-chat works.
Run from terminal: python test_submit_clipboard.py

Prerequisites: pip install pyperclip pyautogui

Before running: focus Cursor, then run this script. It will:
1. Copy test text to clipboard
2. Wait 1 second (switch to Cursor if needed)
3. Send Ctrl+L (focus chat) then Ctrl+V (paste)
"""
import os
import platform
import sys
import time

TEST_TEXT = "Test from test_submit_clipboard.py - if you see this, clipboard+paste works!"


def main():
    print("=== Clipboard + Cursor Chat Test ===\n")

    # Check IDE env for correct hotkey
    ide = (os.environ.get("IDE") or "").lower()
    cursor = ide == "cursor"
    mac = platform.system().lower() == "darwin"
    print(f"IDE env: {ide or '(not set)'} -> cursor={cursor}")
    print(f"Platform: {platform.system()}")

    try:
        import pyperclip
        import pyautogui
    except ImportError as e:
        print(f"\nERROR: Install deps: pip install pyperclip pyautogui")
        print(f"  {e}")
        sys.exit(1)

    # 1. Copy to clipboard
    print("\n1. Copying test text to clipboard...")
    try:
        pyperclip.copy(TEST_TEXT)
        print("   pyperclip.copy() OK")
    except Exception as e:
        print(f"   FAILED: {e}")
        sys.exit(1)

    # 2. Verify clipboard (optional)
    try:
        got = pyperclip.paste()
        if got == TEST_TEXT:
            print("   Clipboard verify OK")
        else:
            print(f"   WARNING: paste() returned {len(got)} chars, expected {len(TEST_TEXT)}")
    except Exception as e:
        print(f"   Verify failed: {e}")

    # 3. Wait for user to switch to Cursor
    print("\n2. Switching to Cursor in 2 seconds... (focus Cursor window now)")
    time.sleep(2)

    # 4. Focus chat
    print("\n3. Sending focus-chat hotkey...")
    if cursor:
        hotkey = ("command", "l") if mac else ("ctrl", "l")
        print(f"   Cursor: {'Cmd+L' if mac else 'Ctrl+L'}")
    else:
        hotkey = ("ctrl", "command", "i") if mac else ("ctrl", "alt", "i")
        print(f"   VS Code: {'Ctrl+Cmd+I' if mac else 'Ctrl+Alt+I'}")
    pyautogui.hotkey(*hotkey)
    time.sleep(0.5)

    # 5. Paste
    print("\n4. Sending paste...")
    paste_key = ("command", "v") if mac else ("ctrl", "v")
    pyautogui.hotkey(*paste_key)
    time.sleep(0.2)

    print("\nDone. Check Cursor chat - you should see the test text.")
    print("If not: set IDE=cursor and rerun, or focus chat before running.")


if __name__ == "__main__":
    main()
