# ProjectTeamGreat
Established to create NLP method for early 2000's K-POP lyrics.

## 프로젝트 가이드라인

  1) 코퍼스 수집

    코퍼스는 팀 당 최소 200개, 각 개인별로 균등하게 나눌 것을 권장하고 있습니다. 
    따라서 팀원당 50 최소 여개의 코퍼스를 수집하는 것이 됩니다.
    코퍼스를 200개 이상 수집 해오는 팀에게는 가산점이 붙는다고 합니다.
    이 부분은 추후에 상의를 통하여 코퍼스 수집 갯수를 늘릴지 말지 결정하도록 하겠습니다.
  
    1-2) 수집 방식
    
      https://www.melon.com/index.htm 곡 정보와 가사는 멜론이 제일 구체적이기 때문에 주 수집은 멜론에서 하도록합니다.
      우리 팀은 2000~2010년 사이의 아이돌 그룹에 대해 조사를 해야 합니다.
      다만 조사하는 과정에서 서로 겹치는 일을 피하기 위해,
      제가 해당 리포지토리의 ""data/아이돌목록.xlsx""를 참고하여 각 팀원 별 조사 영역을 지정 해두었습니다.
    
      개인에게 지정해둔 영역은 제가 ""[자신의 영어이니셜]/toFind.txt""에 적어두었으니 코퍼스 수집을 시작하시기 전에 확인을 해주세요.
      그리고 수집을 한 데이터는 ""[자신의 영어이니셜]/songs.xlsx""에 기입하여 주세요.
      해당 파일에 교수님이 요구 하신 코퍼스 형식대로 올려 두었으니 거기에 맞춰 작성하시면 됩니다.
      마지막에 tsv파일로 집계하는건 제가 할 것이니 우선 엑셀로 데이터를 정리만 해두시면 됩니다.
    
  2) 프로젝트 현황
  
    교수님이 제시한 가이드라인 상에선 데이터 수집 전략과 응용 프로그램에 개발 대한 구체적인 서술이 필요합니다.
    이번 중간고사에서는 실질적인 개발은 필요하지 않으나, 개발하려는 응용 프로그램에 대한 이론적인 계획 정도는 완성해야 할 듯 합니다.
    또한 중간 발표시에는 데이터 수집 전략에 대해서도 언급을 하고 넘어가야 될 것 같습니다.
    
    교준씨가 웹 크롤러를 구축하신 덕에 각 조사영역에 대한 raw 데이터들 상당 수 많은 양을 얻을 수 있게 되었습니다.
    해당 데이터들은 조금 더 정제 할 필요가 있으나, 큰 뼈대들은 전부 구할 수 있는 상태 입니다.
    향후 프로젝트에선 이 데이터들을 어떤 방식으로 정제하고 사용 할 지에 대한 논의가 필요한 상태입니다.
  

### 주제 : 
성별 장르 제목 기반한 작사 도우미

### 필요성 : 
가사를 작성하는데 어려움을 느끼는 사람들의 고충을 덜어주고 
영감을 주어 빠르고 효율적으로 작사를 하기 위함.
가사를 못쓴다 관련한 기사 같은 거 하나 껴놓기

### 기술 개발 전략 : 
데이터는 멜론 데이터를 활용할 것 
임베딩은 어떻게 할 것
활용할 자연어 처리 모델 (BERT? GRU?)
UI 간단히

### 데이터 수집 전략 :
크롤링 툴 파이참 찍어주기
일본어는 뺐다.
순위는 일일히 했다.

### 역할 :
김은호 - 팀장
현소미 - 제안서 작성, 정보수집
윤주석 - 발표
진교준 - 메인 코더

