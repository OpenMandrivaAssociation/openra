%define oname OpenRA
%define __noautoreq 'mono\\(StyleCop\\).*'
%define __noautoprov 'mono\\(Mono.Nat\\)|mono\\(ICSharpCode.SharpZipLib\\)'

Name:           openra
Version:        20181215
Release:        1
Url:            http://www.openra.net
Summary:        Recreation of the early Command & Conquer games
License:        GPL-3.0
Group:          Games/Strategy
Source0:         https://github.com/OpenRA/OpenRA/releases/download/release-%{version}/%{oname}-release-%{version}-source.tar.bz2
#Source2:        thirdparty.tar.gz
#Source3:        http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  git
BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info
BuildRequires:  pkgconfig(mono)
BuildRequires:  pkgconfig(lua)

Requires:       %{_lib}SDL2_2.0_1

BuildConflicts:	openra
Requires:       lua5.1
Requires:       mono
Requires:       mono-winforms
Requires:       openal
Requires:       xdg-utils
Requires:       zenity

BuildRequires:  mono(ICSharpCode.SharpZipLib) = 0.86.0.518
Requires:       mono(ICSharpCode.SharpZipLib) = 0.86.0.518

BuildRequires:  mono(Mono.Nat)
Requires:       mono(Mono.Nat)

%description
OpenRA is an Open Source, Real Time Strategy game engine.
Its primary focus is on creating an extendable platform
to recreate games in the style of the early Westwood games.
It ships mods that reimagine Command & Conquer: Tiberian Dawn,
Red Alert as well as Dune 2000 if the original game files are
provided.

%prep
%setup -q

%build

make dependencies
make core
make tools
make docs

%install
make DESTDIR="%{buildroot}" prefix=%{_prefix} install-all
make DESTDIR="%{buildroot}" prefix=%{_prefix} install-linux-shortcuts
make DESTDIR="%{buildroot}" prefix=%{_prefix} install-linux-mime
make DESTDIR="%{buildroot}" prefix=%{_prefix} install-linux-appdata

%check
make test

%clean
make DESTDIR="%{buildroot}" prefix=%{_prefix} uninstall

%files
%doc DOCUMENTATION.md Lua-API.md README.md
%{_bindir}/openra
%{_bindir}/openra-editor
%{_prefix}/lib/openra/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/openra.xml
%{_datadir}/appdata/openra.appdata.xml
