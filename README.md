# Quran Memorization Assistant (QMA)

**A desktop application to help you memorize the Quran (Hifdh) with intelligent repetition and progress tracking.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Release](https://img.shields.io/github/v/release/bouness/Quran-Memorization-Assistant)](https://github.com/bouness/Quran-Memorization-Assistant/releases/latest)
[![Build Status](https://img.shields.io/github/actions/workflow/status/bouness/Quran-Memorization-Assistant/main.yml?branch=main)](https://github.com/bouness/Quran-Memorization-Assistant/actions)

## 📖 Overview

The Quran Memorization Assistant is a Python-based desktop application designed to make the process of memorizing the Quran (Hifdh) more structured, efficient, and personalized. It helps you manage your revision, track your memorization progress, and set daily goals.

Ready‑to‑use installers are automatically built by GitHub Actions and published on the [**Releases page**](https://github.com/bouness/Quran-Memorization-Assistant/releases/latest). You can also run the application directly from the source code.

## ✨ Features

*   **Structured Memorization:** Break down the Quran into manageable portions (Juz, Surah, Ayah) and track mastery.
*   **Intelligent Revision Scheduling:** Spaced‑repetition system (SRS) to schedule verses for review at optimal intervals.
*   **Progress Tracking:** Visualize your memorization journey – what’s mastered, due for review, and overall progress.
*   **Customizable Goals:** Set daily or weekly memorization and revision targets.
*   **Offline Audio Support:** Load your preferred recitations from local audio files (MP3) – see [Audio Setup](#-audio-setup) below.
*   **Cross‑Platform:** Run from source on Windows, macOS, and Linux.

## 🚀 Download & Install

The easiest way to get started is to download the latest installer from the [**Releases page**](https://github.com/bouness/Quran-Memorization-Assistant/releases/latest).

*   **For Windows:** Download `QMAInstaller.exe` and run it. Follow the installation wizard.
*   **For other platforms:** Run from source (see below) or use the portable build scripts.

## 🎵 Audio Setup

The application plays Ayat audio to aid memorization. You need to provide your own audio files, organised in a specific folder structure.

### Folder Structure

*   Create a **root folder** for all your Quran audio, e.g., `~/MyQMAAudio` (on Linux/macOS) or `C:\MyQMAAudio` (on Windows).
*   Inside this root folder, create one **subfolder for each reciter** you want to use. Name the subfolder with the reciter's name (e.g., `Fares_Abaad`, `Yassin_Al-Jazaery`).
*   In each reciter subfolder, place the audio files exactly as downloaded from the source (usually named like `001001.mp3` for Surah 1, Ayah 1).

Example structure:
```
~/MyQMAAudio/
├── Fares_Abaad/
│   ├── 001001.mp3
│   ├── 001002.mp3
│   └── ...
├── Yassin_Al-Jazaery/
│   ├── 001001.mp3
│   ├── 001002.mp3
│   └── ...
└── ... (other reciters)
```

### Downloading Audio

1.  Visit [https://everyayah.com/recitations_ayat.html](https://everyayah.com/recitations_ayat.html).
2.  Choose a reciter and download the ZIP file for the **entire Quran** (usually named after the reciter, e.g., `Fares_Abaad.zip`).
3.  Extract the ZIP contents **directly into your root folder** (`~/MyQMAAudio`). The extraction will create a folder named after the reciter containing all the MP3 files.
4.  Repeat for any other reciters you wish to add.

### Loading Audio in the App

*   **If you installed using the Windows installer:** You may also place reciter folders directly into the installation path under `assets/audio` (e.g., `C:\Program Files\QMA\assets\audio\Fares_Abaad`). The app will look there by default.
*   **In the application:** Go to **Settings** and click the **"Browse"** button. Navigate to and select your **root audio folder** (e.g., `~/MyQMAAudio` or `C:\MyQMAAudio`). The app will automatically detect all reciter subfolders and allow you to switch between them.

> **Note:** The app does not scan individual reciter folders; you must point it to the parent folder that contains all reciter subfolders.

## 🖥️ Running from Source

### Prerequisites
*   Python 3.7 or higher
*   `pip` package manager

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bouness/Quran-Memorization-Assistant.git
    cd Quran-Memorization-Assistant
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

## 🛠️ Building from Source

You can create your own standalone executable using the provided scripts.

*   **Windows:** Run `build.bat` – this uses Inno Setup (configured in `app.iss`) to create an installer in the `installer` folder.
*   **macOS / Linux:** Run `./build.sh` to prepare the package.

The build process is also automated via **GitHub Actions** – every push to the main branch triggers a fresh build and publishes the installer to the Releases page.

## 📁 Repository Structure

*   `app.py` – Main application entry point.
*   `configs.py` – Configuration and user settings handling.
*   `version.py` – Current version number.
*   `requirements.txt` – Python dependencies.
*   `assets/` – Icons, images, and UI resources (also the default audio folder location).
*   `installer/` – Contains the generated Windows installer.
*   `build.bat` / `build.sh` – Build scripts.
*   `app.iss` – Inno Setup script for Windows installer.
*   `.github/workflows/` – CI/CD pipeline definitions.

## 🤝 Contributing

Contributions are welcome! Feel free to:
1.  Fork the repository.
2.  Create a feature branch.
3.  Commit your changes.
4.  Push and open a Pull Request.

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

*   Audio files courtesy of [EveryAyah.com](https://everyayah.com).
*   Built with Python and its amazing ecosystem.

