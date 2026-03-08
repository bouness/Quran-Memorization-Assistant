# Quran Memorization Assistant (QMA)

**A desktop application to help you memorize the Quran (Hifdh) with intelligent repetition and progress tracking.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Release](https://img.shields.io/github/v/release/bouness/Quran-Memorization-Assistant?include_prereleases&sort=semver)](https://github.com/bouness/Quran-Memorization-Assistant/releases/latest)
[![Build Status](https://img.shields.io/github/actions/workflow/status/bouness/Quran-Memorization-Assistant/main.yml?branch=main)](https://github.com/bouness/Quran-Memorization-Assistant/actions)

## 📖 Overview

The Quran Memorization Assistant is a Python-based desktop application designed to make the process of memorizing the Quran (Hifdh) more structured, efficient, and personalized. It helps you manage your revision, track your memorization progress, and set daily goals.

Ready‑to‑use installers are automatically built by GitHub Actions and published on the [**Releases page**](https://github.com/bouness/Quran-Memorization-Assistant/releases/latest). You can also run the application directly from the source code.

## ✨ Features

*   **Structured Memorization:** Break down the Quran into manageable portions (Juz, Surah, Ayah) and track mastery.
*   **Intelligent Revision Scheduling:** Spaced‑repetition system (SRS) to schedule verses for review at optimal intervals.
*   **Progress Tracking:** Visualize your memorization journey – what’s mastered, due for review, and overall progress.
*   **Customizable Goals:** Set daily or weekly memorization and revision targets.
*   **Offline Audio Support:** Load your preferred recitation from local audio files (MP3) – see [Audio Setup](#-audio-setup) below.
*   **Cross‑Platform:** Run from source on Windows, macOS, and Linux.

## 🚀 Download & Install

The easiest way to get started is to download the latest installer from the [**Releases page**](https://github.com/bouness/Quran-Memorization-Assistant/releases/lookup/latest).

*   **For Windows:** Download `QMAInstaller.exe` and run it. Follow the installation wizard.
*   **For other platforms:** Run from source (see below) or use the portable build scripts.

## 🎵 Audio Setup

The application plays Ayat audio to aid memorization. You need to provide your own audio files.

1.  **Download a full Quran recitation** from [https://everyayah.com/recitations_ayat.html](https://everyayah.com/recitations_ayat.html). Choose any reciter you like.
2.  **Extract** the downloaded ZIP archive to a folder on your computer (e.g., `C:\QuranAudio\` or `~/QuranAudio/`).
3.  **Inside the application**, go to **Settings → Audio Folder** and browse to the extracted folder. The app will automatically recognise the files and associate them with the correct verses.

> **Note:** The audio files are expected to be named in a specific format (usually `001001.mp3` for Surah 1, Ayah 1). The folder structure from everyayah.com works out of the box.

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
*   `assets/` – Icons, images, and UI resources.
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

---
