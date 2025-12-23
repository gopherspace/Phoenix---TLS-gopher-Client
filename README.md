# Phoenix - TLS gopher+ Client

Phoenix is a modern, secure gateway to Gopherspace, bridging the gap between classic protocols and contemporary security standards.

## 📖 Documentation

Detailed instructions are available in the following manuals:
*   🇺🇸 [User Manual (English)](USER_MANUAL_EN.txt)
*   🇩🇪 [Benutzerhandbuch (Deutsch)](USER_MANUAL_DE.txt)

## 🛠 Features
*   **🔒 TLS/gophers Support:** Native support for encrypted connections. Simply use `gophers://` for secure browsing.
*   **➕ Gopher+ Metadata:** Detects extended server information, author tags, and alternative file formats.
*   **🌈 enhanced:eXperience:** Advanced color highlighting for Gophermaps using a JSON-based mapping engine.
*   **🔖 Bookmark Management:** Efficiently save and manage your favorite Gopherspace locations locally.
*   **🎨 Dynamic Theme Engine:** Choose from 12 built-in designs to customize your browsing experience.
*   **🌍 Multi-Language:** Full support for 8 languages, including English, German, French, Spanish, and Italian.

## ✨ enhanced:eXperience Support

Phoenix brings color to the classic protocol. By placing an `enhanced.experience` file on a Gopher server, individual lines of a gophermap can be styled.

Available accents: accentblue, green (success), red (danger), orange (warning), blue (header), and grey (secondary).

**Configuration Example (`enhanced.experience`):**
```json
{
  "rules": {
    "0": "header",
    "7": "accent",
    "17": "warning"
  }
}
```
## 🛠 Technical Information

    Author: René Gabel (gopherspace.de)
    Engineering: AI-assisted by Google Gemini
    Build: 2025-Rev1 (Last change: December 23, 2025)

## ⚖️ License

This project is licensed under:

    MIT License & CC BY-NC 4.0
    Copyright (c) 2025 René Gabel / gopherspace.de

Please refer to the LICENSE.txt file for the full legal text.

Enjoy exploring the Gopherspace with Phoenix!
