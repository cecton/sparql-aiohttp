from textwrap import dedent, indent
import unittest

from aiosparql.syntax import (
    IRI, Literal, Node, PrefixedName, RDF, RDFTerm, Triples, UNDEF)


class Syntax(unittest.TestCase):
    def test_node(self):
        node = Node("john", [
            (RDF.type, "doe"),
            ("foo", "bar"),
            ("foo", "baz"),
        ])
        self.assertEqual(str(node), dedent("""\
            john foo "bar" ;
                foo "baz" ;
                rdf:type "doe" ."""))

    def test_triples(self):
        triples = Triples([("john", RDF.type, "doe")])
        triples.append(("john", "foo", "bar"))
        triples.extend([("jane", "hello", Literal("world", "en"))])
        self.assertEqual(str(triples), dedent("""\
            john rdf:type "doe" ;
                foo "bar" .

            jane hello "world"@en ."""))
        self.assertEqual(triples.indent("  "), indent(str(triples), "  "))

    def test_iri(self):
        self.assertEqual(str(IRI("http://example.org")),
                         "<http://example.org>")
        self.assertEqual(IRI("http://example.org"), IRI("http://example.org"))
        self.assertEqual(IRI("http://example.org"), "http://example.org")
        self.assertEqual(len(set([IRI("http://example.org"),
                                  IRI("http://example.org")])),
                         1)
        self.assertEqual(IRI("http://example.org/") + "boo",
                         IRI("http://example.org/boo"))

    def test_undef(self):
        self.assertEqual(str(UNDEF()), "UNDEF")
        self.assertEqual(UNDEF(), UNDEF())
        self.assertEqual(len(set([UNDEF(), UNDEF()])), 1)

    def test_literal(self):
        self.assertEqual(Literal("foobar"), "foobar")
        self.assertEqual(Literal("foobar"), Literal("foobar"))
        self.assertNotEqual(Literal("foobar", lang="en"),
                            Literal("foobar", lang="es"))
        self.assertEqual(len(set([Literal("foobar"), Literal("foobar")])), 1)
        self.assertEqual(len(set([Literal("foobar", "en"),
                                  Literal("foobar", "es")])),
                         2)

    def test_prefixed_name(self):
        self.assertEqual(PrefixedName(IRI("foo"), "bar", "baz"), IRI("foobaz"))
        self.assertEqual(PrefixedName(IRI("foo"), "bar", "baz"),
                         PrefixedName(IRI("foo"), "bar", "baz"))
        self.assertEqual(len(set([PrefixedName(IRI("foo"), "bar", "baz"),
                                  PrefixedName(IRI("foo"), "bar", "baz")])),
                         1)
        mapping = {
            "foobaz": "ok"
        }
        self.assertEqual(
            mapping.get(PrefixedName(IRI("foo"), "bar", "baz"), "notok"), "ok")

    def test_rdf_term(self):
        self.assertEqual(RDFTerm("foo"), RDFTerm("foo"))
        self.assertEqual(RDFTerm("foo"), "foo")
        self.assertEqual(len(set([RDFTerm("foo"), RDFTerm("foo")])), 1)
