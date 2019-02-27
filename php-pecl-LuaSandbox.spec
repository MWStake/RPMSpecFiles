%global pecl_name LuaSandbox
%global basepkg   %{getenv:PHP}

Summary: LuaSandbox is an extension to allow safely running untrusted Lua 5.1 code from within PHP
Name: %{basepkg}-pecl-%{pecl_name}
Version: %{getenv:VER}
Release: 1%{dist}
License: MIT
Group: Development/Languages
URL: https://www.mediawiki.org/wiki/LuaSandbox
# You can download this from gerrit or github
# github allows linking to tags, though.
Source0: https://github.com/wikimedia/mediawiki-php-luasandbox/archive/%{version}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{basepkg}-devel
BuildRequires: lua-devel
BuildRequires: automake
BuildRequires: gcc
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
Provides:     php-pecl(hexmode/%{pecl_name}) = %{version}
Provides:     php-pecl(hexmode/%{pecl_name})%{?_isa}  = %{version}



%description

LuaSandbox is an extension for PHP to allow safely running untrusted
Lua 5.1 code from within PHP, which will generally be faster than
shelling out to a Lua binary and using inter-process communication.

%prep
%setup -n mediawiki-php-luasandbox-%{version}

phpize
./configure

%build
make test NO_INTERACTION=1

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT
# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{php_inidir}
%{__cat} > %{buildroot}%{php_inidir}/luasandbox.ini << 'EOF'
; Enable luasandbox extension module
extension = luasandbox.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ]  ; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc
/usr/lib64/php/modules/luasandbox.so
%config /etc/php.d/luasandbox.ini

%changelog
* Thu Nov  1 2018 Mark A. Hershberger <mah@everybody.org> - php-pecl-LuaSandbox
- Initial build.

