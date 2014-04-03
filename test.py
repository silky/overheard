import unittest
from overheard import *

class ArchivTest(unittest.TestCase):

    def test_old_arxiv_id(self):
        # good ids
        self.assertTrue(old_arxiv_id('1234567'))
        self.assertTrue(old_arxiv_id('1234567v1'))
        self.assertTrue(old_arxiv_id('1234567v12'))

        # too short
        self.assertFalse(old_arxiv_id('123456'))
        self.assertFalse(old_arxiv_id('1234567v'))

        # too long
        self.assertFalse(old_arxiv_id('12345678'))

        # wrong letter
        self.assertFalse(old_arxiv_id('1234567a1'))

        # junk at start
        self.assertFalse(old_arxiv_id('a1234567'))
        self.assertFalse(old_arxiv_id('a1234567v1'))
        self.assertFalse(old_arxiv_id('a1234567v12'))

        # junk at end
        self.assertFalse(old_arxiv_id('1234567a'))
        self.assertFalse(old_arxiv_id('1234567v1a'))
        self.assertFalse(old_arxiv_id('1234567v12a'))

        # two versions
        self.assertFalse(old_arxiv_id('1234567v1v2'))

    def test_new_arxiv_id(self):
        # good ids
        self.assertTrue(new_arxiv_id('1234.5678'))
        self.assertTrue(new_arxiv_id('1234.5678v1'))
        self.assertTrue(new_arxiv_id('1234.5678v12'))

        # wrong delimiter
        self.assertTrue(new_arxiv_id('1234a5678'))

        # too short
        self.assertFalse(new_arxiv_id('123.5678'))
        self.assertFalse(new_arxiv_id('1234.567'))
        self.assertFalse(new_arxiv_id('1234.5678v'))

        # too long
        self.assertFalse(new_arxiv_id('1234.56788'))

        # wrong letter
        self.assertFalse(new_arxiv_id('1234.5678a1'))

        # junk at start
        self.assertFalse(new_arxiv_id('a1234.5678'))
        self.assertFalse(new_arxiv_id('a1234.5678v1'))
        self.assertFalse(new_arxiv_id('a1234.5678v12'))

        # junk at end
        self.assertFalse(new_arxiv_id('1234.5678a'))
        self.assertFalse(new_arxiv_id('1234.5678v1a'))
        self.assertFalse(new_arxiv_id('1234.5678v12a'))

        # two versions
        self.assertFalse(new_arxiv_id('1234.5678v1v2'))

    def test_long_comment_regexp(self):
        self.assertTrue(re.search(long_comment_regexp, '% and comment'))
        self.assertTrue(re.search(long_comment_regexp, ' % and comment'))

        # make sure I get the whole comment
        self.assertEqual(re.search(long_comment_regexp, '%% and comment').group(1),
                         '%% and comment')
        self.assertEqual(re.search(long_comment_regexp, ' %% and comment').group(1),
                         '%% and comment')
        self.assertEqual(re.search(long_comment_regexp, '% and % comment').group(1),
                         '% and % comment')
        self.assertEqual(re.search(long_comment_regexp, ' % and % comment').group(1),
                         '% and % comment')

        # these are short comments
        self.assertFalse(re.search(long_comment_regexp, 'some text % and comment'))
        self.assertFalse(re.search(long_comment_regexp, 'some text %% and comment'))
        self.assertFalse(re.search(long_comment_regexp, 'some text % and % comment'))

    def test_short_comment_regexp(self):
        self.assertTrue(re.search(short_comment_regexp, 'some text % and comment'))

        # make sure I get the whole comment
        self.assertEqual(re.search(short_comment_regexp, 'some text % and % comment').group(1),
                         '% and % comment')
        self.assertEqual(re.search(short_comment_regexp, 'some text %% and comment').group(1),
                         '%% and comment')
                                
        # these are long comments
        #self.assertFalse(re.search(short_comment_regexp, '% and comment'))
        #self.assertFalse(re.search(short_comment_regexp, ' % and comment'))
        #self.assertFalse(re.search(short_comment_regexp, '%% and comment'))
        #self.assertFalse(re.search(short_comment_regexp, ' %% and commment'))
        #self.assertFalse(re.search(short_comment_regexp, '% and % comment'))
        #self.assertFalse(re.search(short_comment_regexp, ' % and % comment'))

def test():
    #suite = unittest.defaultTestLoader.loadTestsFromName('gsn_util.test')
    suite = unittest.defaultTestLoader.loadTestsFromName('test')
    unittest.TextTestRunner().run(suite)

if type(__builtins__) is type({}):
    names = __builtins__.keys()
else:
    names = dir(__builtins__)

if __name__ == '__main__' and '__IPYTHON__' not in names:
    test()