# TODO
# - the x11 libraires packaged to %{_libdir}/NX aren't used, still links (without rpath) to system xorg libs
#   so get rid of the copies or make link with them!
%define		agent_minor	7
%define		auth_minor	1
%define		comp_minor	2
%define		compext_minor	1
%define	 	compshad_minor	2
%define		proxy_minor	1
%define		win_minor	2
%define		X11_minor	2
Summary:	NoMachine NX is the next-generation X compression scheme
Summary(pl.UTF-8):	NoMachine NX to schemat kompresji nowej generacji dla X
Name:		nx
Version:	3.5.0
Release:	1
License:	GPL
Group:		Libraries
#SourceDownload: http://www.nomachine.com/sources.php
Source0:	http://web04.nomachine.com/download/%{version}/sources/%{name}-X11-%{version}-%{X11_minor}.tar.gz
# Source0-md5:	12060433a74ac61a1c776d1d6d136117
Source1:	http://web04.nomachine.com/download/%{version}/sources/%{name}agent-%{version}-%{agent_minor}.tar.gz
# Source1-md5:	0a36c7e6a86c6c741179464b8f79c487
Source2:	http://web04.nomachine.com/download/%{version}/sources/%{name}auth-%{version}-%{auth_minor}.tar.gz
# Source2-md5:	cf38ec1e5a5f6453946cd387c14f2684
Source3:	http://web04.nomachine.com/download/%{version}/sources/%{name}proxy-%{version}-%{proxy_minor}.tar.gz
# Source3-md5:	488bb4d9b8e9f82dc272b4e6e9c57d30
Source4:	http://web04.nomachine.com/download/%{version}/sources/%{name}comp-%{version}-%{comp_minor}.tar.gz
# Source4-md5:	ad8c0f133122c6d07732ca69c8759410
Source5:	http://web04.nomachine.com/download/%{version}/sources/%{name}compext-%{version}-%{compext_minor}.tar.gz
# Source5-md5:	abde2ccc33e31fc695031c2cfb60f3dd
Source6:	http://web04.nomachine.com/download/%{version}/sources/%{name}compshad-%{version}-%{compshad_minor}.tar.gz
# Source6-md5:	90a762dd9eb19c8c97876ad837923857
Source7:	http://web04.nomachine.com/download/%{version}/sources/%{name}win-%{version}-%{win_minor}.tar.gz
# Source7-md5:	84c7f1575d9a1506370125ed050514ab
Patch0:		nx-optflags.patch
Patch1:		nx-syslibs.patch
Patch2:		nx-libpng15.patch
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
BuildRequires:	xorg-cf-files
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-util-imake
Requires:	nxcomp >= %{version}.%{comp_minor}
Requires:	nxcompext >= %{version}.%{compext_minor}
Requires:	nxcompshad >= %{version}.%{compshad_minor}
Requires:	xorg-font-font-cursor-misc
Requires:	xorg-font-font-misc-misc
Requires:	xorg-font-font-misc-misc-base
Provides:	nx-X11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't satisfy xorg deps for the rest of the distro
%define		_noautoprovfiles	%{_libdir}/NX

# and as we don't provide them, don't require either
%define		_noautoreq libX11.so libXext.so libXrender.so libXcompext.so

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

%description -l pl.UTF-8
NoMachine NX to schemat kompresji dla X nowej generacji. Działa na
zdalnych sesjach X11 nawet przy prędkosci 56k albo większej.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6 -a7
%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
export CFLAGS="%{rpmcflags} -fPIC"
export CXXFLAGS="%{rpmcflags} -fPIC"
export CPPFLAGS="%{rpmcflags} -fPIC"

perl -pi -e"s|CXXFLAGS=.-O.*|CXXFLAGS=\"$CXXFLAGS\"|" */configure

# build Compression Library and Proxy
for i in nxcomp nxproxy nxcompshad; do
	cd $i
	%configure
	%{__make}
	cd ..
done

# build X11 Support Libraries and Agents

%{__make} -C nx-X11 World

# build Extended Compression Library
cd nxcompext
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/{pkgconfig,NX},%{_bindir}}

# X11
install nx-X11/lib/X11/libX11.so.6.2 nx-X11/lib/Xext/libXext.so.6.4 nx-X11/lib/Xrender/libXrender.so.1.2.2 $RPM_BUILD_ROOT%{_libdir}/NX
install nx-X11/programs/Xserver/nxagent $RPM_BUILD_ROOT%{_bindir}

# proxy
install nxproxy/nxproxy $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig %{_libdir}/NX

%postun
/sbin/ldconfig %{_libdir}/NX

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/NX
%attr(755,root,root) %{_libdir}/NX/*.so.*
