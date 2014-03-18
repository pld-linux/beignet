Summary:	Open source implementation of the OpenCL specification for Intel GPUs
Name:		beignet
Version:	0.8
Release:	0.1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://cgit.freedesktop.org/beignet/snapshot/Release_v%{version}.tar.gz
URL:		http://www.freedesktop.org/wiki/Software/Beignet/
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	clang-devel
BuildRequires:	cmake
BuildRequires:	libdrm-devel
BuildRequires:	llvm
BuildRequires:	llvm-devel
BuildRequires:	ocl-icd-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
Provides:	ocl-icd(beignet)
Provides:	ocl-icd-driver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Beignet is an open source implementation of the OpenCL specification -
a generic compute oriented API. This code base contains the code to
run OpenCL programs on Intel GPUs which basically defines and
implements the OpenCL host functions required to initialize the
device, create the command queues, the kernels and the programs and
run them on the GPU.

%prep
%setup -qc
mv Release_v%{version}/{*,.*} .
rmdir Release_v%{version}

%build
install -d build
cd build
%cmake \
	-DLIB_INSTALL_DIR=%{_libdir} \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/beignet.bc
%attr(755,root,root) %{_libdir}/%{name}/libcl.so
%{_libdir}/%{name}/ocl_stdlib.h
%{_libdir}/%{name}/ocl_stdlib.h.pch
/etc/OpenCL/vendors/intel-beignet.icd
