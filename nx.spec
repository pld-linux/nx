# TODO
# - the x11 libraires packaged to %{_libdir}/NX aren't used, still links (without rpath) to system xorg libs
#   so get rid of the copies or make link with them!
%define		agent_minor	9
%define		auth_minor	1
%define		comp_minor	2
%define		compext_minor	1
%define	 	compshad_minor	2
%define		proxy_minor	1
%define		X11_minor	2
%define		scripts_minor	1
%define		ssh_minor	2
Summary:	NoMachine NX is the next-generation X compression scheme
Summary(pl.UTF-8):	NoMachine NX to schemat kompresji nowej generacji dla X
Name:		nx
Version:	3.5.0
Release:	5
License:	GPL
Group:		Libraries
#SourceDownload: http://www.nomachine.com/sources.php
Source0:	http://64.34.173.142/download/%{version}/sources/%{name}-X11-%{version}-%{X11_minor}.tar.gz
# Source0-md5:	12060433a74ac61a1c776d1d6d136117
Source1:	http://64.34.173.142/download/%{version}/sources/%{name}agent-%{version}-%{agent_minor}.tar.gz
# Source1-md5:	54f7391e457c2aa765a30f322ee68397
Source2:	http://64.34.173.142/download/%{version}/sources/%{name}auth-%{version}-%{auth_minor}.tar.gz
# Source2-md5:	cf38ec1e5a5f6453946cd387c14f2684
Source3:	http://64.34.173.142/download/%{version}/sources/%{name}proxy-%{version}-%{proxy_minor}.tar.gz
# Source3-md5:	488bb4d9b8e9f82dc272b4e6e9c57d30
Source4:	http://64.34.173.142/download/%{version}/sources/%{name}comp-%{version}-%{comp_minor}.tar.gz
# Source4-md5:	ad8c0f133122c6d07732ca69c8759410
Source5:	http://64.34.173.142/download/%{version}/sources/%{name}compext-%{version}-%{compext_minor}.tar.gz
# Source5-md5:	abde2ccc33e31fc695031c2cfb60f3dd
Source6:	http://64.34.173.142/download/%{version}/sources/%{name}compshad-%{version}-%{compshad_minor}.tar.gz
# Source6-md5:	90a762dd9eb19c8c97876ad837923857
Source7:	http://64.34.173.142/download/%{version}/sources/%{name}scripts-%{version}-%{scripts_minor}.tar.gz
# Source7-md5:	17712cc9e9aff58f9fd22bf670a4a98b
Source8:	http://64.34.173.142/download/%{version}/sources/%{name}ssh-%{version}-%{ssh_minor}.tar.gz
# Source8-md5:	f52fcdb38e09f8dcfb9ff0344dfbbbd6
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
Requires:	xorg-font-font-cursor-misc
Requires:	xorg-font-font-misc-misc
Requires:	xorg-font-font-misc-misc-base
Provides:	nx-X11
Obsoletes:	nxcomp
Obsoletes:	nxcompext
Obsoletes:	nxcompshad
Obsoletes:	nxproxy
Obsoletes:	nxssh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't satisfy xorg deps for the rest of the distro
%define		_noautoprovfiles	%{_libdir}/NX

# and as we don't provide them, don't require either
%define		_noautoreq		libX11.so libXcomposite.so libXdamage.so libXext.so libXfixes.so libXpm.so libXrandr.so libXrender.so libXtst.so libXcomp.so libXcompext.so libXcompshad.so

# so check gets really confused in here
%define		no_install_post_check_so	1

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

%description -l pl.UTF-8
NoMachine NX to schemat kompresji dla X nowej generacji. Działa na
zdalnych sesjach X11 nawet przy prędkosci 56k albo większej.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8
%patch0 -p1
%patch1 -p1
%patch2 -p0

cat <<EOF >>nx-X11/config/cf/host.def
#define UseRpath YES
#define UsrLibDir %{_libdir}/NX
EOF

%build
export CFLAGS="%{rpmcflags} -fPIC -DPIC"
export CXXFLAGS="%{rpmcflags} -fPIC -DPIC"
export CPPFLAGS="%{rpmcflags} -fPIC -DPIC"
export LDFLAGS="%{rpmldflags} -Wl,-rpath,%{_libdir}/NX"

perl -pi -e"s|CXXFLAGS=.-O.*|CXXFLAGS=\"$CXXFLAGS\"|" */configure

# build Compression Library and Proxy
for i in nxcomp nxcompshad nxproxy; do
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
cd ..

# build
cd nxssh
%configure \
	PERL=%{__perl} \
	--with-dns \
	--with-pam \
	--with-mantype=man \
	--with-md5-passwords \
	--with-ipaddr-display \
	%{?with_libedit:--with-libedit} \
	--with-4in6 \
	--disable-suid-ssh \
	--with-tcp-wrappers \
	%{?with_ldap:--with-libs="-lldap -llber"} \
	%{?with_ldap:--with-cppflags="-DWITH_LDAP_PUBKEY"} \
	%{?with_kerberos5:--with-kerberos5=%{_prefix}} \
	--with-privsep-path=%{_privsepdir} \
	--with-pid-dir=%{_localstatedir}/run \
	--with-xauth=%{_bindir}/xauth \
	--enable-utmpx \
	--enable-wtmpx

echo '#define LOGIN_PROGRAM                "/bin/login"' >>config.h
%{__make} nxssh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/{pkgconfig,NX},%{_bindir}}

# X11
install nx-X11/lib/X11/libX11.so.* \
	nx-X11/lib/Xcomposite/libXcomposite.so.* \
	nx-X11/lib/Xdamage/libXdamage.so.* \
	nx-X11/lib/Xext/libXext.so.* \
	nx-X11/lib/Xfixes/libXfixes.so.* \
	nx-X11/lib/Xpm/libXpm.so.* \
	nx-X11/lib/Xrandr/libXrandr.so.* \
	nx-X11/lib/Xrender/libXrender.so.* \
	nx-X11/lib/Xtst/libXtst.so.* \
		$RPM_BUILD_ROOT%{_libdir}/NX

install nx-X11/programs/Xserver/nxagent $RPM_BUILD_ROOT%{_bindir}
install nx-X11/programs/nxauth/nxauth $RPM_BUILD_ROOT%{_bindir}

# Compression Libraries
install nxcomp/libXcomp.so.* \
	nxcompext/libXcompext.so.* \
	nxcompshad/libXcompshad.so.* \
		$RPM_BUILD_ROOT%{_libdir}/NX

# proxy
install nxproxy/nxproxy $RPM_BUILD_ROOT%{_bindir}

# nxssh
install nxssh/nxssh $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc nxscripts/*
%attr(755,root,root) %{_bindir}/nxagent
%attr(755,root,root) %{_bindir}/nxauth
%attr(755,root,root) %{_bindir}/nxproxy
%attr(755,root,root) %{_bindir}/nxssh
%dir %{_libdir}/NX
%attr(755,root,root) %{_libdir}/NX/*.so.*
