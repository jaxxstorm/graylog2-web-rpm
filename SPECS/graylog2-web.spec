%define debug_package %{nil}
%define base_install_dir %{_javadir}{%name}

Name:           graylog2-web
Version:        0.20.0.07
Release:        1%{?dist}
Summary:        graylog2-web

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://www.graylog2.org
Source0:        graylog2-web-interface-0.20.0-preview.7.tgz
Source1:        init.d-%{name}
Source2:        sysconfig-%{name}
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       jpackage-utils
Requires:       jre >= 1.6.0

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A distributed, highly available, RESTful search engine

%prep
%setup -q -n graylog2-web-interface-0.20.0-preview.7
#we have to use a specific name here until graylog starts using real version number
#%setup -q -n %{name}-%{version}

%build
true

%install
rm -rf $RPM_BUILD_ROOT
# I know we can use -p to create the root directory, but this is more to
# keep track of the required dir
%{__mkdir} -p %{buildroot}/opt/graylog2/web
cp -rfv bin %{buildroot}/opt/graylog2/web/
cp -rfv lib %{buildroot}/opt/graylog2/web/
cp -rfv share %{buildroot}/opt/graylog2/web/

# config
cp -rfv conf %{buildroot}/opt/graylog2/web/


# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2/web

# plugins

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir} -p %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
%{__install} -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

#Docs and other stuff
%{__install} -p -m 644 README.md %{buildroot}/opt/graylog2/web

%pre
# create graylog2 group
if ! getent group graylog2 >/dev/null; then
        groupadd -r graylog2
fi

# create graylog2 user
if ! getent passwd graylog2 >/dev/null; then
        useradd -r -g graylog2 -d %{_javadir}/%{name} \
            -s /sbin/nologin -c "Party Gorilla" graylog2
fi

%post
/sbin/chkconfig --add graylog2-web

%preun
if [ $1 -eq 0 ]; then
  /sbin/service/graylog2-web stop >/dev/null 2>&1
  /sbin/chkconfig --del graylog2-web
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/init.d/graylog2-web
%config(noreplace) %{_sysconfdir}/sysconfig/graylog2-web
%defattr(-,graylog2,graylog2,-)
/opt/graylog2/web
%dir %{_localstatedir}/log/graylog2

%changelog
* Mon Dec 10 2013 lee@leebriggs.co.uk 0.20.0.07-1
- Initial RPM

