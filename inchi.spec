# Conditional build:
%bcond_without	tests		# build without tests

%define inchi_so_ver 1.04.00
%define url_ver 1.04
Summary:	The IUPAC International Chemical Identifier library
Name:		inchi
Version:	1.0.4
Release:	1
Source0:	http://www.inchi-trust.org/fileadmin/user_upload/software/inchi-v%{url_ver}/INCHI-1-API.ZIP
# Source0-md5:	8447bf108af12fe66eecba41bbc89918
Source1:	http://www.inchi-trust.org/fileadmin/user_upload/software/inchi-v%{url_ver}/INCHI-1-DOC.ZIP
# Source1-md5:	4b438cc7da7472577307a2063414c973
Source2:	http://www.inchi-trust.org/fileadmin/user_upload/software/inchi-v%{url_ver}/INCHI-1-TEST.ZIP
# Source2-md5:	8176b5e0e24c6aad78c522265378362e
Group:		Libraries
Patch0:		%{name}-rpm.patch
License:	LGPL v2+
URL:		http://www.inchi-trust.org/?q=node/14
BuildRequires:	dos2unix
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The IUPAC International Chemical Identifier (InChITM) is a
non-proprietary identifier for chemical substances that can be used in
printed and electronic data sources thus enabling easier linking of
diverse data compilations. It was developed under IUPAC Project
2000-025-1-800 during the period 2000-2004. Details of the project and
the history of its progress are available from the project web site.

This package contains the command line conversion utility.

%package libs
Summary:	The IUPAC International Chemical Identifier library
Group:		Libraries

%description libs
The IUPAC International Chemical Identifier (InChITM) is a
non-proprietary identifier for chemical substances that can be used in
printed and electronic data sources thus enabling easier linking of
diverse data compilations. It was developed under IUPAC Project
2000-025-1-800 during the period 2000-2004. Details of the project and
the history of its progress are available from the project web site.

%package devel
Summary:	Development headers for the InChI library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The inchi-devel package includes the header files and libraries
necessary for developing programs using the InChI library.

If you are going to develop programs which will use this library you
should install inchi-devel. You'll also need to have the inchi package
installed.

%package doc
Summary:	Documentation for the InChI library
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
The inchi-doc package contains user documentation for the InChI
software and InChI library API reference for developers.

%prep
%setup -q -n INCHI-1-API -a 1 -a 2
%patch0 -p1 -b .r

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
%ghost %{_libdir}/libinchi.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/inchi
%{_libdir}/libinchi.so

%files doc
%defattr(644,root,root,755)
%doc INCHI-1-DOC/*
