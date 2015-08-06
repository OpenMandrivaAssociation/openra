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


Name:           openra
Version:        20150614
Release:        1.1
Url:            http://www.openra.net
Summary:        Recreation of the early Command & Conquer games
License:        GPL-3.0
Group:          Amusements/Games/Strategy/Real Time
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
Requires:       SDL2
%if 0%{?suse_version}
BuildRequires:  lua51
Requires:       lua51
Requires:       freetype2
# workaround System.DllNotFoundException`: libgdiplus.so
Requires:       libgdiplus-devel
%endif
%if 0%{?fedora_version}
BuildRequires:  lua = 5.1
Requires:       lua = 5.1
Requires:       freetype
%endif
Requires:       mono-core
Requires:       mono-winforms
Requires:       openal
Requires:       xdg-utils
Requires:       zenity

BuildRequires:  mono(ICSharpCode.SharpZipLib) = 0.86.0.518
Requires:       mono(ICSharpCode.SharpZipLib) = 0.86.0.518

BuildRequires:  mono(Mono.Nat)
Requires:       mono(Mono.Nat)

# don't provide the bundled dependencies to other packages
AutoReqProv:    off

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

%if 0%{?suse_version}
%fdupes %{buildroot}%{_prefix}/lib
%endif

%check
make test

%clean
make DESTDIR="%{buildroot}" prefix=%{_prefix} uninstall

%post
%desktop_database_post
%icon_theme_cache_post
%mime_database_post

%postun
%desktop_database_postun
%icon_theme_cache_postun
%mime_database_postun

%files
%defattr(-,root,root)
%doc DOCUMENTATION.md Lua-API.md README.md
%{_bindir}/openra
%{_bindir}/openra-editor
%{_prefix}/lib/openra/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/openra.xml
%{_datadir}/appdata/openra.appdata.xml

%changelog
* Sun Jun 14 2015 mailaender@opensuse.org
- release 20150614
