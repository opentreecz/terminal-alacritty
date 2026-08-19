Name:           alacritty
Version:        %{version}
Release:        1%{?dist}
Summary:        A cross-platform, OpenGL terminal emulator
License:        Apache-2.0 OR MIT
URL:            https://alacritty.org
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust >= 1.85.0
BuildRequires:  pkg-config
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  libxcb-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  cmake

Requires:       fontconfig
Requires:       freetype
Requires:       libxcb
Requires:       libxkbcommon

%description
Alacritty is a modern terminal emulator that comes with sensible defaults,
but allows for extensive configuration. By integrating with other
applications, rather than reimplementing their functionality, it manages
to provide a flexible set of features with high performance.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release --locked

%install
# Binary
install -Dm755 target/release/alacritty %{buildroot}%{_bindir}/alacritty

# Desktop file
install -Dm644 extra/linux/Alacritty.desktop %{buildroot}%{_datadir}/applications/Alacritty.desktop

# App icon
install -Dm644 extra/logo/alacritty-term.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/Alacritty.svg

# Man pages
install -Dm644 extra/man/alacritty.1.scd %{buildroot}%{_mandir}/man1/alacritty.1
install -Dm644 extra/man/alacritty-msg.1.scd %{buildroot}%{_mandir}/man1/alacritty-msg.1
install -Dm644 extra/man/alacritty.5.scd %{buildroot}%{_mandir}/man5/alacritty.5
install -Dm644 extra/man/alacritty-bindings.5.scd %{buildroot}%{_mandir}/man5/alacritty-bindings.5

# Shell completions
install -Dm644 extra/completions/alacritty.bash %{buildroot}%{_datadir}/bash-completion/completions/alacritty
install -Dm644 extra/completions/alacritty.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/alacritty.fish
install -Dm644 extra/completions/_alacritty %{buildroot}%{_datadir}/zsh/site-functions/_alacritty

# Terminfo
install -Dm644 extra/alacritty.info %{buildroot}%{_datadir}/terminfo/a/alacritty

%files
%license LICENSE-APACHE LICENSE-MIT
%doc README.md CHANGELOG.md
%{_bindir}/alacritty
%{_datadir}/applications/Alacritty.desktop
%{_datadir}/icons/hicolor/scalable/apps/Alacritty.svg
%{_mandir}/man1/alacritty.1*
%{_mandir}/man1/alacritty-msg.1*
%{_mandir}/man5/alacritty.5*
%{_mandir}/man5/alacritty-bindings.5*
%{_datadir}/bash-completion/completions/alacritty
%{_datadir}/fish/vendor_completions.d/alacritty.fish
%{_datadir}/zsh/site-functions/_alacritty
%{_datadir}/terminfo/a/alacritty

%changelog
* Mon Jan 01 2024 Alacritty Maintainers <maintainers@alacritty.org> - %{version}-1
- Initial RPM package build via GitHub Actions
