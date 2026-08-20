import nltk

# 최초 실행 시에만 아래 주석을 풀고 데이터를 다운로드하세요.
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk.corpus import wordnet

def look_up(query: str):
    try:
        # 단어의 품사별 의미(Synset) 목록 가져오기
        query = query.lower()
        synsets = wordnet.synsets(query)
        
        if synsets:
            synsets = sorted(
                synsets, 
                key=lambda s: (
                    0 if query in s.name().lower() 
                    else (1 if any(query in lemma.lower() for lemma in s.lemma_names()) else 2)
                )
            )
            print("정렬된 synsets:", synsets) # 디버깅용 출력
            
            # NLTK 품사 기호(n, v, a, s, r)를 매핑
            pos_map = {
                'n': 'noun',
                'v': 'verb',
                'a': 'adjective',
                's': 'adjective',
                'r': 'adverb'
            }
            
            # 찾은 모든 의미를 리스트로 담아 반환 (인덱스 이동 기능 지원용)
            meanings_list = []
            for meaning in synsets:
                raw_pos = meaning.pos()
                pos_type = pos_map.get(raw_pos, raw_pos)
                
                meanings_list.append({
                    'type': pos_type,
                    'meaning': meaning.definition()
                })
                
            return meanings_list
        else:
            return False
            
    except Exception as e:
        # 디버깅이 필요할 경우 print(e) 추가 가능
        return "error"

# 테스트 예시
# if __name__=="__main__":
#     print(look_up("computer"))