## 工具包
---

### 使用说明
<details>
<summary>
关键词提取工具
</summary>
<br/>
文件：cal_class.py

功能：从`text`中提取n个关键字，并返回@@相隔的字符串。

安装依赖：

注：可能需要python3.9,如果失败请参照[Rakun2](https://github.com/SkBlaz/rakun2)重新创建conda环境。
```
pip install rakun2
```

</details>

<details>
<summary>
句子分类工具
</summary>
<br/>
文件：cal_keywords.py

功能：根据`text`分类，列表列表由key_tech.csv指定。

安装依赖：
```
pip install sentence_transformers, pandas
```

</details>

---

### Acknowledgement
The repo is partly reused from projects listed below. We thank for their open source spirit.

- [Rakun2](https://github.com/SkBlaz/rakun2)
- [sentence_transformers](https://github.com/UKPLab/sentence-transformers)