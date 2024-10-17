#
# spec file for package openra
#
# Copyright (c) 2015 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
%define __noautoreq 'mono\\(StyleCop\\).*'
%define __noautoprov 'mono\\(Mono.Nat\\)|mono\\(ICSharpCode.SharpZipLib\\)'

Name:           openra
Version:        20150614
Release:        1
Url:            https://www.openra.net
Summary:        Recreation of the early Command & Conquer games
License:        GPL-3.0
Group:          Games/Strategy
Source:         OpenRA-%{version}.tar.bz2
Source2:        thirdparty.tar.gz
Source3:        http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  git
BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info
BuildRequires:  pkgconfig(mono)
Requires:       %{_lib}SDL2_2.0_1
BuildRequires:  lua5.1-devel
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
%setup -q -n OpenRA-%{version} -a2
make version

%build
mkdir -p ./thirdparty/download

cp %{SOURCE3} ./thirdparty/download

# support latest SDL 2.0.3
sed -i 's/libSDL2-2.0.so.0/libSDL2-2.0.so.1/' thirdparty/SDL2-CS.dll.config

ln -sf %{_prefix}/lib/mono-nat/Mono.Nat.dll ./thirdparty/download/Mono.Nat.dll
ln -sf %{_prefix}/lib/mono/sharpziplib/ICSharpCode.SharpZipLib.dll ./thirdparty/download/ICSharpCode.SharpZipLib.dll

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
