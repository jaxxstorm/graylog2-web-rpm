graylog2-web
===============

Graylog2 Web RPM packages


Releases
=============

A compiled RPM is available from the [releases page](https://github.com/jaxxstorm/graylog2-web-rpm/releases)

Installing
=============

This RPM requires some config after install. You'll need to edit the location of your [graylog2-server](https://github.com/jaxxstorm/graylog2-server-rpm) instance in the config file at /etc/graylog2/web.conf

Further instructions can be found [here](http://support.torch.sh/help/kb/graylog2-web-interface/installing-graylog2-web-interface-v0200-previewx-on-nix-systems)


Build your own
=============

building your own is simple
```
git clone https://github.com/jaxxstorm/graylog2-web-rpm.git ~/rpmbuild
cd rpmbuild && rpmbuild -ba SPECS/graylog2-web.spec
```

Patches
=============

These rpms have been tested extensively on my personal CentOS instance, however I realise they aren't perfect.
Please submit a pull request to improve them!


Acknowledgements
=============

Thanks to [Tavisto](https://github.com/tavisto/elasticsearch-rpms) for his excellent work on the elasticsearch rpm, was a great starting point for init scripts
and spec files

Thanks to the [graylog2](https://github.com/graylog2) team for making such an awesome open source product!

