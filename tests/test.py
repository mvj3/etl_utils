# -*- coding: utf-8 -*-

import os, sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

import unittest

from etl_utils import *

class TestPhrasalRecognizer(unittest.TestCase):
    def test_chinese(self):
        self.assertTrue(is_chinese(u"你"))
        self.assertFalse(is_chinese(u"h"))

        self.assertTrue(is_number(u"3"))
        self.assertFalse(is_number(u"a"))

        self.assertTrue(is_alphabet(u"h"))
        self.assertFalse(is_alphabet(u"3"))

        self.assertTrue(is_other(u"。"))
        self.assertFalse(is_other(u"a"))

        #test Q2B and B2Q
        for i in range(0x0020,0x007F):
                print Q2B(B2Q(unichr(i))),B2Q(unichr(i))

        #test uniform
        ustring=u'中国 人名ａ高频Ａ'
        ustring=uniform(ustring)
        ret=string2List(ustring)
        print ret

        self.assertEqual(u"@",    stringQ2B(u"＠"))
        self.assertEqual(u"Z",    Q2B(u"Ｚ"))
        self.assertEqual(u"...",  stringQ2B(unicode("…", "UTF-8")))
        self.assertEqual(u"'",    stringQ2B(u"′"))

    def test_dict_utils(self):
        d1 = {"a" : {"b" : "c"} }
        self.assertEqual(dict_nested_read(d1, ["a", "b"]), "c")

    def test_ItemsGroupAndIndexes(self):
        igi = ItemsGroupAndIndexes()
        igi.add([1,2,3])
        igi.add([4,5,6])
        igi.add([7,8,9])
        igi.add([10,11])
        self.assertEqual(igi.result_json(), [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11]])
        self.assertEqual(igi.find(7), [7,8,9])
        self.assertTrue(igi.exists(3))
        self.assertFalse(igi.exists(13))
        self.assertTrue(igi.exists_between(10, 11))
        self.assertEqual(igi.groups_len(), 4)
        self.assertEqual(igi.items_len(), 11)

    def test_re_special_chars(self):
        __answers_str = "WhoWhoseWho\xe2\x80\x99s"
        self.assertEqual(re_special_chars.sub("", __answers_str), "WhoWhoseWhos")




if __name__ == '__main__': unittest.main()