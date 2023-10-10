# new_clothing_store

1) 사용자가 지정하는 색에 따른 옷 추천: 각 픽셀의 RGB 평균 이용하여 KNN클러스터링
2) Virtual try on: CVPR 2021 “Parser-Free Virtual Try-on via Distilling Appearance Flows”
3) 원하는 옷이 있는 위치로 길 안내: 터틀봇3 버거 이용하여 주행
   
*통신 - 터틀봇<->사용자 UI: TCP
      - 영상처리 서버 <-> 사용자 UI: SSH
*사용자 UI: pyQT
