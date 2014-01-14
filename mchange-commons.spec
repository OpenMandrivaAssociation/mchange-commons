%{?_javapackages_macros:%_javapackages_macros}
Name:    mchange-commons
Version: 0.2.3.4
Release: 3.0%{?dist}
Summary: A collection of general purpose utilities for c3p0
License: LGPLv2 or EPL
URL:     https://github.com/swaldman/mchange-commons-java


BuildRequires: java-devel >= 1:1.6.0
BuildRequires: java-javadoc >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: junit
BuildRequires: ant-junit
BuildRequires: log4j

Requires: jpackage-utils
Requires: java

Source0: https://github.com/swaldman/%{name}-java/archive/%{name}-java-%{version}-final.tar.gz

# Patch to build with JDBC 4.1/Java 7
Patch1: mchange-commons-jdbc-4.1.patch

# Remove one of the tests that intermittently fails
Patch2: mchange-commons-remove-weakness-test.patch

BuildArch: noarch

%description
Originally part of c3p0, %{name} is a set of general purpose
utilities.

%package javadoc
Summary:       API documentation for %{name}

Requires:      jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-java-%{name}-java-%{version}-final

%patch1 -p0 -b .jdbc41
%patch2 -p0 -b .testweakness

# remove all binary bits
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
ant \
  -Dbuild.sysclasspath=first \
  -Djunit.jar.file=`build-classpath junit` \
  -Dlog4j.jar.file=`build-classpath log4j`

sed -i -e "s|@mchange-commons-java.version.maven@|%{version}|g" \
  src/maven/pom.xml

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 build/%{name}-java-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-java.jar

# javadocs
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 src/maven/pom.xml \
  %{buildroot}%{_mavenpomdir}/JPP-%{name}-java.pom

%add_maven_depmap JPP-%{name}-java.pom %{name}-java.jar

%files
%doc LICENSE*
%{_javadir}/*
%{_mavenpomdir}/JPP-*
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE*
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Mat Booth <fedora@matbooth.co.uk> - 0.2.3.4-2
- Include pom file
- Update project URL

* Thu Mar 28 2013 Mat Booth <fedora@matbooth.co.uk> - 0.2.3.4-1
- Update to latest upstream release
- License change to "LGPLv2 or EPL"

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.8.20110130hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.2-0.7.20110130hg
- Fix file permissions
- Update to current packaging guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.6.20110130hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Deepak Bhole <dbhole@redhat.com> - 0.2-0.5.20110130hg
- Added patch to build with JDBC 4.1/Java 7
- Added patch to disable one of the tests that is not always guaranteed to pass

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.4.20110130hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 31 2011 Mat Booth <fedora@matbooth.co.uk> 0.2-0.3.20110130hg
- Add build dep on ant-junit.
- Build and install javadoc.

* Sun Jan 30 2011 Mat Booth <fedora@matbooth.co.uk> 0.2-0.2.20110130hg
- Update for guideline compliance.

* Fri Oct 8 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.2-0.1.20101008hg
- initial package
