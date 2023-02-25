from algorithm.cosine_similarity import CosineSimilarity
from algorithm.jaccard import JaccardSimilarity
from algorithm.simhash import SimHashSimilarity


def algorithmAll(content_x,content_y):
    if(len(content_x)<4 or len(content_y) < 4):
        if (content_x==content_y):
            return [1,1,1]
        else:
            return [0,0,0]

    else:
        data=[]
        similarityA = CosineSimilarity(content_x, content_y)
        similarityA = similarityA.main()
        print(similarityA)
        print('相似度: %.2f%%' % (similarityA*100))

        similarityB=JaccardSimilarity(content_x, content_y)
        similarityB = similarityB.main()
        print('相似度: %.2f%%' % (similarityB*100))

        similarityC = SimHashSimilarity(content_x, content_y)
        similarityC = similarityC.main()
        threshold = 3
        print(f'海明距离：{similarityC} 判定距离：{threshold} 是否相似：{similarityC <= threshold} 相似度：{similarityC/threshold}')
        temp=0
        if(similarityC <= threshold):
            temp=1
        else:
            temp=0
        data.append(round(similarityA,2))
        data.append(round(similarityB,2))
        data.append(temp)
        return data

def algorithmSelect(a,b):
    sum = 0
    z = zip(a, b)
    print(z)

    for i, j in z:
        if (i == j):
            sum = sum + 1
    temp=0
    if sum/len(a)>0.5:
        temp=1
    else:
        temp=0
    return [sum/len(a),sum/len(a),temp]