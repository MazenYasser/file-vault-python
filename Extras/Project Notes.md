# Simple file uploader ideas, lessons.

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