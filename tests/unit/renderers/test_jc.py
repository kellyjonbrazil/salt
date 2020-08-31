# -*- coding: utf-8 -*-

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt libs
import salt.renderers.jc as jc_renderer
from salt.exceptions import SaltRenderError

# Import JC lib
try:
    import jc
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

# Import Salt Testing libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import TestCase, skipIf


@skipIf(not HAS_LIB, "The 'jc' library is missing")
class JCRendererTestCase(TestCase, LoaderModuleMockMixin):
    def setup_loader_modules(self):
        return {jc: {}}

    def test_jc_renderer_kv_parser_nodata(self):
        data = ''
        expected_result = {}
        result = jc_renderer.render(data, parser='kv')

        self.assertEqual(result, expected_result)

    def test_jc_renderer_kv_parser_withdata(self):
        data = '''\
            foo: abc
            bar=efg
            # this is a comment
            baz = hij
        '''
        expected_result = {
            "foo": "abc",
            "bar": "efg",
            "baz": "hij"
        }
        result = jc_renderer.render(data, parser='kv')

        self.assertEqual(result, expected_result)

    def test_jc_renderer_no_parser(self):
        data = '''\
            foo: abc
            bar=efg
            # this is a comment
            baz = hij
        '''
        with self.assertRaises(SaltRenderError):
            jc_renderer.render(data)

    def test_jc_renderer_nonexistent_parser(self):
        data = '''\
            foo: abc
            bar=efg
            # this is a comment
            baz = hij
        '''
        with self.assertRaises(SaltRenderError):
            jc_renderer.render(data, parser='nonexistentparser')

    def test_jc_renderer_wrong_parser(self):
        data = '1'
        with self.assertRaises(SaltRenderError):
            jc_renderer.render(data, parser='airport')
