import unittest
from lib.analysis import user
import lib.config as config
from lib.in_out import reader
import lib.nickTracker as nickTracker
from mock import patch
import networkx as nx
import lib.util as util
import os
import StringIO
import sys
import filecmp


class UserTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.test_data_dir = self.current_directory + "/../../../data/test_lib/test_analysis/user_test/"
        self.log_data = util.load_from_disk(self.test_data_dir + "log_data")
        self.nicks = util.load_from_disk(self.test_data_dir + "nicks")
        self.nick_same_list = util.load_from_disk(self.test_data_dir + "nick_same_list")


    def tearDown(self):
        self.current_directory = None
        self.test_data_dir = None
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None


    @patch("lib.util.splice_find", autospec = True)
    @patch("lib.util.build_graphs", autospec = True)
    @patch("lib.util.get_year_month_day", autospec = True)
    def test_nick_change_graph(self, mock_get_year_month_day, mock_build_graphs, mock_splice_find):
        mock_splice_find_data = util.load_from_disk(self.current_directory + "/data/user_test/nick_change_graph/splice_find_list")
        mock_build_graphs_data = util.load_from_disk(self.current_directory + "/data/user_test/build_graphs_list")
        mock_get_year_month_day_data = util.load_from_disk(self.current_directory + "/data/user_test/get_year_month_day_list")
        mock_splice_find.side_effect = mock_splice_find_data
        mock_build_graphs.side_effect = mock_build_graphs_data
        mock_get_year_month_day.side_effect = mock_get_year_month_day_data
        expected_nick_change_graph_list = util.load_from_disk(self.test_data_dir + "nick_change_graph_list")
        expected_aggregate_nick_change_graph = util.load_from_disk(self.test_data_dir + "aggregate_nick_change_graph")

        nick_change_graph_list = user.nick_change_graph(self.log_data, True)

        mock_splice_find.side_effect = mock_splice_find_data
        mock_build_graphs.side_effect = mock_build_graphs_data
        mock_get_year_month_day.side_effect = mock_get_year_month_day_data
    
        aggregate_nick_change_graph = user.nick_change_graph(self.log_data, False)

        for i in xrange(len(nick_change_graph_list)):
            self.assertTrue(nx.is_isomorphic(expected_nick_change_graph_list[i], nick_change_graph_list[i]))

        self.assertTrue(nx.is_isomorphic(expected_aggregate_nick_change_graph, aggregate_nick_change_graph))


    @patch("lib.config.DEBUGGER", new = True)
    @patch("lib.config.PRINT_WORDS", new = True)
    def test_top_keywords_for_nick(self):
        user_keyword_freq_dict_data = util.load_from_disk(self.test_data_dir + "user_keyword_freq_dict")
        user_keyword_freq_dict = user_keyword_freq_dict_data

        expected_top_keywords = util.load_from_disk(self.current_directory + "/data/user_test/top_keywords1")
        expected_top_keywords_normal_freq = util.load_from_disk(self.current_directory + "/data/user_test/top_keywords_normal_freq1")
        expected_captured_output = util.load_from_disk(self.current_directory + "/data/user_test/stdout_captured_output_top_keywords_for_nick1")

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        top_keywords, top_keywords_normal_freq = user.top_keywords_for_nick(user_keyword_freq_dict, user_keyword_freq_dict[12]['nick'], 0.01, 100)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(output, expected_captured_output)
        self.assertEqual(top_keywords, expected_top_keywords)
        self.assertEqual(top_keywords_normal_freq, expected_top_keywords_normal_freq)


        user_keyword_freq_dict = user_keyword_freq_dict_data
        expected_top_keywords = util.load_from_disk(self.current_directory + "/data/user_test/top_keywords2")
        expected_top_keywords_normal_freq = util.load_from_disk(self.current_directory + "/data/user_test/top_keywords_normal_freq2")

        top_keywords, top_keywords_normal_freq = user.top_keywords_for_nick(user_keyword_freq_dict, user_keyword_freq_dict[12]['nick'], 0.01, 60)

        self.assertEqual(top_keywords, expected_top_keywords)
        self.assertEqual(top_keywords_normal_freq, expected_top_keywords_normal_freq)


        user_keyword_freq_dict = user_keyword_freq_dict_data
        expected_top_keywords = util.load_from_disk(self.current_directory + "/data/user_test/top_keywords3")
        expected_top_keywords_normal_freq = util.load_from_disk(self.current_directory + "/data/user_test/top_keywords_normal_freq3")
        expected_captured_output = util.load_from_disk(self.current_directory + "/data/user_test/stdout_captured_output_top_keywords_for_nick3")

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        top_keywords, top_keywords_normal_freq = user.top_keywords_for_nick(user_keyword_freq_dict, user_keyword_freq_dict[0]['nick'], 0.8, 20)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(output, expected_captured_output)
        self.assertEqual(top_keywords, expected_top_keywords)
        self.assertEqual(top_keywords_normal_freq, expected_top_keywords_normal_freq)

    @patch("lib.config.DEBUGGER", new = True)
    @patch("lib.config.PRINT_WORDS", new = True)
    @patch("lib.config.KEYWORDS_THRESHOLD", new = 0.01)
    @patch("lib.config.KEYWORDS_MIN_WORDS", new = 100)
    @patch("lib.util.get_nick_representative", autospec = True)
    @patch("lib.util.check_if_msg_line", autospec = True)
    @patch("lib.util.correctLastCharCR", autospec = True)
    @patch("lib.util.correct_last_char_list", autospec = True)
    @patch("lib.util.splice_find", autospec = True)
    @patch("lib.util.correct_nick_for_", autospec = True)
    @patch("lib.util.rec_list_splice", autospec = True)
    @patch("lib.analysis.user.extended_stop_words", autospec = True)
    @patch("lib.analysis.user.top_keywords_for_nick", autospec = True)
    def test_keywords(self, mock_top_keywords_for_nick, mock_extended_stop_words, mock_rec_list_splice, mock_correct_nick_for_, mock_splice_find, mock_correct_last_char_list, mock_correctLastCharCR, mock_check_if_msg_line, mock_get_nick_representative):
        mock_get_nick_representative.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/get_nick_representative_list")
        mock_check_if_msg_line.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/check_if_msg_line_list")
        mock_correctLastCharCR.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/correctLastCharCR_list")
        mock_correct_last_char_list.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/correct_last_char_list_list")
        mock_splice_find.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/keywords/splice_find_list")
        mock_correct_nick_for_.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/correct_nick_for_list")
        mock_rec_list_splice.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/rec_list_splice_list")
        mock_extended_stop_words.return_value = util.load_from_disk(self.current_directory + "/data/user_test/keywords/extended_stop_words")
        mock_top_keywords_for_nick.side_effect = util.load_from_disk(self.current_directory + "/data/user_test/keywords/top_keywords_for_nick")
        expected_keywords_filtered = util.load_from_disk(self.test_data_dir + "keywords/keywords_filtered")
        expected_user_keyword_freq_dict = util.load_from_disk(self.test_data_dir + "user_keyword_freq_dict")
        expected_user_words_dict = util.load_from_disk(self.test_data_dir + "keywords/user_words_dict")
        expected_nicks_for_stop_words = util.load_from_disk(self.test_data_dir + "keywords/nicks_for_stop_words")
        expected_sorted_keywords_for_channels = util.load_from_disk(self.test_data_dir + "keywords/sorted_keywords_for_channels")
        expected_captured_output = util.load_from_disk(self.current_directory + "/data/user_test/keywords/stdout_captured_output")
        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, sorted_keywords_for_channels = user.keywords(self.log_data , self.nicks, self.nick_same_list)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_captured_output, output)
        self.assertEqual(expected_keywords_filtered, keywords_filtered)
        self.assertEqual(expected_user_keyword_freq_dict, user_keyword_freq_dict)
        self.assertEqual(expected_user_words_dict, user_words_dict)
        self.assertEqual(expected_nicks_for_stop_words, nicks_for_stop_words)
        self.assertEqual(expected_sorted_keywords_for_channels, sorted_keywords_for_channels)

    @patch("lib.config.ENABLE_SVD", new = False)
    @patch("lib.config.ENABLE_ELBOW_METHOD_FOR_K", new = False)
    @patch("lib.config.NUMBER_OF_CLUSTERS", new = 11)
    @patch("lib.config.SHOW_N_WORDS_PER_CLUSTER", new = 10)
    @patch("lib.config.CHECK_K_TILL", new = 20)
    @patch("lib.analysis.user.keywords", autospec = True)
    @patch("lib.analysis.user.extended_stop_words", autospec = True)
    @patch("lib.analysis.user.time", autospec = True)
    def test_keywords_clusters(self, mock_time, mock_extended_stop_words, mock_keywords):
        keywords_filtered = util.load_from_disk(self.test_data_dir + "keywords/keywords_filtered")
        user_keyword_freq_dict = util.load_from_disk(self.test_data_dir + "user_keyword_freq_dict")
        user_words_dict = util.load_from_disk(self.test_data_dir + "keywords/user_words_dict")
        nicks_for_stop_words = util.load_from_disk(self.test_data_dir + "keywords/nicks_for_stop_words")
        sorted_keywords_for_channels = util.load_from_disk(self.test_data_dir + "keywords/sorted_keywords_for_channels")

        mock_keywords.return_value = keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, sorted_keywords_for_channels
        mock_extended_stop_words.return_value = util.load_from_disk(self.current_directory + "/data/user_test/extended_stop_words")
        mock_time.return_value = 0
        expected_captured_output = util.load_from_disk( self.test_data_dir + "stdout_captured_output_keywords_clusters");

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        user.keywords_clusters(self.log_data, self.nicks, self.nick_same_list, self.current_directory, "temp_output_keywords_clusters")
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_captured_output, output)
        self.assertTrue(filecmp.cmp(self.test_data_dir + "output_keywords_clusters.txt", self.current_directory + "/temp_output_keywords_clusters.txt"))
        os.remove(self.current_directory + "/temp_output_keywords_clusters.txt")


    @unittest.expectedFailure
    @patch("lib.config.ENABLE_SVD", new = True)
    @patch("lib.config.ENABLE_ELBOW_METHOD_FOR_K", new = True)
    @patch("lib.config.NUMBER_OF_CLUSTERS", new = 11)
    @patch("lib.config.SHOW_N_WORDS_PER_CLUSTER", new = 10)
    @patch("lib.config.CHECK_K_TILL", new = 20)
    @patch("lib.analysis.user.keywords", autospec = True)
    @patch("lib.analysis.user.extended_stop_words", autospec = True)
    @patch("lib.analysis.user.time", autospec = True)
    def test_keywords_clusters_expected_failure(self, mock_time, mock_extended_stop_words, mock_keywords):
        keywords_filtered = util.load_from_disk(self.test_data_dir + "keywords/keywords_filtered")
        user_keyword_freq_dict = util.load_from_disk(self.test_data_dir + "user_keyword_freq_dict")
        user_words_dict = util.load_from_disk(self.test_data_dir + "keywords/user_words_dict")
        nicks_for_stop_words = util.load_from_disk(self.test_data_dir + "keywords/nicks_for_stop_words")
        sorted_keywords_for_channels = util.load_from_disk(self.test_data_dir + "keywords/sorted_keywords_for_channels")

        mock_keywords.return_value = keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, sorted_keywords_for_channels
        mock_extended_stop_words.return_value = util.load_from_disk(self.current_directory + "/data/user_test/extended_stop_words")
        mock_time.return_value = 0
        expected_captured_output = util.load_from_disk( self.test_data_dir + "stdout_captured_output_keywords_clusters");

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        user.keywords_clusters(self.log_data, self.nicks, self.nick_same_list, self.current_directory ,"temp_output_keywords_clusters")
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_captured_output, output)
        self.assertTrue(filecmp.cmp(self.test_data_dir + "output_keywords_clusters.txt", self.current_directory + "/temp_output_keywords_clusters.txt"))
        os.remove(self.current_directory + "/temp_output_keywords_clusters.txt")


    def test_extended_stop_words(self):
        nicks_for_stop_words = util.load_from_disk(self.test_data_dir + "keywords/nicks_for_stop_words")
        stop_word_without_apostrophe = util.load_from_disk(self.current_directory + "/data/user_test/stop_word_without_apostrophe")
        expected_stop_words_extended = util.load_from_disk(self.current_directory + "/data/user_test/keywords/extended_stop_words")

        stop_words_extended = user.extended_stop_words(nicks_for_stop_words, stop_word_without_apostrophe)

        self.assertEqual(expected_stop_words_extended, stop_words_extended)


if __name__ == '__main__':
    unittest.main()
