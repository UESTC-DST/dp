## 工具包

---

### 使用说明

<details>
<summary>
关键词提取工具
</summary>
<br/>



**文件:** cal_keywords.py

**功能:** 从`text`中提取n个关键字，并返回@@相隔的字符串。

**安装依赖：**

注：可能需要python3.9,如果失败请参照[Rakun2](https://github.com/SkBlaz/rakun2)重新创建conda环境。

```
pip install rakun2
```

**使用:**

具体请看注释

```
from cal_keywords import get_keywords

keywords_str = get_keywords("A dog is here.")
```

</details>

<details>
<summary>
句子分类工具
</summary>
<br/>



**文件:** cal_class.py

**功能:** 根据`text`分类，类别列表由key_tech.csv指定。

**安装依赖:**

```
pip install sentence_transformers, pandas
```

**使用:**

具体请看注释

```
from cal_class import get_class

class_str, cat_scores = get_class("A dog is here.")
```

</details>

<details>
    <summary>
        国际版领英爬虫
    </summary>
    <br />
    
**文件**：utils.LinkedInScaper.py


**功能**：爬取给定人名的**工作经历、教育履历以及个人简历**

**注意事项**：1、使用务必**打开VPN**；2、在浏览器上先手动登录个人的国际版领英账号，然后使用插件**Edit This Cookie**将Cookie导出到**utils.damai_cookie.txt**中

**安装依赖**：

```
pip install selenium
```

**注意：建议python版本为3.7.3，如果selenium报错，请降低selenium的版本**

**使用**：具体使用请查看example.linkedIn_example.py

</details>

</details>

<details>
    <summary>
        sementic scholary爬虫
    </summary>
    <br />


**文件**：utils.sementic.example.py

**功能**：使用官方API来爬取论文信息

**注意事项**：官方限定了使用频率，请求频率为100次/5分钟

**安装依赖**：

```
pip install requests
```

**使用**：具体使用请查看example.sementic_example.py

</details>

---

### Acknowledgement

The repo is partly reused from projects listed below. We thank for their open source spirit.

- [Rakun2](https://github.com/SkBlaz/rakun2)
- [sentence_transformers](https://github.com/UKPLab/sentence-transformers)
