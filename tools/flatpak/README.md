# Flatpak Instructions for zoia-lib

## Building and Running Locally (Experimental)

To build and run the Flatpak locally, ensure you have Flatpak and flatpak-builder installed. Follow these steps:

1. **Build the Flatpak**:
    ```bash
    flatpak-builder --force-clean build-dir tools/flatpak/io.github.meanmedianmoge.zoia_lib.yml
    ```

2. **Run the Application**:
    ```bash
    flatpak-builder --run build-dir tools/flatpak/io.github.meanmedianmoge.zoia_lib.yml zoia-librarian
    ```

Make sure to replace `io.github.meanmedianmoge.zoia_lib.yml` with the correct path to your Flatpak manifest if it differs.  