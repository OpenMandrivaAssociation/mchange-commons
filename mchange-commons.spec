%_javapackages_macros
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
