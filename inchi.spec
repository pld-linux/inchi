#
# Conditional build:
%bcond_without	tests		# build without tests

%define inchi_so_ver 1.04.00
%define url_ver 1.04
Summary:	The IUPAC International Chemical Identifier library
Summary(pl.UTF-8):	Biblioteka międzynarodowych identyfikatorów chemicznych IUPAC
Name:		inchi
Version:	1.0.4
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://www.inchi-trust.org/fileadmin/user_upload/software/inchi-v%{url_ver}/INCHI-1-API.ZIP
# Source0-md5:	8447bf108af12fe66eecba41bbc89918
Source1:	http://www.inchi-trust.org/fileadmin/user_upload/software/inchi-v%{url_ver}/INCHI-1-DOC.ZIP
# Source1-md5:	4b438cc7da7472577307a2063414c973
Source2:	http://www.inchi-trust.org/fileadmin/user_upload/software/inchi-v%{url_ver}/INCHI-1-TEST.ZIP
# Source2-md5:	8176b5e0e24c6aad78c522265378362e
Patch0:		%{name}-rpm.patch
URL:		http://www.inchi-trust.org/?q=node/14
BuildRequires:	dos2unix
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The IUPAC International Chemical Identifier (InChI(TM)) is a
non-proprietary identifier for chemical substances that can be used in
printed and electronic data sources thus enabling easier linking of
diverse data compilations. It was developed under IUPAC Project
2000-025-1-800 during the period 2000-2004. Details of the project and
the history of its progress are available from the project web site.

This package contains the command line conversion utility.

%description -l pl.UTF-8
IUPAC International Chemical Identifier (InChi(TM)) to niewłasnościowy
międzynarodowy identyfikator dla substancji chemicznych, który można
używać w drukowanych i elektronicznych źródłach danych, co umożliwia
łatwiejsze powiązania w rozmaitych kompilacjach danych. Identyfikator
powstał w ramach projektu IUPAC 2000-025-1-800 w okresie 2000-2004.
Szczegóły projektu i historię postępów można znaleźć na stronie WWW.

Ten pakiet zawiera narzędzie linii poleceń do konwersji.

%package libs
Summary:	The IUPAC International Chemical Identifier library
Summary(pl.UTF-8):	Biblioteka międzynarodowych identyfikatorów chemicznych IUPAC
Group:		Libraries

%description libs
The IUPAC International Chemical Identifier (InChI(TM)) is a
non-proprietary identifier for chemical substances that can be used in
printed and electronic data sources thus enabling easier linking of
diverse data compilations. It was developed under IUPAC Project
2000-025-1-800 during the period 2000-2004. Details of the project and
the history of its progress are available from the project web site.

%description libs -l pl.UTF-8
IUPAC International Chemical Identifier (InChi(TM)) to niewłasnościowy
międzynarodowy identyfikator dla substancji chemicznych, który można
używać w drukowanych i elektronicznych źródłach danych, co umożliwia
łatwiejsze powiązania w rozmaitych kompilacjach danych. Identyfikator
powstał w ramach projektu IUPAC 2000-025-1-800 w okresie 2000-2004.
Szczegóły projektu i historię postępów można znaleźć na stronie WWW.

%package devel
Summary:	Development headers for the InChI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki InChI
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package includes the header files necessary for developing
programs using the InChI library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących bibliotekę InChI.

%package doc
Summary:	Documentation for the InChI library
Summary(pl.UTF-8):	Dokumentacja do biblioteki InChI
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
This package contains user documentation for the InChI software and
InChI library API reference for developers.

%description doc -l pl.UTF-8
Ten pakiet zawiera dokumentację użytkownika do oprogramowania InChI
oraz dokumentację API biblioteki InChI dla programistów.

%prep
%setup -q -n INCHI-1-API -a 1 -a 2
%patch0 -p1

%{__sed} -i -e 's,gcc,$(CC),' INCHI_API/gcc_so_makefile/makefile

rm INCHI_API/gcc_so_makefile/result/{libinchi,inchi}*
for file in INCHI_API/inchi_dll/inchi_api.h LICENCE readme.txt ; do
	dos2unix -k $file
done

cd INCHI-1-TEST/test
unzip -d reference -qq -a InChI_TestSet-result.zip
sed -i -e 's,./inchi-1,../../INCHI_API/gcc_so_makefile/result/inchi_main,g' TestSet2InChI.sh

%build
%{__make} -C INCHI_API/gcc_so_makefile \
	ISLINUX=1 \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%if %{with tests}
export LD_LIBRARY_PATH=$(pwd)/INCHI_API/gcc_so_makefile/result/
cd INCHI-1-TEST/test
sh ./TestSet2InChI.sh
for t in InChI_TestSet*.txt; do
	cmp $t reference/$t
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/inchi}
install -pm 755 INCHI_API/gcc_so_makefile/result/inchi_main $RPM_BUILD_ROOT%{_bindir}/inchi-1
install -p INCHI_API/gcc_so_makefile/result/libinchi.so.%{inchi_so_ver} $RPM_BUILD_ROOT%{_libdir}
ln -s libinchi.so.%{inchi_so_ver} $RPM_BUILD_ROOT%{_libdir}/libinchi.so.1
ln -s libinchi.so.1 $RPM_BUILD_ROOT%{_libdir}/libinchi.so
install -pm644 INCHI_API/inchi_dll/inchi_api.h $RPM_BUILD_ROOT%{_includedir}/inchi

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/inchi-1

%files libs
%defattr(644,root,root,755)
%doc LICENCE readme.txt
%attr(755,root,root) %{_libdir}/libinchi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinchi.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinchi.so
%{_includedir}/inchi

%files doc
%defattr(644,root,root,755)
%doc INCHI-1-DOC/*
