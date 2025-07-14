Summary:	Open source implementation of the OpenCL specification for Intel GPUs
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja specyfikacji OpenCL dla GPU formy Intel
Name:		beignet
Version:	1.3.2
Release:	0.1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://www.freedesktop.org/wiki/Software/Beignet/NEWS/
Source0:	https://01.org/sites/default/files/beignet-%{version}-source.tar.gz
# Source0-md5:	a577ab18d67a891c8767b8ea62253543
Patch0:		cflags.patch
Patch1:		static_llvm.patch
Patch2:		%{name}-llvm11-support.patch
# Debian patches
Patch10:	%{name}-reduce-notfound-output.patch
Patch11:	%{name}-update-docs.patch
Patch12:	%{name}-docs-broken-links.patch
Patch13:	%{name}-cl_accelerator_intel.patch
Patch14:	%{name}-grammar.patch
Patch15:	%{name}-clearer-type-errors.patch
Patch16:	%{name}-debian-885423.patch
Patch17:	%{name}-disable-wayland-warning.patch
Patch18:	%{name}-eventchain-memory-leak.patch
Patch19:	%{name}-llvm6-support.patch
Patch20:	%{name}-llvm7-support.patch
Patch21:	%{name}-accept-old-create-queue.patch
Patch22:	%{name}-reduce-notfound-output2.patch
Patch23:	%{name}-coffeelake.patch
Patch24:	%{name}-in-order-queue.patch
Patch25:	%{name}-accept-ignore--g.patch
Patch26:	%{name}-llvm8-support.patch
Patch27:	%{name}-llvm9-support.patch
Patch28:	%{name}-cometlake.patch
# modified
Patch29:	%{name}-llvm10-support.patch
URL:		https://www.freedesktop.org/wiki/Software/Beignet/
BuildRequires:	EGL-devel
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	OpenGL-devel
BuildRequires:	clang-devel >= 3.9
BuildRequires:	cmake >= 2.6.0
BuildRequires:	libdrm-devel >= 2.4.66
BuildRequires:	libedit-devel
BuildRequires:	libstdc++-devel
BuildRequires:	llvm >= 3.9
BuildRequires:	llvm-devel >= 3.9
BuildRequires:	ncurses-devel
BuildRequires:	ocl-icd-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(egl) >= 13.0.0
BuildRequires:	pkgconfig(gl) >= 13.0.0
BuildRequires:	python
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	zlib-devel
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
%setup -qn Beignet-%{version}-Source
%patch -P0 -p1
%patch -P1 -p1
%patch -P10 -p1
%patch -P11 -p1
%patch -P12 -p1
%patch -P13 -p1
%patch -P14 -p1
%patch -P15 -p1
%patch -P16 -p1
%patch -P17 -p1
%patch -P18 -p1
%patch -P19 -p1
%patch -P20 -p1
%patch -P21 -p1
%patch -P22 -p1
%patch -P23 -p1
%patch -P24 -p1
%patch -P25 -p1
%patch -P26 -p1
%patch -P27 -p1
%patch -P28 -p1
%patch -P29 -p1
%patch -P2 -p1

# don't lower default -std= on g++ 5+ (recent llvm requires C++14)
%if "%{_ver_ge '%{cxx_version}' '5.0'}" == "1"
%{__sed} -i -e 's/ -std=c++0x / /' CMakeLists.txt
%endif

%build
install -d build
cd build
%cmake \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DCMAKE_CXX_FLAGS_PLD="%{rpmcxxflags} -DNDEBUG -DGBE_DEBUG=0" \
	-DCMAKE_C_FLAGS_PLD="%{rpmcxxflags} -DNDEBUG -DGBE_DEBUG=0" \
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
%{_libdir}/%{name}/beignet.pch
%ifarch %{x8664}
%{_libdir}/%{name}/beignet_20.bc
%{_libdir}/%{name}/beignet_20.pch
%endif
%{_libdir}/%{name}/include
/etc/OpenCL/vendors/intel-beignet.icd
