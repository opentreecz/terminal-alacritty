# Packaging Guide

This document describes how Linux distribution packages (.deb, .rpm, .pkg.tar.zst) are built and released for Alacritty.

## Overview

Alacritty provides automated package builds for:

| Format | Distributions | Architectures |
|--------|--------------|---------------|
| `.deb` | Debian, Ubuntu, Linux Mint, Pop!_OS | amd64, arm64, armhf |
| `.rpm` | Fedora, RHEL, CentOS, openSUSE | x86_64, aarch64, armv7hl |
| `.pkg.tar.zst` | Arch Linux, Manjaro, EndeavourOS | x86_64, aarch64, armv7h |

## Release Triggers

Packages are automatically built when:

1. **Tag push** - A git tag matching `v[0-9]+.[0-9]+.[0-9]+*` is pushed (e.g., `v1.0.0`, `v1.2.3-rc1`)
2. **Release publish** - A GitHub Release is published via the UI
3. **Manual dispatch** - Triggered manually via GitHub Actions UI (for testing)

## Where to Find Artifacts

After a successful build, all packages are uploaded to the corresponding **GitHub Release** page:

```
https://github.com/opentreecz/terminal-alacritty/releases/tag/v<VERSION>
```

Each release includes:
- `alacritty_<VERSION>_amd64.deb`
- `alacritty_<VERSION>_arm64.deb`
- `alacritty_<VERSION>_armhf.deb`
- `alacritty-<VERSION>-1.<dist>.<arch>.rpm`
- `alacritty-<VERSION>-1-<arch>.pkg.tar.zst`
- `SHA256SUMS.txt` (checksums for all artifacts)

## Package Contents

All packages include:

- `/usr/bin/alacritty` - Main binary
- `/usr/share/applications/Alacritty.desktop` - Desktop entry
- `/usr/share/icons/hicolor/scalable/apps/Alacritty.svg` - Application icon
- `/usr/share/man/man1/alacritty.1` - Man page
- `/usr/share/man/man1/alacritty-msg.1` - Man page for alacritty-msg
- `/usr/share/man/man5/alacritty.5` - Configuration man page
- `/usr/share/man/man5/alacritty-bindings.5` - Key bindings man page
- `/usr/share/bash-completion/completions/alacritty` - Bash completion
- `/usr/share/fish/vendor_completions.d/alacritty.fish` - Fish completion
- `/usr/share/zsh/*/alacritty` - Zsh completion
- `/usr/share/terminfo/a/alacritty` - Terminfo entry

## Runtime Dependencies

| Debian/Ubuntu | Fedora/RHEL | Arch Linux |
|---------------|-------------|------------|
| libfontconfig1 | fontconfig | fontconfig |
| libfreetype6 | freetype | freetype2 |
| libxcb-xfixes0 | libxcb | libxcb |
| libxkbcommon0 | libxkbcommon | libxkbcommon |

## Building Packages Locally

### Prerequisites

- Rust >= 1.85.0 (install via [rustup](https://rustup.rs))
- Build dependencies for your distribution (see `packaging/debian/control` or `packaging/rpm/alacritty.spec`)

### Build .deb locally

```bash
# Install dependencies (Debian/Ubuntu)
sudo apt-get install pkg-config libfontconfig1-dev libfreetype6-dev \
  libxcb-xfixes0-dev libxkbcommon-dev

# Build the binary
cargo build --release --locked

# Create the package (adjust version/arch)
VERSION=1.0.0
ARCH=amd64
PKG_DIR="alacritty_${VERSION}_${ARCH}"
mkdir -p "${PKG_DIR}/DEBIAN" "${PKG_DIR}/usr/bin"
cp target/release/alacritty "${PKG_DIR}/usr/bin/"
# ... (see .github/workflows/release-packages.yml for full steps)
dpkg-deb --build "${PKG_DIR}"
```

### Build .rpm locally

```bash
# Install dependencies (Fedora)
sudo dnf install rust cargo pkg-config fontconfig-devel freetype-devel \
  libxcb-devel libxkbcommon-devel cmake rpm-build

# Build and use rpmbuild with the spec file
cargo build --release --locked
rpmbuild -bb packaging/rpm/alacritty.spec
```

### Build Arch package locally

```bash
# Install dependencies
sudo pacman -S rust pkg-config fontconfig freetype2 libxcb libxkbcommon cmake

# Build with makepkg
cd packaging/arch
makepkg -sf
```

## Testing the Workflow

To test the release workflow without creating a real release:

1. Go to **Actions** > **Release Linux Packages**
2. Click **Run workflow**
3. Enter a version number (e.g., `0.0.1-test`)
4. Click **Run workflow**

Artifacts will be available for download from the workflow run (not attached to a release).

## Dependabot

This project uses [Dependabot](https://docs.github.com/en/code-security/dependabot) to keep dependencies up to date:

- **Cargo dependencies** - Checked weekly (Mondays), grouped into a single PR
- **GitHub Actions** - Checked weekly (Mondays), grouped into a single PR

### Reviewing Dependabot PRs

1. Check the PR description for changelog/compatibility notes
2. Ensure CI passes (the existing CI workflow runs tests)
3. Merge if all checks pass

## Troubleshooting

### Common Build Failures

| Issue | Solution |
|-------|----------|
| Cross-compilation linker error | Ensure the correct cross-compiler is installed (e.g., `gcc-aarch64-linux-gnu`) |
| Missing pkg-config dependency | Install the `-dev` / `-devel` package for the missing library |
| Cargo.lock out of sync | Run `cargo update` and commit the updated lock file |
| QEMU timeout on armhf | armhf builds are emulated and may be slow; increase timeout if needed |

### Architecture Notes

- **amd64/x86_64**: Native build, fastest
- **arm64/aarch64**: Cross-compiled using `aarch64-linux-gnu-gcc`
- **armhf/armv7h**: Cross-compiled using `arm-linux-gnueabihf-gcc`; may be slow under QEMU emulation

## Packaging File Locations

```
packaging/
├── arch/
│   └── PKGBUILD          # Arch Linux package definition
├── debian/
│   ├── compat            # Debhelper compatibility level
│   ├── control           # Package metadata and dependencies
│   ├── copyright         # License information
│   └── rules             # Build rules
└── rpm/
    └── alacritty.spec    # RPM specification file
```

## Workflow File

The main workflow file is located at:
```
.github/workflows/release-packages.yml
```
