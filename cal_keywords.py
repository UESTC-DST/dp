from rakun2 import RakunKeyphraseDetector

def get_keywords(text, n_keywords=5):
    """
    提取一段文字中的关键词
    param:  text:str 文本，语言英语
            n_keywords: 关键词数量，默认5
    return: keyword_str:str 关键词字符串，@@相隔
    """
    if text is None or isinstance(text, float) or len(text) <= 0:
        return ""
    hyperparameters = {"num_keywords": n_keywords,
                   "merge_threshold": 1.1,
                   "alpha": 0.3,
                   "token_prune_len": 3}

    keyword_detector = RakunKeyphraseDetector(hyperparameters)
    out_keywords = keyword_detector.find_keywords(text, input_type="string")
    result = [k for (k, score) in out_keywords]

    keyword_str = ""
    for s in result:
        keyword_str += str(s)
        keyword_str += "@@"
    keyword_str = keyword_str[:-2]
    return keyword_str