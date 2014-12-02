%define   _base node
## Basic Descriptions of this package
Name:       node
Summary:    Node.js Event IO Engine for V8 JavaScript
Version:		0.11.14
Release:    1
Group:      System/Libraries
License:    Custom
Source0:    %{name}-%{version}.tar.gz

# Required packages
# Pkgconfig tool helps to find libraries that have already been installed
BuildRequires:  libattr-devel
BuildRequires:	python
BuildRequires:	which
BuildRequires:  pkgconfig(glib-2.0)

## Description string that this package's human users can understand
%description
Node.js port for Tizen 2.2

## Preprocess script
%prep
# setup: to unpack the original sources / -q: quiet
# patch: to apply patches to the original sources
%setup -q

## Build script
%build
%define _node_arch %{nil}
%ifarch x86_64
%define _node_arch x64
%endif
%ifarch i386 i686
%define _node_arch x86
%endif
%ifarch armv7l
%define _node_arch arm
%endif
if [ -z %{_node_arch} ];then
	echo "bad arch"
	exit 1
fi

./configure --without-snapshot --with-arm-float-abi=soft
make binary -j8

pushd $RPM_SOURCE_DIR
mv $RPM_BUILD_DIR/%{_base}-%{version}/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz .
rm -rf %{_base}-v%{version}
tar zxvf %{_base}-v%{version}-linux-%{_node_arch}.tar.gz
popd

## Install script
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

# install license file
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}
rm -rf $RPM_BUILD_ROOT/usr/share/%{_base}js/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz

## Postprocess script
%post 

## Binary Package: File list
%files
%manifest nodejs.manifest
%{_bindir}/node
%{_bindir}/npm
/usr/include/node
/usr/share/license/%{name}
/usr/lib/node_modules
/usr/share/doc/node-v%{version}
/usr/share/man
/usr/share/systemtap/tapset/node.stp
