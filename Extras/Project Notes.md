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