import requests as rq
import time
import queue
import json

class getPaperInfo():
    '''
        官方API限制了访问次数，为每5分钟，最多100次，等待方式采用了时间队列
    '''
    def __init__(self,wait_type:str='time_queue'):
        self.getIdURL = 'http://api.semanticscholar.org/graph/v1/paper/search?limit=1&query={}'
        self.getPaperInfoFromTitleURL = 'https://api.semanticscholar.org/graph/v1/paper/{}?fields=authors,title,abstract,publicationDate,citationCount,journal,publicationTypes,citationStyles'
        self.getPaperInfoFromNameURL = 'https://api.semanticscholar.org/graph/v1/author/search?query={}&fields=name,aliases,url,papers.title,papers.authors,papers.journal,papers.year,papers.abstract,papers.publicationTypes,papers.citationCount,papers.citationStyles&limit={}'
        self.timeStamp = queue.Queue(maxsize=99)
        fields = 'name,aliases,url,papers.title,papers.authors,papers.journal,papers.year,papers.abstract,papers.publicationTypes,papers.citationCount,papers.citationStyles'.split(',')
        self.fields = fields
        self.wait_type = wait_type
    
    def check_time(self,st:float=0)->None:
        '''
            在类初始化是建立时间队列，判断100个任务的间隔时间不小于5分钟，如果小于5分钟就循环等待判断
            Params:
                st: 没必要输入，只是为了方便函数处理
            Return:
                无
        '''
        st = 0
        if self.timeStamp.full():
            st = self.timeStamp.get()
        while self.timeStamp.full() and time.time() - st <= 300:
            time.sleep(1)
        self.timeStamp.put(time.time())

    def wait_n_seconds(self,st:float,second:float=3)->None:
        '''
            每步操作要求执行3s及以上，不足3s的，则等待满3s
            Params:
                st:函数开始执行的
        '''
        ed = time.time()
        time.sleep(second-ed+st)

    def get_paper_id(self,title:str)->str:
        '''
            根据论文标题，获取论文的id
            Params:
                title: 论文的标题
            Return:
                返回为字符型，如果查询到了则返回ID，没有查询到则返回-1
        '''
        self.check_time()
        paperId = rq.get(self.getIdURL.format(title))
        paperId = paperId.json()
        try:
            return json.dumps(paperId['data'][0]['paperId'])
        except:
            return '-1'
    
    def get_paper_info(self, paperId:str)->str:
        '''
            根据论文ID获取论文信息
            Params:
                paperId: 论文ID
            Return:
                返回获取到的论文信息
        '''
        self.check_time()
        paperInfo = rq.get(self.getPaperInfoFromTitleURL.format(paperId))
        return paperInfo.json()

    def get_paperInfo_from_title(self,title:str)->str:
        '''
            根据论文标题获取论文信息
            Params:
                title: 论文标题
            Return:
                返回论文信息
        '''
        return self.get_paper_info(self.get_paper_id(title))

    def get_paperInfo_from_name(self,name:str,limit:int=1)->str:
        '''
            根据作者姓名查询其名下所有论文信息，注意：因为Sementic Scholar排序算法没办法选择，所以此处不一定是H指数最高的学者
            Params:
                name: 学者姓名
                limit: 至多采集limit个同名学者的信息
            Return:
                采集到的学着信息，格式为list
        '''
        self.check_time()
        results = rq.get(self.getPaperInfoFromNameURL.format('+'.join(name.split()),limit)).json()
        try:
            return results['data'][0]['papers']
        except:
            return ''