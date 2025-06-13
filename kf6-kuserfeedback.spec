#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.15
%define		qtver		5.15.2
%define		kfname		kuserfeedback

Summary:	User Feedback
Name:		kf6-%{kfname}
Version:	6.15.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	c5b33c76570142acb8346c71a01a9528
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	bison
BuildRequires:	cmake >= 3.16
BuildRequires:	flex
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KUser Feedback.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname} --all-name --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6UserFeedbackCore.so.6
%attr(755,root,root) %{_libdir}/libKF6UserFeedbackCore.so.*.*
%ghost %{_libdir}/libKF6UserFeedbackWidgets.so.6
%attr(755,root,root) %{_libdir}/libKF6UserFeedbackWidgets.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/userfeedback
%{_libdir}/qt6/qml/org/kde/userfeedback/KF6UserFeedbackQml.qmltypes
%{_libdir}/qt6/qml/org/kde/userfeedback/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/userfeedback/libKF6UserFeedbackQml.so
%{_libdir}/qt6/qml/org/kde/userfeedback/qmldir
%{_datadir}/qlogging-categories6/org_kde_UserFeedback.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KUserFeedback
%{_includedir}/KF6/KUserFeedbackCore
%{_includedir}/KF6/KUserFeedbackWidgets
%{_libdir}/cmake/KF6UserFeedback
%{_libdir}/libKF6UserFeedbackCore.so
%{_libdir}/libKF6UserFeedbackWidgets.so
%{_libdir}/qt6/mkspecs/modules/qt_KF6UserFeedbackCore.pri
%{_libdir}/qt6/mkspecs/modules/qt_KF6UserFeedbackWidgets.pri
