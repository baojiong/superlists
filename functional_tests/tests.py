# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys


class NewVisitorTest(StaticLiveServerTestCase):

    # @classmethod
    # def setUpClass(cls):
    #     print('setUpClass')
    #     for arg in sys.argv:
    #         # if 'liveserver' in arg:
    #         cls.server_url = 'http://' + arg.split('=')[1]
    #         return
    #     super().setUpClass()
    #     cls.server_url = cls.live_server_url
    #
    # @classmethod
    # def tearDownClass(cls):
    #     if cls.server_url == cls.live_server_url:
    #         super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        # assertIn 是check一个元素是否在一个列表里，所以文本必须完全一致
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):

        # 伊迪丝听说又一个很酷的在线待办事项应用，她去看了这个应用的首页
        self.browser.get(self.server_url)

        # 她注意到网页的标题和头部都包含"To-Do"这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # 她在一个文本框中输入了 "Buy peacock feathers"
        # 伊迪丝的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        # 她按回车键后，被带到了一个新的页面
        # 待办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中有显示了一个文本框， 可以输入其他待办事项
        # 她输入了"Use peacock feathers to make a fly"
        # 伊迪丝做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，她的清单中显示了这2个待办事项
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # 现在一个叫做佛朗西斯的新用户访问了网站

        ## 我们使用新浏览器会话
        ## 确保伊迪丝的信息不会从cookie中泄漏出来 #
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 弗朗西斯访问首页，页面看不到伊迪丝的清单
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # 弗朗西斯输入一个新待办事项， 新建一个清单
        # 他不想伊迪丝那样兴趣盎然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Milk')
        inputbox.send_keys(Keys.ENTER)

        # 弗朗西斯获得了他的唯一URL
        francis_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.assertNotEqual(francis_url, edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)
        self.assertIn('Buy Milk', page_text)

    def test_layout_and_styling(self):
        # 伊迪丝访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 她看到输入框居中
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)

        # 她新建清单后，输入框仍然居中
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)
