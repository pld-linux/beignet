Summary:	Open source implementation of the OpenCL specification for Intel GPUs
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja specyfikacji OpenGL dla GPU formy Intel
Name:		beignet
Version:	0.9
Release:	0.1
License:	LGPL v2+
Group:		Libraries
# http://cgit.freedesktop.org/beignet/snapshot/Release_v%{version}.tar.gz
Source0:	Release_v%{version}.tar.gz
# Source0-md5:	f7926509892f1a9ed39ffa5ae5f00691
URL:		http://www.freedesktop.org/wiki/Software/Beignet/
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	OpenGL-devel
BuildRequires:	clang-devel
BuildRequires:	cmake >= 2.6.0
BuildRequires:	libdrm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	llvm >= 3.3
BuildRequires:	llvm-devel >= 3.3
BuildRequires:	ocl-icd-devel
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	sed >= 4.0
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

%description -l pl.UTF-8
Beignet to mająca otwarte źródła implementacja specyfikacji OpenCL -
ogólnego API przeznaczonego do obliczeń. Ten pakiet zawiera kod do
uruchamiania programów OpenCL na procesorach graficznych (GPU) firmy
Intel; kod ten zasadniczo definiuje i implementuje funkcje hosta
OpenCL wymagane do zainicjowania urządzenia, tworzenia kolejek
poleceń, jądra i programów oraz uruchamia je na GPU.

%prep
%setup -qc
mv Release_v%{version}/{*,.*} .
rmdir Release_v%{version}

# allow to override CMAKE_VERBOSE_MAKEFILE
%{__sed} -i -e '/^SET(CMAKE_VERBOSE_MAKEFILE "false")/d' CMakeLists.txt

%build
install -d build
cd build
%cmake \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DCMAKE_CXX_FLAGS_PLD="%{rpmcxxflags} -DNDEBUG -DGBE_DEBUG=0" \
	-DCMAKE_C_FLAGS_PLD="%{rpmcxxflags} -DNDEBUG -DGBE_DEBUG=0" \
	-DGEN_PCI_ID=0x0162 \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/beignet.bc
%attr(755,root,root) %{_libdir}/%{name}/libcl.so
%attr(755,root,root) %{_libdir}/%{name}/libgbe.so
%attr(755,root,root) %{_libdir}/%{name}/libgbeinterp.so
%{_libdir}/%{name}/ocl_stdlib.h
%{_libdir}/%{name}/ocl_stdlib.h.pch
/etc/OpenCL/vendors/intel-beignet.icd
