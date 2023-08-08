%global commit0 f740ec6f25dbd16e7739ded955b7cbd4eadd1f16
%global _lto_cflags %{nil}
%global rocm_path /opt/rocm
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global up_name HIP

%define patch_level 2

Name:           amd-rocm-hip
Version:        5.6
Release:        %{patch_level}.git%{?shortcommit0}%{?dist}
Summary:        TBD
License:        TBD

URL:            https://github.com/trixirt/%{up_name}
Source0:        %{url}/archive/%{commit0}/%{up_name}-%{shortcommit0}.tar.gz

BuildArch: noarch

%description
TBD

%package devel
Summary:        TBD

%description devel
%{summary}


%prep
%autosetup -p1 -n %{up_name}-%{commit0}

%install
mkdir -p %{buildroot}%{rocm_path}/hip/include/hip
install -m 644 include/hip/* %{buildroot}%{rocm_path}/hip/include/hip
install -m 644 VERSION %{buildroot}%{rocm_path}/hip
install -m 644 hip-lang-config.cmake.in %{buildroot}%{rocm_path}/hip
mkdir -p %{buildroot}%{rocm_path}/hip/cmake/FindHIP
install -m 644 cmake/*.cmake %{buildroot}%{rocm_path}/hip/cmake
install -m 644 cmake/FindHIP/*.cmake %{buildroot}%{rocm_path}/hip/cmake/FindHIP
cp -r tests %{buildroot}%{rocm_path}/hip/

%files devel
%{rocm_path}

%changelog
* Mon Aug 07 2023 Tom Rix <trix@redhat.com>
- Stub something together
