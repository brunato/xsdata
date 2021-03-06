from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from unittest import mock

from tests.factories import ClassFactory
from tests.factories import FactoryTestCase
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.formats.generators import AbstractGenerator
from xsdata.models.codegen import Class
from xsdata.utils import text
from xsdata.writer import writer


@dataclass
class FakeGenerator(AbstractGenerator):
    dir: Optional[TemporaryDirectory] = None

    def render(self, classes: List[Class]) -> Iterator[Tuple[Path, str, str]]:
        for obj in classes:
            yield Path(f"{self.dir}/{obj.name}.txt"), obj.package, obj.name

    @classmethod
    def module_name(cls, name):
        return text.snake_case(name)

    @classmethod
    def package_name(cls, name):
        return text.snake_case(name)


class CodeWriterTests(FactoryTestCase):
    FAKE_NAME = "fake"

    def tearDown(self):
        writer.generators.pop(self.FAKE_NAME, False)

    def test_formats(self):
        expected = ["pydata", "plantuml"]
        self.assertEqual(expected, writer.formats)
        self.assertIsInstance(writer.get_format("pydata"), DataclassGenerator)

    def test_register_generator(self):
        writer.register_format(self.FAKE_NAME, FakeGenerator())
        self.assertIn("fake", writer.formats)
        self.assertIsInstance(writer.get_format("fake"), FakeGenerator)

    def test_write(self):
        classes = ClassFactory.list(2)
        with TemporaryDirectory() as tmpdir:
            writer.register_format(self.FAKE_NAME, FakeGenerator(tmpdir))
            writer.write(classes, "fake")

            for obj in classes:
                self.assertEqual(obj.name, Path(f"{tmpdir}/{obj.name}.txt").read_text())

    @mock.patch("builtins.print")
    def test_print(self, mock_print):
        classes = ClassFactory.list(2)
        writer.register_format(self.FAKE_NAME, FakeGenerator())
        writer.print(classes, "fake")

        mock_print.assert_has_calls([mock.call(obj.name, end="") for obj in classes])

    def test_designate(self):
        classes = ClassFactory.list(3)
        classes[2].package = "foo!"
        classes[2].module = "tests!"

        writer.register_format(self.FAKE_NAME, FakeGenerator())
        writer.designate(classes, "fake")

        self.assertEqual("foo", classes[0].package)
        self.assertEqual("foo", classes[1].package)
        self.assertEqual("foo", classes[2].package)

        self.assertEqual("tests", classes[0].module)
        self.assertEqual("tests", classes[1].module)
        self.assertEqual("tests_1", classes[2].module)
