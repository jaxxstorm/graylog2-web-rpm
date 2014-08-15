%define debug_package %{nil}
%define base_install_dir %{_javadir}{%name}
%define __jar_repack %{nil}

Name:           graylog2-web
Version:        0.20.6
Release:        1%{?dist}
Summary:        graylog2-web

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://www.graylog2.org
Source0:        graylog2-web-interface-%{version}.tgz
Source1:        init.d-%{name}
Source2:        sysconfig-%{name}
Source3: 	log4j.xml
Source4:	logrotate-%{name}
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       jpackage-utils
Requires:       java-1.7.0-openjdk
Requires: 	logrotate

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A distributed, highly available, RESTful search engine

%prep
%setup -q -n graylog2-web-interface-%{version}
#we have to use a specific name here until graylog starts using real version number
#%setup -q -n %{name}-%{version}

%build
true

%install
rm -rf $RPM_BUILD_ROOT
# I know we can use -p to create the root directory, but this is more to
# keep track of the required dir
# also, autotools doesn't like copying whole folders
# so we use cp instead
%{__mkdir} -p %{buildroot}/opt/graylog2/web
%{__mkdir} -p %{buildroot}/etc/graylog2
cp -rfv bin %{buildroot}/opt/graylog2/web/
cp -rfv lib %{buildroot}/opt/graylog2/web/
cp -rfv share %{buildroot}/opt/graylog2/web/

# config
cp -rfv conf %{buildroot}/opt/graylog2/web/
cp -rfv conf/graylog2-web-interface.conf %{buildroot}/etc/graylog2/web.conf


# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2/web

# plugins

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir} -p %{buildroot}%{_sysconfdir}/init.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
%{__install} -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

#Docs and other stuff
%{__install} -p -m 644 README.md %{buildroot}/opt/graylog2/web
%{__install} -p -m 644 %{SOURCE3} %{buildroot}/opt/graylog2/web
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
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%defattr(-,graylog2,graylog2,-)
/opt/graylog2/web
%config(noreplace) /etc/graylog2/web.conf
%dir %{_localstatedir}/log/graylog2

%changelog
* Mon Jun 02 2014 lee@leebriggs.co.uk 0.20.2
- Added log config 
- Updating version
* Wed Feb 26 2014 lee@leebriggs.co.uk 0.20.1
- new release
* Fri Feb 14 2014 lee@leebriggs.co.uk 0.20.0-rc3
- Bump for new release
* Mon Feb 10 2014 lee@leebriggs.co.uk 0.20.0-rc2
- Bump for new release
* Tue Jan 21 2014 lee@leebriggs.co.uk 0.20.0-rc1.1
- Updating for rc1-1 release
* Tue Jan 14 2014 lee@leebriggs.co.uk 0.20.0-rc1
- Updating for new graylog2 version
* Fri Dec 12 2013 lee@leebriggs.co.uk 0.20.0.08-1
- Added init script updates for setting conf file path
- Adding java 7 dependency
- Updating for new preview release
* Mon Dec 10 2013 lee@leebriggs.co.uk 0.20.0.07-1
- Initial RPM

