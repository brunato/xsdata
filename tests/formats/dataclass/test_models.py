from unittest.case import TestCase

from lxml.etree import Element

from xsdata.formats.dataclass.models import Namespaces
from xsdata.models.enums import Namespace


class NamespacesTests(TestCase):
    def test_add(self):
        namespaces = Namespaces()
        namespaces.add("foo")
        namespaces.add("foo")
        namespaces.add("bar", "one")
        namespaces.add("bar", "two")
        namespaces.add(Namespace.XSI.uri, "a")
        namespaces.add(Namespace.XSI.uri, "b")
        namespaces.add(Namespace.XS.uri, "c")
        namespaces.add(Namespace.XS.uri, "d")

        expected = {
            "bar": {"one", "two"},
            "foo": {"ns0"},
            "http://www.w3.org/2001/XMLSchema": {"xs"},
            "http://www.w3.org/2001/XMLSchema-instance": {"xsi"},
        }
        self.assertEqual(expected, namespaces.items)

    def test_add_all(self):
        namespaces = Namespaces()
        namespaces.add_all(
            {
                "b": "bar",
                None: "http://www.w3.org/2001/XMLSchema",
                "foo": "http://www.w3.org/2001/XMLSchema-instance",
            }
        )
        expected = {
            "bar": {"b"},
            "http://www.w3.org/2001/XMLSchema": {"xs"},
            "http://www.w3.org/2001/XMLSchema-instance": {"xsi"},
        }
        self.assertEqual(expected, namespaces.items)

    def test_property_prefixes(self):
        namespaces = Namespaces()
        namespaces.add_all(
            {
                "b": "bar",
                None: "http://www.w3.org/2001/XMLSchema",
                "foo": "http://www.w3.org/2001/XMLSchema-instance",
            }
        )
        self.assertEqual(["b", "xs", "xsi"], namespaces.prefixes)

    def test_property_ns_map(self):
        namespaces = Namespaces()
        namespaces.add_all(
            {
                "b": "bar",
                None: "http://www.w3.org/2001/XMLSchema",
                "foo": "http://www.w3.org/2001/XMLSchema-instance",
            }
        )
        namespaces.add("bar", "again")
        namespaces.add("one")
        namespaces.add("two")

        expected = {
            "b": "bar",
            "again": "bar",
            "ns0": "one",
            "ns1": "two",
            "xs": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
        self.assertEqual(expected, namespaces.ns_map)

    def test_clear(self):
        namespaces = Namespaces()
        namespaces.add_all(
            {"b": "bar", "foo": "http://www.w3.org/2001/XMLSchema-instance"}
        )
        self.assertEqual(2, len(namespaces.ns_map))
        namespaces.clear()
        self.assertEqual(0, len(namespaces.ns_map))

    def test_register(self):
        namespaces = Namespaces()
        namespaces.add("http://komposta.net", "bar")
        namespaces.add("http://foobar", "ns2")  # ns{\d} are not registered

        element = Element("{http://komposta.net}root")
        self.assertEqual({"ns0": "http://komposta.net"}, element.nsmap)

        namespaces.register()
        element = Element("{http://komposta.net}root")
        self.assertEqual({"bar": "http://komposta.net"}, element.nsmap)

        element = Element("{http://foobar}root")
        self.assertEqual({"ns0": "http://foobar"}, element.nsmap)
