from pykis import KisAuth, PyKis, KisQuote, KisOrder, KisStock

auth = KisAuth(
     # HTS 로그인 ID  예) soju06
     id="",
     # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
     appkey="",
     # 앱 시크릿 키  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
     secretkey="",
     # 앱 키와 연결된 계좌번호  예) 00000000-01
     account="73265188-01",
     # 모의투자 여부
     virtual=False,
 )

 # 안전한 경로에 시크릿 키를 파일로 저장합니다.
auth.save("secret.json")

# 실전투자용 PyKis 객체 생성
kis = PyKis(KisAuth.load("secret.json"), keep_token=True)

# 국내 주식
hanmi: KisStock = kis.stock("128940")  # SK하이닉스 (코스피)

print(
    f"""
종목코드: {hanmi.symbol}
종목명: {hanmi.name}
종목시장: {hanmi.market}
"""
)

# 또한 info 프로퍼티를 통해 상세 정보를 얻을 수 있습니다.
print(
    f"""
종목코드: {hanmi.info.symbol}
종목표준코드: {hanmi.info.std_code}
종목명: {hanmi.info.name}
종목영문명: {hanmi.info.name_eng}
종목시장: {hanmi.info.market}
종목시장한글명: {hanmi.info.market_name}
"""
)

# 한미약품 1주 시장가 매수 주문
order: KisOrder = hanmi.buy(qty=1)
# 한미약품 1주 지정가 매수 주문
order: KisOrder = hanmi.buy(price=350000, qty=1)
# 한미약품 전량 시장가 매도 주문
order: KisOrder = hanmi.sell()
# 한미약품 전량 지정가 매도 주문
order: KisOrder = hanmi.sell(price=194700)

####