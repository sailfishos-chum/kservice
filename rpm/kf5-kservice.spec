%global kf5_version 5.107.0

Name: opt-kf5-kservice
Summary: KDE Frameworks 5 Tier 3 solution for advanced plugin and service introspection
Version: 5.107.0
Release: 1%{?dist}

# mixture of LGPLv2 and LGPLv2+ (mostly the latter)
License: LGPLv2
URL:     https://invent.kde.org/frameworks/kservice
Source0: %{name}-%{version}.tar.bz2

%{?opt_kf5_default_filter}

BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
BuildRequires: opt-kf5-kconfig-devel >= %{kf5_version}
BuildRequires: opt-kf5-kcoreaddons-devel >= %{kf5_version}
BuildRequires: opt-kf5-kcrash-devel >= %{kf5_version}
BuildRequires: opt-kf5-kdbusaddons-devel >= %{kf5_version}
#BuildRequires: opt-kf5-kdoctools-devel >= %{kf5_version}
BuildRequires: opt-kf5-ki18n-devel >= %{kf5_version}
BuildRequires: opt-kf5-rpm-macros
BuildRequires: opt-qt5-qtbase-devel

BuildRequires:  flex
BuildRequires:  bison

%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
Requires: opt-kf5-kconfig-core >= %{kf5_version}
Requires: opt-kf5-kcoreaddons >= %{kf5_version}
Requires: opt-kf5-kdbusaddons >= %{kf5_version}
Requires: opt-kf5-ki18n >= %{kf5_version}

%description
KDE Frameworks 5 Tier 3 solution for advanced plugin and service
introspection.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires: opt-kf5-kconfig-devel >= %{kf5_version}
Requires: opt-kf5-kcoreaddons-devel >= %{kf5_version}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../
%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%find_lang %{name} --all-name --with-man

mv %{buildroot}%{_opt_kf5_sysconfdir}/xdg/menus/applications.menu \
   %{buildroot}%{_opt_kf5_sysconfdir}/xdg/menus/kf5-applications.menu

mkdir -p %{buildroot}%{_opt_kf5_datadir}/kservices5
mkdir -p %{buildroot}%{_opt_kf5_datadir}/kservicetypes5


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSES/*.txt
# this is not a config file, despite rpmlint complaining otherwise -- rex
%{_opt_kf5_sysconfdir}/xdg/menus/kf5-applications.menu
%{_opt_kf5_datadir}/qlogging-categories5/kservice.*
%{_opt_kf5_bindir}/kbuildsycoca5
%{_opt_kf5_libdir}/libKF5Service.so.5*
%{_opt_kf5_datadir}/kservicetypes5/
%{_opt_kf5_datadir}/kservices5/
#{_opt_kf5_mandir}/man8/*.8*
%{_opt_kf5_datadir}/locale/

%files devel

%{_opt_kf5_includedir}/KF5/KService/
%{_opt_kf5_libdir}/libKF5Service.so
%{_opt_kf5_libdir}/cmake/KF5Service/
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_KService.pri
