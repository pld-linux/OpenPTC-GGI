Summary:	OpenPTC for GGI
Summary(pl):	OpenPTC dla GGI
Name:		OpenPTC-GGI
Version:	0.5.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.gaffer.org/ptc/download/distributions/Unix/%{name}-%{version}.tgz
# Source0-md5:	99a195653435f6749f4d0faec96b51c2
Patch0:		%{name}-acfix.patch
Patch1:		%{name}-gcc3.patch
Patch2:		%{name}-include.patch
Patch3:		%{name}-DESTDIR.patch
URL:		http://www.gaffer.org/ptc/ptc.html
BuildRequires:	Hermes-devel >= 1.2.4
BuildRequires:	autoconf
BuildRequires:	libggi-devel
BuildRequires:	libstdc++-devel >= 2.10.0
Requires:	Hermes >= 1.2.4
Provides:	OpenPTC
Obsoletes:	OpenPTC-x11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prometheus Truecolour (OpenPTC) is a third-generation standard for
cross platform low-level graphics access. A lot of design experience
has gone into it to provide one of the cleanest APIs available for
this kind of purpose.

OpenPTC will provide you with a frame-buffer to draw into. You can
choose that buffer to use a pixel format convenient for you, OpenPTC
will convert it to the video modes on the target platform, using
highly optimised x86 and MMX routines where available. This is
achieved using the HERMES ((c)1998/99 Christian Nentwich et al) pixel
conversion library.

OpenPTC 1.0 is available for X11, GGI (Linux), Win32, DOS and JAVA.
Work for other platforms is in progress. All implementations of PTC
come with full source code and may be used free of charge even in
commercial projects.

%description -l pl
Prometheus Truecolour (OpenPTC) jest trzeci± generacj± standardu dla
wieloplatformowej niskopoziomowej grafiki. Umo¿liwia operacje na
frame-bufferze oraz konwersj± (przy pomocy biblioteki Hermes) na ró¿ne
tryby graficzne.

OpenPTC jest dostêpne dla X11, GGI, Win32, DOS i JAVA.

%package devel
Summary:	OpenPTC development package
Summary(pl):	Pakiet programistyczny dla OpenPTC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	OpenPTC-devel
Obsoletes:	OpenPTC-x11-devel

%description devel
OpenPTC development package.

%description devel -l pl
Pakiet programistyczny dla OpenPTC.

%package static
Summary:	OpenPTC static libraries
Summary(pl):	Biblioteki statyczne dla OpenPTC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	OpenPTC-static
Obsoletes:	OpenPTC-x11-static

%description static
OpenPTC static libraries.

%description static -l pl
Biblioteki statyczne dla OpenPTC.

%package demos
Summary:	OpenPTC demos and examples
Summary(pl):	Programy demonstracyjne i przyk³adowe do OpenPTC
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description demos
OpenPTC demos and examples (executables and sources).

%description demos -l pl
Programy demonstracyjne i przyk³adowe do OpenPTC (pliki wykonywalne i
¼ród³a).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__autoconf}
echo y | \
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find demos examples -name '*.o' | xargs rm -f
cp -rf demos examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
echo '%defattr(644,root,root,755)' > demos.list
find demos examples -type d | \
	sed -e "s@^@%dir %{_examplesdir}/%{name}-%{version}/@" >> demos.list
find demos examples -type f -a ! -perm -100 | \
	sed -e "s@^@%{_examplesdir}/%{name}-%{version}/@" >> demos.list
find demos examples -type f -a -perm -100 | \
	sed -e "s@^@%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/@" >> demos.list

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BUGS DOCUMENTATION README WARNING
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ptc-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/ptc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files demos -f demos.list
%defattr(644,root,root,755)
