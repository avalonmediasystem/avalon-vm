Name:           avalon-vm
Version:        1.0
Release:        1
Summary:        Avalon-VM setup and support

Group:          System Environment/Base
License:        GPL
URL:            http://avalonmediasystem.org
Source0:        http://example.com/avalon-vm-1.0.tar.gz

BuildArch:	noarch
#BuildRequires:  
Requires:       firstboot NetworkManager-gnome gcc perl-YAML-LibYAML perl-XML-Twig
Provides:	perl(AvalonConfig)

%description
The firstboot experience, including the EULA and FFMPEG building scripts

%prep
%setup -q


%build
echo "Nothing to do!"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/avalon
%{__install} --mode=644 EULA.avalon logo.png AvalonConfig.pm $RPM_BUILD_ROOT/%{_datadir}/avalon
%{__install} --mode=755 buildFFMPEG avalon_config_email avalon_randomize_passwords dist-prep make_tarball $RPM_BUILD_ROOT/%{_datadir}/avalon
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/firstboot/modules
%{__install} --mode=644 avalon_*.py $RPM_BUILD_ROOT/%{_datadir}/firstboot/modules
mkdir -p $RPM_BUILD_ROOT/etc/init.d
%{__install} --mode=755 avalon_host_config $RPM_BUILD_ROOT/etc/init.d


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_datadir}/avalon
%{_datadir}/avalon/*
%{_datadir}/firstboot/modules/*
/etc/init.d/avalon_host_config

%post
/sbin/chkconfig avalon_host_config on

%changelog
