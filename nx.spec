# TODO:
# - build packages from separate specs where possible
# - use optflags where missing
Summary:	NoMachine NX is the next-generation X compression scheme
Summary(pl):	NoMachine NX to schemat kompresji nowej generacji dla X
Name:		nx
Version:	1.4.0
Release:	0.1
License:	GPL
Group:		Libraries
#SourceDownload: http://www.nomachine.com/download/snapshot/nxsources/
Source0:	http://www.nomachine.com/download/nxsources/nxproxy/%{name}proxy-%{version}-2.tar.gz
#Source0-md5:	15d89810730c7ed0e669b5525e5f3620
Source1:	http://www.nomachine.com/download/nxsources/nxcomp/%{name}comp-%{version}-29.tar.gz
#Source1-md5:	cf17be978269ff0fc69de94c633ec5b2
Source2:	http://www.nomachine.com/download/nxsources/nxcompext/%{name}compext-%{version}-3.tar.gz
#Source2-md5:	ab12f1f32329f5da0f53dd0969fe897e
Source3:	http://www.nomachine.com/download/nxsources/nx-X11/%{name}-X11-%{version}-6.tar.gz
#Source3-md5:	3ac35266d47e3bb98506c851fa0c7959
Source4:	http://www.nomachine.com/download/nxsources/nxagent/%{name}agent-%{version}-63.tar.gz
#Source4-md5:	a325d4e325d950a65f0bee515f7c9f18
Source5:	http://www.nomachine.com/download/nxsources/nxauth/%{name}auth-%{version}-1.tar.gz
#Source5-md5:	ea3b8b2b1b31c8cb33b47821ee1958a3
Source6:	http://www.nomachine.com/download/nxsources/nxviewer/%{name}viewer-%{version}-4.tar.gz
#Source6-md5:	629f90c1f8ef50517e8b1de2c30adcb4
Source7:	http://www.nomachine.com/download/nxsources/nxdesktop/%{name}desktop-%{version}-57.tar.gz
#Source7-md5:	0d2571d70c7ed39ad566d8d3daecfd22
URL:		http://www.nomachine.com/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
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

%build
cd nxcomp
%configure
%{__make}
cd ../nxproxy
%configure
%{__make}
cd ../nx-X11
%{__make} World
cd ../nxcompext
%configure
%{__make}
cd ../nxviewer
xmkmf -a
cp -a /usr/X11R6/%{_lib}/libXp.so* ../nx-X11/exports/lib
%{__make}
%{__make} install DESTDIR=../
cd ../nxdesktop
./configure \
	--prefix=/usr \
	--sharedir=%{_libdir}/NX
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/NX/lib,%{_bindir}}

cp -a nx-X11/lib/X11/libX11.so* \
	nx-X11/lib/Xext/libXext.so* \
	nx-X11/lib/Xrender/libXrender.so.* \
	nxcomp/libXcomp.so.* \
	nxcompext/libXcompext.so* \
	$RPM_BUILD_ROOT%{_libdir}/NX/lib
cp -a nxproxy/nxproxy \
	nxviewer/nxviewer/nxviewer \
	nxviewer/nxpasswd/nxpasswd \
	nxdesktop/nxdesktop \
	nx-X11/programs/Xserver/nxagent \
	$RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
grep -qs "^%{_libdir}/NX/lib$" /etc/ld.so.conf
[ $? -ne 0 ] && echo "%{_libdir}/NX/lib" >> /etc/ld.so.conf
/sbin/ldconfig

%postun
if [ "$1" = "0" ]; then
	umask 022
	grep -v "%{_libdir}/NX/lib" /etc/ld.so.conf > /etc/ld.so.conf.new
	mv -f /etc/ld.so.conf.new /etc/ld.so.conf
fi
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/NX
%dir %{_libdir}/NX/lib
%attr(755,root,root) %{_libdir}/NX/lib/*
