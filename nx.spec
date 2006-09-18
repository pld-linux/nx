# TODO:
# - build packages from separate specs where possible
# - use optflags where missing
%define	_agent_minor	93
%define	_auth_minor	3
%define	_desktop_minor	50
%define	_viewer_minor	15
%define	_proxy_minor	2
%define	_X11_minor	31
Summary:	NoMachine NX is the next-generation X compression scheme
Summary(pl):	NoMachine NX to schemat kompresji nowej generacji dla X
Name:		nx
Version:	2.0.0
Release:	2
License:	GPL
Group:		Libraries
#SourceDownload: http://www.nomachine.com/download/snapshot/nxsources/
Source0:	http://web04.nomachine.com/download/%{version}/sources/%{name}-X11-%{version}-%{_X11_minor}.tar.gz
# Source0-md5:	0c63cfdc37658eb74f4a84077b05fe9e
Source1:	http://web04.nomachine.com/download/%{version}/sources/%{name}agent-%{version}-%{_agent_minor}.tar.gz
# Source1-md5:	d08f5872a88902ccecd17312e4255aab
Source2:	http://web04.nomachine.com/download/%{version}/sources/%{name}auth-%{version}-%{_auth_minor}.tar.gz
# Source2-md5:	8385751f7ab9c6407a56e95356030ba4
Source4:	http://web04.nomachine.com/download/%{version}/sources/%{name}desktop-%{version}-%{_desktop_minor}.tar.gz
# Source4-md5:	f55dc97544a061dfa0f099329dcc3f53
Source5:	http://web04.nomachine.com/download/%{version}/sources/%{name}viewer-%{version}-%{_viewer_minor}.tar.gz
# Source5-md5:	0e4b1d546b4b8a0224cd0d200ec88827
Source7:	http://web04.nomachine.com/download/%{version}/sources/%{name}proxy-%{version}-%{_proxy_minor}.tar.gz
# Source7-md5:	b078c19372c82e85667cbbac880fa688
Patch0:		%{name}-X11-libs.patch
Patch1:		%{name}compext-libs.patch
Patch2:		%{name}viewer.patch
Patch3:		%{name}-gcc-4.1.patch
Patch4:		%{name}-fonts.patch
Patch5:	%{name}-system-nxcomp.patch
URL:		http://www.nomachine.com/
#BuildRequires:	Xaw3d-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRequires:	nxcomp-devel >= 2.0.0
BuildRequires:	nxcompext-devel >= 2.0.0
BuildRequires:	xorg-cf-files
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-util-imake
Requires:	xorg-font-font-cursor-misc
Requires:	xorg-font-font-misc-misc-base
Requires:	xorg-font-font-misc-misc
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
%setup -q -c -a1 -a2 -a4 -a5 -a7
%patch0 -p1
#%patch1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1

%build
export CFLAGS="%{rpmcflags} -fPIC"
export CXXFLAGS="%{rpmcflags} -fPIC"
export CPPFLAGS="%{rpmcflags} -fPIC"

cd nx-X11
%{__make} \
	CC="%{__cc}" \
	World

cd ../nxdesktop
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix}
sed -i -e "s|/usr/NX|%{_prefix}|" Makefile
sed -i -e "s|-lX11|-lX11-nx|" Makefile
sed -i -e "s|-lXext|-lXext -L/usr/X11R6/%{_lib}|" Makefile
%{__make}

cd ../nxviewer
ln -s ../nx-X11/config config
ln -s ../nx-X11/exports/ exports
xmkmf -a .
%{__make} \
	EXTRA_LIBRARIES="-L%{_libdir} -L../nx-X11/exports/lib" \
	CC="%{__cc}" \
	World

cd ../nxproxy
%configure
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/pkgconfig,%{_bindir},%{_includedir}/nxcompsh}

# X11
install nx-X11/lib/X11/libX11-nx.so.* \
	nx-X11/lib/Xext/libXext-nx.so.* \
	nx-X11/lib/Xrender/libXrender-nx.so.* \
	$RPM_BUILD_ROOT%{_libdir}
install nx-X11/programs/Xserver/nxagent $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libX{11-nx.so.6,ext-nx.so.6,render-nx.so.1}

# desktop
install nxdesktop/nxdesktop $RPM_BUILD_ROOT%{_bindir}

# viewer
install nxviewer/nxviewer/nxviewer $RPM_BUILD_ROOT%{_bindir}
install nxviewer/nxpasswd/nxpasswd $RPM_BUILD_ROOT%{_bindir}

# proxy
install nxproxy/nxproxy $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
