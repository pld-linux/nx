# TODO:
# - build packages from separate specs where possible
# - use optflags where missing
%define	_agent_minor	93
%define	_auth_minor	1
%define	_compext_minor	16
%define	_comp_minor	65
%define	_desktop_minor	75
%define	_viewer_minor	14
%define	_proxy_minor	9
%define	_X11_minor	15
Summary:	NoMachine NX is the next-generation X compression scheme
Summary(pl):	NoMachine NX to schemat kompresji nowej generacji dla X
Name:		nx
Version:	1.5.0
Release:	0.1
License:	GPL
Group:		Libraries
#SourceDownload: http://www.nomachine.com/download/snapshot/nxsources/
Source0:	http://web04.nomachine.com/download/%{version}/sources/%{name}-X11-%{version}-%{_X11_minor}.tar.gz
# Source0-md5:	920b4debd9006b759c2dc7fa49827b9d
Source1:	http://web04.nomachine.com/download/%{version}/sources/%{name}agent-%{version}-%{_agent_minor}.tar.gz
# Source1-md5:	5fbc1bec79c1f7b175f9c3d22c7a4b4b
Source2:	http://web04.nomachine.com/download/%{version}/sources/%{name}auth-%{version}-%{_auth_minor}.tar.gz
# Source2-md5:	a7c5e68e9678cb5c722c334b33baf660
Source3:	http://web04.nomachine.com/download/%{version}/sources/%{name}compext-%{version}-%{_compext_minor}.tar.gz
# Source3-md5:	8608a76bb9852c9bea8aedeba5cd1158
Source4:	http://web04.nomachine.com/download/%{version}/sources/%{name}desktop-%{version}-%{_desktop_minor}.tar.gz
# Source4-md5:	cf26ce98b879bcd7eae8ad26d32d079a
Source5:	http://web04.nomachine.com/download/%{version}/sources/%{name}viewer-%{version}-%{_viewer_minor}.tar.gz
# Source5-md5:	8d2246c016e8ac01b6c539cad792cd27
Source6:	http://web04.nomachine.com/download/%{version}/sources/%{name}comp-%{version}-%{_comp_minor}.tar.gz
# Source6-md5:	cab094a88acb299cc1e89dfb2c6a95eb
Source7:	http://web04.nomachine.com/download/%{version}/sources/%{name}proxy-%{version}-%{_proxy_minor}.tar.gz
# Source7-md5:	d2e3c1a109db336dfa497f4c2004f2d5
Patch0:		%{name}-X11-libs.patch
Patch1:		%{name}compext-libs.patch
Patch2:		%{name}viewer.patch
URL:		http://www.nomachine.com/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	which
Requires:	XFree86
Provides:	nx-X11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

%description -l pl
NoMachine NX to schemat kompresji dla X nowej generacji. Dzia³a na
zdalnych sesjach X11 nawet przy prêdkosci 56k albo wiêkszej.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6 -a7
%patch0
%patch1
%patch2

%build
export CFLAGS="%{rpmcflags} -fPIC"
export CXXFLAGS="%{rpmcflags} -fPIC"
export CPPFLAGS="%{rpmcflags} -fPIC"

cd nxcomp
%configure
%{__make}

cd ../nxcompext
%configure
perl -pi -e "s|LDFLAGS     = |LDFLAGS = -fPIC -L/usr/X11R6/%{_lib}|" Makefile
%{__make}

cd ../nx-X11
%{__make} World

cd ../nxdesktop
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix}
perl -pi -e "s|/usr/NX|%{_prefix}|" Makefile
perl -pi -e "s|-lX11|-lX11-nx|" Makefile
perl -pi -e "s|-lXext|-lXext -L/usr/X11R6/%{_lib}|" Makefile
%{__make}

cd ../nxviewer
xmkmf -a
%{__make} World

cd ../nxproxy
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/pkgconfig,%{_bindir},%{_includedir}/nxcompsh}

# comp
install nxcomp/libXcomp.so.* $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libXcomp.so.1

# X11
install nx-X11/lib/X11/libX11-nx.so.* \
	nx-X11/lib/Xext/libXext-nx.so.* \
	nx-X11/lib/Xrender/libXrender-nx.so.* \
	$RPM_BUILD_ROOT%{_libdir}
install nx-X11/programs/Xserver/nxagent $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libX{11-nx.so.6,ext-nx.so.6,render-nx.so.1}

# desktop
install nxdesktop/nxdesktop $RPM_BUILD_ROOT%{_bindir}

# compext
install nxcompext/libXcompext.so.* $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libXcompext.so.1

# viewer
install nxviewer/nxviewer/nxviewer $RPM_BUILD_ROOT%{_bindir}
install nxviewer/nxpasswd/nxpasswd $RPM_BUILD_ROOT%{_bindir}

# proxy
install nxproxy/nxproxy $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
