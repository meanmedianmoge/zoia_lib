# Flatpak Instructions for zoia-lib

## Building and Running Locally (Experimental)

To build and run the Flatpak locally, ensure you have Flatpak and `flatpak-builder` installed, then install the matching runtime branch:

```bash
flatpak install flathub org.kde.Platform//6.10 org.kde.Sdk//6.10
```

The Flatpak build installs the vendored `NodeGraphQt` wheel from `tools/nodegraph/`, so it does not need to clone a separate dependency repository.

1. **Build the Flatpak**:
    ```bash
    flatpak-builder --force-clean --install-deps-from=flathub build-dir tools/flatpak/io.github.meanmedianmoge.zoia_lib.yml
    ```

2. **Run the Application**:
    ```bash
    flatpak-builder --run build-dir tools/flatpak/io.github.meanmedianmoge.zoia_lib.yml zoia-librarian
    ```
