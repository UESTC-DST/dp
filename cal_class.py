from sentence_transformers import SentenceTransformer, util
import pandas as pd
key_tech = pd.read_csv("./key_tech.csv")
cat_cn = key_tech["cat_cn"].to_list()
cat_en = key_tech["cat_en"].to_list()

def similarity(sentence_one):
    sentences_1 = [sentence_one]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings1 = model.encode(sentences_1, convert_to_tensor=True)
    embeddings2 = model.encode(cat_en, convert_to_tensor=True)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    return cosine_scores

def get_class(sentence_one, n_cat=3):
    """
    简单的分类匹配函数，将sentence匹配至某三个类别
    param:  sentence_one:str 用于分析的句子，例如论文标题，必须是英语
            n_cat:int 返回class_str中包含的类别数量，默认3.
    return: (class_str, cat_score)
        class_str:str 分类字符串，@@相隔
        cat_score:tuple 类别得分列表，包含类别index，类别，分数
    """
    if sentence_one is None or isinstance(sentence_one, float) or len(sentence_one) <= 0:
        return "",[]
    cosine_scores = similarity(sentence_one)
    scores = cosine_scores.tolist()[0]
    cat_score = []
    for i, (c, score) in enumerate(zip(cat_cn, scores)):
        cat_score.append((i, c, score))
    cat_score = sorted(cat_score, key= lambda item: item[2],reverse=True)
    result = ""
    for i in range(n_cat):
        result += cat_cn[cat_score[i][0]]
        result += "@@"
    result = result[:-2]
    return result, cat_score