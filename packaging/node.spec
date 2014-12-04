%define _base node
	
Name: %{_base}js
Version: 0.11.14
Release: 1
Summary: A server-side JavaScript environment that uses an asynchronous event-driven model
Packager: Kazuhisa Hara <kazuhisya@gmail.com>
Group: System/Libraries
License: MIT License
URL: http://nodejs.org
Source0: %{url}/dist/v%{version}/%{_base}-v%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-tmp
Prefix: /usr
BuildRequires:  libattr-devel
BuildRequires:	python
BuildRequires:	which
BuildRequires:  pkgconfig(glib-2.0)

%description
Node.js port for Tizen 2.2
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package binary
Summary: Node.js build binary tarballs
Group: Development/Libraries
License: MIT License
URL: http://nodejs.org
%description binary
Node.js port for Tizen 2.2
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.
%package npm
Summary: Node Packaged Modules
Group: Development/Libraries
License: MIT License
URL: http://nodejs.org
Obsoletes: npm
Provides: npm
Requires: nodejs

%description npm
Node.js port for Tizen 2.2
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.
%package devel
Summary: Header files for %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Node.js port for Tizen 2.2
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%prep
rm -rf $RPM_SOURCE_DIR/%{_base}-v%{version}
%setup -q -n %{_base}-v%{version}

%build
%define _node_arch arm
CFLAGS="-fexpensive-optimizations -frename-registers -fomit-frame-pointer -O2"
CXXFLAGS="-fexpensive-optimizations -frename-registers -fomit-frame-pointer -O2 -fpermissive -fvisibility-inlines-hidden"
./configure \
		--dest-cpu=arm \
		--dest-os=linux \
		--with-arm-float-abi=soft \
		--without-snapshot \
		--tag=\
		--prefix=/
make binary %{?_smp_mflags}
pushd $RPM_SOURCE_DIR
mv $RPM_BUILD_DIR/%{_base}-v%{version}/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz .
rm -rf %{_base}-v%{version}
tar zxvf %{_base}-v%{version}-linux-%{_node_arch}.tar.gz
popd
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
cp -Rp $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}/* $RPM_BUILD_ROOT/usr/
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{_base}-v%{version}/
for file in ChangeLog LICENSE README.md ; do
	mv $RPM_BUILD_ROOT/usr/$file $RPM_BUILD_ROOT/usr/share/doc/%{_base}-v%{version}/
done
mkdir -p $RPM_BUILD_ROOT/usr/share/%{_base}js
mv $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz $RPM_BUILD_ROOT/usr/share/%{_base}js/

# prefix all manpages with "npm-"
pushd $RPM_BUILD_ROOT/usr/lib/node_modules/npm/man/
for dir in *; do
	mkdir -p $RPM_BUILD_ROOT/usr/share/man/$dir
	pushd $dir
	for page in *; do
		if [[ $page != npm* ]]; then
			mv $page npm-$page
		fi
	done
	popd
	cp $dir/* $RPM_BUILD_ROOT/usr/share/man/$dir
done
popd

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}

%files
%defattr(-,root,root,-)
%{_prefix}/share/doc/%{_base}-v%{version}
%defattr(755,root,root)
%{_bindir}/node

%doc
/usr/share/man/man1/node.1.gz

%files binary
%defattr(-,root,root,-)
%{_prefix}/share/%{_base}js/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz

%files npm
%defattr(-,root,root,-)
%{_prefix}/lib/node_modules/npm
%{_bindir}/npm

%doc
/usr/share/man/man1/npm*
/usr/share/man/man3
/usr/share/man/man5
/usr/share/man/man7

%files devel
/usr/include/node
/usr/share/systemtap/tapset/node.stp
