# Simple file uploader ideas, lessons.
----------------------------------------

# Compression Methods Overview

## Lossless vs. Lossy Compression

- **Lossless Compression**  
    - Maintains complete data integrity; no information is lost.
    - Useful when original data must be preserved (e.g., text, code, some images).

- **Lossy Compression**  
    - Reduces file size more than lossless methods.
    - Some data is discarded, potentially reducing quality (common in audio, video, and some image formats).

## Gzip vs. Zip

- **Gzip**
    - Typically achieves better compression ratios than Zip.
    - Designed for compressing single files.
    - Commonly combined with `tar` to create `.tar.gz` ("tarballs") for compressing multiple files or directories.

- **Zip**
    - Allows random access to individual files within the archive without full decompression.
    - Commonly used for compressing and archiving multiple files and directories.
    - Slightly less efficient compression compared to Gzip.

## Extra compression methods
| Format      | Tool/Lib            | Compression Ratio | Speed    |
|-------------|---------------------|-------------------|----------|
| gzip        | gzip, zlib          | Medium            | Fast     |
| bz2         | bz2                 | Better            | Slower   |
| xz          | lzma / xz           | Best (often)      | Slowest  |
| zstandard   | zstandard (Facebook)| Excellent         | Fast     |

## Observations
- **BytesIO Usage**  
    - `BytesIO` is an in-memory file-like object, useful for building file processing pipelines without writing to disk.
    - When using `cctx.stream_writer`, after exiting the `with` block, the stream is closed and the buffer is flushed into the destination (e.g., from a buffer to `BytesIO` in memory).
    - The `closefd` flag can be set to prevent the stream writer from closing the underlying file, allowing further operations.
    - Files have separate read and write pointers; reset the pointer to `0` (e.g., with `seek(0)`) before reading, otherwise you'll be at the end and read nothing.

---

# Lessons & Concepts Learned (Saturday, June 7 2025)

## General Architecture & Design

- **Modular design** using multiple files (`uploader.py`, `downloader.py`, etc.) improves scalability and testability.
- Use of **`FileVaultApp` controller class** to manage vault operations and dependencies (e.g., Fernet).
- Implemented a **dispatch map** to route menu actions to their corresponding logic without using `if`/`match-case`.
- Applied the **Questionary TUI pattern**, separating question definitions (`question_bank`), action routing, and sequence logic.

## Imports & Circular Dependencies

- **Circular Import Errors** occur when two modules import each other. Fix by:
  - Refactoring logic to remove unnecessary imports.
  - Passing shared components (like `question_bank`) as function arguments instead of importing them.
- Avoid tight coupling between input/UI logic and functional logic.

## Encryption & Security

- **Fernet (from `cryptography`)** used for symmetric encryption.
- Keys should be securely generated and stored (`encryption_key.enc`).
- Encryption key injected into the app, not accessed as a global — this is clean dependency management.

## File Compression & Decompression

- Used **Zstandard (zstd)** for efficient, streamable compression.
- Stream compression and decompression via `.stream_writer()` and `.stream_reader()` — avoids memory overload on large files.
- `BytesIO` lets you compress in-memory before encrypting, avoiding disk I/O.
- Always `seek(0)` before reading from a stream you just wrote to.

## TUI Concepts

- **Dispatch maps** (`str → function`) simplify routing from menu options to behavior.
- `questionary.select()` used for interactive menus, `questionary.path()` for file selection.
- Main loop runs in `while True`, calling `ui.run()` — this keeps the app interactive.
- Graceful handling of unimplemented actions with `dict.get()` or fallback functions.

## Python Tooling & Practices

- `pathlib.Path` makes file path handling safer, cross-platform, and object-oriented.
- Organized app layout into `app/`, `cli_interface/`, `data/`, and `keys/` folders.
- Logging actions in `logs.jsonl` prepares the app for history tracking and auditability.
- Colorized terminal output (e.g., `\033[92m`) improves UX with clear status messages.

---
# 📚 Lessons and Concepts Learned (Saturday, June 8 2025)

## 🧠 Path Handling and Cross-Platform CLI UX

- **Pathlib's Path().resolve()** ensures paths are absolute and platform-safe.
- Drag-and-drop file paths into terminals on macOS often enclose the path in single quotes (`'`). Strip these for correctness.
- Always use `Path()` or `Pathlib` for combining paths, not string concatenation.

## 🛠 Configuration Management

- **Dataclasses** are great for representing structured config objects (e.g., `Config`).
- You can validate configuration with methods like `.is_valid()` that iterate through annotated fields.
- Always sanitize user path inputs in CLI apps: check `exists()` and `is_dir()` to avoid invalid configs.
- Config files can be safely stored in a dot-prefixed folder (e.g., `.filevault_config`) to semi-hide them from casual users.
- When saving to disk, always validate user inputs before writing to avoid corrupted config state.

## 🧩 Global Config Access

- Returning both `config` and `config_path` is okay for smaller apps, but...
- The **Module-as-Singleton** pattern (e.g., `from app import settings`) provides a cleaner, Django-like API.
- `settings.configure(...)` followed by `get_config()` lets you access config globally without passing it around everywhere.

## ✅ CLI Flow & Questionary UX

- `questionary.ask()` returns `None` on cancellation (e.g., Ctrl+C). Always check for `None` to prevent crashes.
- Wrapping each prompt in a loop lets you gracefully re-prompt or exit on invalid input.
- You can dynamically generate TUI options (like actions or file lists) by querying the file system at runtime.

## 🧠 General Concepts

- **Singletons** give global access to a single instance of something. In Python, modules themselves act like singletons.
- **Avoid using `globals()` for mutable state** — prefer encapsulated modules or dependency injection.
- **Design patterns** are tools — use them to solve real problems (like managing state), not just for their own sake.
-------------------
