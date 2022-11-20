from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys
import numpy as np
import json

# 模拟等待
def wait(base=np.random.randint(3,6)):
    time.sleep(base + random.random() * 2)

'''
务必在使用前打开VPN
'''
class LinkedInScraper:
    '''
        <h>注意事项：在使用前，务必开启全局VPN，之后在领英官网登录账号，再配合Edit this Cookie浏览器插件导出Cookies到当前目录下的damai_cookies.txt<h>\br
        该类通过selenium来爬取领英的职位、教育以及个人简介三部分信息
    '''
    # 注意：使用前，请提前打开VPN
    def __init__(self,chrome_driver:str='./chromedriver.exe') -> None:
        np.random.seed(5)
        with open('./damai_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())
        # 往browser里添加cookies
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.get('https://www.linkedin.com/checkpoint/lg/sign-in-another-account')
        # 此处可以用谷歌浏览器插件EditThisCookie来获取cookie，数组长度不一定为1
        for cookie in json.load(open('./damai_cookies.txt')):
            cookie.pop('sameSite')
            self.driver.add_cookie(cookie)
        self.driver.maximize_window()
        self.driver.refresh()
        wait()
        # # 先定位到邮箱框和密码框
        # mailInput = self.driver.find_element_by_id('username')
        # mailInput.send_keys(mail)
        # wait()
        # pwdInput = self.driver.find_element_by_id('password')
        # pwdInput.send_keys(password)
        # wait(1)
        # loginButton = self.driver.find_element_by_css_selector('.btn__primary--large.from__button--floating')
        # loginButton.click()
        # wait()

    def search(self,keywords):
        '''
            Input: keywords: 应包含人名以及单位(减少重名带来的错误)，人名和单位之间使用空格或者tab隔开
            Return: 返回教育信息和单位履历
        '''
        empty = json.dumps({'education':'','work':''})
        # 先回到搜索初始页面
        # self.driver.get('https://www.linkedin.com/feed/')
        # wait()
        # 定位搜索框
        searchBox = self.driver.find_element_by_css_selector('.search-global-typeahead__input.always-show-placeholder')
        searchBox.clear()
        searchBox.send_keys(keywords)
        wait(0)
        searchBox.send_keys(Keys.ENTER)
        wait()

        # 获取搜索列表
        searchList = self.driver.find_element_by_css_selector('.search-results-container')

        try:
            # 判断是否为空
            searchList.find_element_by_css_selector('reusable-search-filters__no-results.artdeco-card.mb2')
            return empty
        except:
            pass
        try:
            searchList = searchList.find_element_by_css_selector('.app-aware-link.search-nec__hero-kcard-v2-link-wrapper.link-without-hover-state.link-without-visited-state.t-normal.t-black--light')
        except:
            try:
                searchList = searchList.find_element_by_css_selector('.reusable-search__entity-result-list.list-style-none')
                searchList = searchList.find_elements_by_css_selector('.reusable-search__result-container')[0]
            except:
                return empty
        # try:
        #     # 此处如果成功，则说明搜索到多个内容
        #     searchList = searchList.find_element_by_css_selector('.reusable-search__entity-result-list.list-style-none')
        #     searchList = searchList.find_elements_by_css_selector('li')
        #     searchList = searchList[0]
        #     wait(0)
        # except:
        #     # 否则搜索到一个内容
        #     pass
        old_url = self.driver.current_url
        # 此处判断是否为领英会员，如果是领英会员参数为：.EntityPhoto-circle-3-ghost-person.ivm-view-attr__ghost-entity 
        icon = searchList.find_element_by_css_selector('.display-flex.align-items-center')
        icon.click()
        wait(10)
        # 此处要处理搜索对象为领英会员情况
        if old_url == self.driver.current_url:
            self.driver.get('https://www.linkedin.com/feed/')
            return empty
        self.total_list = self.driver.find_elements_by_css_selector('.artdeco-card.ember-view.relative.break-words.pb3.mt2')
        return json.dumps({'education':self.getEducation(),'work':self.getWork(),'country':self.getCountry()},ensure_ascii=False)
        # return json.dumps({'education':'','work':'','country':self.getCountry()})

    def find(self, elements, keyword):
        ''' 
            用来在领英个人页面的elements中查找拥有关键词的css_selector
            Input:
                elements: elements对应的列表
                keyword: 关键词
            Output:
                css_selector
        '''
        for element in elements:
            header = element.find_element_by_css_selector('.pvs-header__title-container')
            title = header.find_element_by_css_selector('span').text
            if title == keyword:
                return element
        return ''

    def getCountry(self):
        country = ''
        try:
            ph5 = self.driver.find_element_by_css_selector('.ph5.pb5')
            country = ph5.find_element_by_css_selector('.text-body-small.inline.t-black--light.break-words').text
            country = country.split(' ')[0]
        except:
            country = ''
        return country
    def getEducation(self):
        keyword = '教育经历'
        educationList = self.find(elements=self.total_list,keyword=keyword)
        if educationList == '':
            return json.dumps({'学校':'','时间':''},ensure_ascii=False)
        educationList = educationList.find_element_by_css_selector('.pvs-list__outer-container')
        educationList = educationList.find_element_by_css_selector('ul')
        educationList = educationList.find_elements_by_css_selector('.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column')

        return_education_list = []
        for education in educationList:
            return_education_list.append(self.getEduInfo(education))

        wait(1)
        return return_education_list
    
    def getWorkInfo(self,element):
        '''
            Input:
                element: 公司一条信息对应的element
            Return:
                inc: 公司名称
        '''
        info_list = element.find_elements_by_css_selector('.t-14.t-normal')
        inc,during = '',''
        if len(info_list) > 4:
            inc_name = element.find_element_by_css_selector('.display-flex.align-items-center')
            inc_name = inc_name.find_element_by_css_selector('span')
            inc = inc_name.find_element_by_css_selector('span').text.__str__()
            workList = element.find_elements_by_css_selector('.pvs-list__paged-list-item')
            during_list = []
            for _ in workList:
                div = _.find_element_by_css_selector('.display-flex.flex-row.justify-space-between')
                span = div.find_element_by_css_selector('.t-14.t-normal.t-black--light')
                during = span.find_element_by_css_selector('span').text.__str__()
                if '年' in during:
                    during_list.append(during.split('·')[0].strip())
            if len(during_list) >= 2:
                during = during_list[-1].split('-')[0] + ' - ' + during_list[0].split('-')[1]
        else:
            inc = info_list[0].find_element_by_css_selector('span').text.__str__()
            if len(info_list) >= 2:
                during = info_list[1].find_element_by_css_selector('span').text.__str__()
            during = during.split('·')[0]
            if '年' not in during:
                during = ''
        return json.dumps({'工作单位':inc.split('·')[0].strip(),'时间':during.strip()},ensure_ascii=False)

    def getEduInfo(self,element):
        '''
            Input:
                element: 一条教育信息对应的element
            Return:
                返回学校名称
        '''
        div = element.find_element_by_css_selector('.display-flex.flex-row.justify-space-between')
        during = ''
        try:
            during = div.find_element_by_css_selector('.t-14.t-normal.t-black--light').text.__str__().split('\n')[0]
        except:
            pass
        a = div.find_element_by_css_selector('a')
        div = a.find_element_by_css_selector('div')
        span = div.find_element_by_css_selector('span')
        school = span.find_element_by_css_selector('span').text
        return json.dumps({'学校':school,'时间':during.split('·')[0]},ensure_ascii=False)
    
    def getWork(self):
        keyword = '工作经历'
        workList = self.find(elements=self.total_list,keyword=keyword)
        if (workList == ''):
            return json.dumps({'工作单位':'','时间':''},ensure_ascii=False)
        # 判断是否有展开按钮
        try:
            works = []
            expand = workList.find_element_by_css_selector('.pvs-list__footer-wrapper')
            expand.click()
            wait()
            work_list = self.driver.find_element_by_css_selector('.artdeco-card.ember-view.pb3')
            workList = work_list.find_element_by_css_selector('.pvs-list__container')
            work_list = work_list.find_element_by_css_selector('ul')
            work_list = work_list.find_elements_by_css_selector('.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated')

            for single_work in work_list:
                works.append(self.getWorkInfo(single_work))
            return works
        except:
            work_container = workList.find_element_by_css_selector('.pvs-list__outer-container')
            work_list = work_container.find_element_by_css_selector('ul')
            work_list = work_list.find_elements_by_css_selector('.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column')
            works = []
            
            for single_work in work_list:
                works.append(self.getWorkInfo(single_work))
            return works
        
    def getName(self,driver):
        return driver.find_element_by_css_selector('.text-heading-xlarge.inline.t-24.v-align-middle.break-words').text

