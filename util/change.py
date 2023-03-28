class Emotion:
    def __init__(self):
        pass
  #감정조절,스트레스,슬픔,속상,외로움,불안,걱정,긴장,중립,긍정,자신감,성실,행복
    gamjung = 0
    stress = 1
    sulpum = 2
    sad = 3
    lonely = 4
    bulan = 5
    worry = 6
    nervous = 7
    jungrip = 8
    positive = 9
    confidence = 10
    sungsil = 11
    happy = 12

        
    def to_num(self, st):
        st = st.strip()
        if st == "감정조절":
            return self.gamjung
        if st == "스트레스":
            return self.stress
        if st == "슬픔":
            return self.sulpum
        if st == "속상":
            return self.sad
        if st == "외로움":
            return self.lonely
        if st == "불안":
            return self.bulan
        if st == "걱정":
            return self.worry
        if st == "긴장":
            return self.nervous
        if st == "중립":
            return self.jungrip
        if st == "긍정":
            return self.positive
        if st == "자신감":
            return self.confidence
        if st == "성실":
            return self.sungsil
        if st == "행복":
            return self.happy
        
