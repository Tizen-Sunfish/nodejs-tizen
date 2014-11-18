## Basic Descriptions of this package
Name:       nodejs
Summary:    Node.js Event IO engine for V8 JavaScript
Version:		0.11
Release:    14
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
Node.js port for Tizen

## Preprocess script
%prep
# setup: to unpack the original sources / -q: quiet
# patch: to apply patches to the original sources
%setup -q

## Build script
%build
./configure --without-snapshot --with-arm-float-abi=soft
make -j8

## Install script
%install
chmod 777 /usr/bin
make install

# install license file
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}

## Postprocess script
%post 

## Binary Package: File list
%files
%manifest nodejs.manifest
/usr/bin/node
/usr/share/license/%{name}
