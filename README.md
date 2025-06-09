# 🔒 FileVault

**A modular terminal-based encrypted file storage and retrieval system with compression, configuration, and TUI support using Questionary.**

---

## 🚀 Features

- **Upload** any file from your system:
  - Compresses it with Zstandard (zstd)
  - Encrypts it with a Fernet key (secured using PBKDF2 + user password)
- **Download** previously uploaded files:
  - Decrypts + decompresses them, restores original content
- **Secure encryption key storage**
  - Key is encrypted and saved; user password required on each run
- **First-time setup**
  - User is prompted to configure upload/download directories and password
- **Interactive TUI using `questionary`**
  - Arrow-key navigation, input validation, and context-sensitive menus

---

## 📂 Project Structure

```plaintext
.filevault_config/
├── config.json         # User config (upload/download dirs)
└── secrets.json        # Salt + encrypted Fernet key (secured)

app/
├── config.py           # Handles config loading, validation, saving
├── uploader.py         # Compression + encryption logic
├── downloader.py       # Decryption + decompression logic
├── vault_app.py        # Main app logic (upload/download interfaces)
└── settings.py         # Singleton-style config access

cli_interface/Questionary/
├── questionary_tui.py      # Main TUI class using Questionary
├── question_bank.py        # Centralized question definitions
├── question_routing.py     # Maps actions to questions and function flows using "Dispatch Map" pattern
└── sequence_functions.py   # Functions executed for each user action

Data/
├── Downloads           # Default downloads folder
├── Uploads             # Default uploads folder
└── Samples             # (Optional) test sample files

encryption_key_generator.py   # Generates + encrypts Fernet key (PBKDF2)
main.py                       # Entry point
```
---

## 🔐 How Encryption Works

1. On first launch:
   - User is prompted for a password.
   - A new Fernet key is generated.
   - The Fernet key is encrypted using a key derived from:
     - The password
     - A random salt
   - The encrypted Fernet key and salt are saved.

2. On subsequent launches:
   - User re-enters the password.
   - The key is re-derived and used to decrypt the saved Fernet key.

3. This Fernet key is then used to encrypt or decrypt user files.

---

## ⚙️ Configuration

- Stored in `.filevault_config/config.json`
- Editable via the app’s "Change configurations" menu.
- Includes:
  - Upload directory
  - Download directory

---

## 📌 Notes
-	Files are encrypted one at a time — no support for folders (yet).
-	Password is not stored anywhere or changeable (yet). If lost, files cannot be recovered.
-	No online dependency — everything is local.
-   If you upload the same file again, it will be overwritten.


## 📦 Dependencies

- `cryptography`
- `zstandard`
- `tqdm`
- `questionary`

Install via:
```bash
pip install -r requirements.txt
```
---

## ▶️ Run the FileVault

To start the application, run:

```
python main.py
```

## ✅ Future work
- Action history log
- Password change flow
- File deduplication
- Argparse CLI, to make the app usable with no TUI.

## 👨‍💻 Author

Built by Mazen Yasser with ❤️ and ☕


If you loved this project and wanted to connect, you can find me on [LinkedIn](https://www.linkedin.com/in/mazen-yasser225/)


