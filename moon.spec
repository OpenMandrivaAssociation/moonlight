%define name moon
%define version 2.0
%define release %mkrel 1
%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name
%define monover 2.6.1
%define monobasicver 2.6

Summary: Open Source implementation of Silverlight
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ftp.novell.com/pub/mono/sources/moon/moonlight-%{version}.tar.bz2
Source1: http://www.go-mono.com/sources/mono/mono-%monover.tar.bz2
Source2: http://www.go-mono.com/sources/mono-basic/mono-basic-%monobasicver.tar.bz2
Patch: moon-2.0-format-strings.patch
Patch1: moon-2.0-fix-linkage.patch
Patch2: moon-2.0-firefox-3.6-detection.patch
#gw fix building with --no-undefined enabled
Patch5: mono-2.0-fix-linking.patch
Patch8: mono-2.6-format-strings.patch
License: LGPLv2
Group: System/Libraries
Url: http://www.mono-project.com/Moonlight
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: ffmpeg-devel
BuildRequires: libxtst-devel
BuildRequires: libxrandr-devel
%if %mdvver >= 201000
BuildRequires: xulrunner-devel
%else
BuildRequires: xulrunner-devel-unstable
%endif
%if %mdvver >= 200900
BuildRequires: libcairo-devel >= 1.6
BuildRequires: gnome-desktop-sharp-devel
%else
BuildRequires: gnome-desktop-sharp
%endif
BuildRequires: libgtk+2.0-devel
BuildRequires: libmagick-devel
BuildRequires: dbus-glib-devel
BuildRequires: libalsa-devel
BuildRequires: libpulseaudio-devel
BuildRequires: mono-devel
BuildRequires: ndesk-dbus 
BuildRequires: bison
Requires: %libname >= %version

%description
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems. It supports rich browser applications, similar to
Adobe Flash.

%package doc
Summary:	Documentation for %name
Group:		Development/Other
Requires(post): mono-tools >= 1.1.9
Requires(postun): mono-tools >= 1.1.9

%description doc
This package provides API documentation for %name.

%package -n %libname
Group:System/Libraries
Summary: Open Source implementation of Silverlight

%description -n %libname
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems. It supports rich browser applications, similar to
Adobe Flash.

%package -n %develname
Group:Development/C++
Summary: Open Source implementation of Silverlight
Requires: %libname = %version-%release
Provides: lib%name-devel = %version-%release

%description -n %develname
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems. It supports rich browser applications, similar to
Adobe Flash.


%prep
%setup -q -n moonlight-%version -a 1 -a 2
%patch -p1
%patch1 -p1 -b .fix-linking
%if %mdvver >= 201010
%patch2 -p1
%endif
autoreconf -fi
cd mono-%monover
%patch5 -p1 -b .linking
%patch8 -p1 -b .format-strings
autoreconf -fi

%build
cd mono-%monover
%configure2_5x
make
cd ../mono-basic-%monobasicver
export LC_ALL=UTF-8
./configure --prefix=%_prefix
make
cd ..
%configure2_5x \
  --with-ff3=yes \
%if %mdvver >= 200900
  --with-cairo=system \
%endif
 --with-mcspath=`pwd`/mono-%monover/mcs --with-mono-basic-path=`pwd`/mono-basic-%monobasicver

#gw parallel build does not work in 2.0
make

%install
rm -rf %{buildroot}
%makeinstall_std 
mkdir -p %buildroot%_libdir/mozilla/plugins
ln -s %_libdir/moon/plugin/libmoonloader.so %buildroot%_libdir/mozilla/plugins
rm -f %buildroot%_libdir/moon/plugin/README

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%endif

%post doc
%_bindir/monodoc --make-index > /dev/null

%postun doc
if [ "$1" = "0" -a -x %_bindir/monodoc ]; then %_bindir/monodoc --make-index > /dev/null
fi

%files
%defattr(-,root,root)
%doc README TODO
%_bindir/mopen
%_bindir/munxap
%_bindir/mxap
%_bindir/respack
%_bindir/smcs
%_bindir/sockpol
%_bindir/unrespack
%_bindir/xaml2html
%_bindir/xamlg
%_prefix/lib/mono/gac/Moon*
%_prefix/lib/mono/gac/System.Windows.Browser/
%_prefix/lib/mono/gac/System.Windows.Controls/
%_prefix/lib/mono/gac/System.Windows.Controls.Data/
%_prefix/lib/mono/gac/System.Windows
%_libdir/mozilla/plugins/libmoon*
%dir %_prefix/lib/mono/moonlight
%_prefix/lib/mono/moonlight/*.dll
%if %mdvver >= 200900
#gw TODO: put somewhere else
%_libdir/libshocker.so
%endif
%dir %_prefix/lib/moonlight
%dir %_prefix/lib/moonlight/2.0-redist
%_prefix/lib/moonlight/2.0-redist/*
%dir %_prefix/lib/moonlight/2.0
%_prefix/lib/moonlight/2.0/*
%dir %_libdir/moonlight
%_libdir/moonlight/*.exe*
%dir %_libdir/moonlight/plugin
%_libdir/moonlight/plugin/*.*
%_mandir/man1/mopen.1*
%_mandir/man1/mxap.1*
%_mandir/man1/respack.1*
%_mandir/man1/sockpol.1*
%_mandir/man1/svg2xaml.1*
%_mandir/man1/xamlg.1*

%files -n %libname
%defattr(-,root,root)
%_libdir/libmoon.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%_libdir/libmoon.so
%_libdir/*.la
%_datadir/pkgconfig/moonlight*.pc

%files doc
%defattr(-,root,root)
%_prefix/lib/monodoc/sources/moonlight-gtk*
