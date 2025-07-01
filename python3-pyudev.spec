#
# Conditional build:
%bcond_with	doc		# HTML documentation build (not included in sdist)
%bcond_with	tests		# pytest tests (missing files, requires functional udev with device db)
#
%define 	module	pyudev
Summary:	Pure Python binding for libudev
Summary(pl.UTF-8):	Czysto pythonowe wiązanie do libudev
Name:		python3-%{module}
Version:	0.24.3
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pyudev/
Source0:	https://files.pythonhosted.org/packages/source/p/pyudev/%{module}-%{version}.tar.gz
# Source0-md5:	07bbe9111308d2509645705b8321c416
URL:		https://pyudev.readthedocs.io/
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest >= 2.8
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-docutils
BuildRequires:	python3-pytest >= 2.2
BuildRequires:	sphinx-pdg-3 >= 1.0.7
%endif
Requires:	python3-modules >= 1:3.7
Requires:	udev-libs >= 1:151
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyudev is a LGPL licensed, pure Python binding for libudev, the device
and hardware management and information library for Linux. It supports
almost all libudev functionality, you can enumerate devices, query
device properties and attributes or monitor devices, including
asynchronous monitoring with threads, or within the event loops of Qt,
GLib or wxPython.

%description -l pl.UTF-8
pyudev to wydane na licencji LGPL czysto pythonowe wiązanie do libudev
- biblioteki zarządzania urządzeniami i sprzętem dla Linuksa.
Obsługuje prawie całą funkcjonalność libudev, potrafi wyliczać
urządzenia, odpytywać o właściwości i atrybuty urządzeń oraz
monitorować urządzenia, włącznie z asynchronicznym monitorowaniem z
użyciem wątków albo wewnątrz pętli zdarzeń Qt, GLiba czy wxPythona.

%package apidocs
Summary:	API documentation for Python pyudev module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pyudev
Group:		Documentation

%description apidocs
API documentation for Python pyudev module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pyudev.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd):$(pwd)/build-3/lib \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=build-3/lib \
sphinx-build-3 -b html -d doc/_doctrees doc doc/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/pyudev
%{py3_sitescriptdir}/pyudev-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{_static,api,tests,*.html,*.js}
%endif
