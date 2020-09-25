﻿# 2DGP 텀프로젝트

2D게임프로그래밍 텀프로젝트 내용이다.

## SIHAW TOWN
![enter image description here](https://lh3.googleusercontent.com/proxy/4WQ4Qvcyfhxm6KTNvsYa-shnF_ffgvAEtNKwxvnDHvvoEKjtYXvO7VDlP_SiYGSOejtYwlFEx-MKbgw)
시화타운은 스타듀밸리를 원작으로 한 카피 게임이다.
>스타듀밸리는 농장경영 게임이며 4계절 특성에 맞는 작물을 키워 농장을 발전 시키는 게임이다. 농사, 채집, 낚시, 채광 등으로 돈을 벌 수 있으며 돈은 집, 농장, 도구 등을 업그레이드 하는데 주로 사용한다. 마을 npc와 호감도를 쌓을 수 있으며 게임 내 다양한 이벤트가 있다.

시화타운은 스타듀밸리의 모든 기능을 구현하진 못하더라도 핵심 기능들은 구현할 예정이다. 게임의 주된 목적은 농사에 초점에 맞춰 진행 할 것이다. 조작법은 스타듀밸리와 마찬가지로 w,s,a,d 와 마우스 클릭으로 할 것이다.

## GameState
**GamaeState**는 총 5개로 구성되어있다.
각 **GameState**마다 이동 조건은 밑에 다이어그램으로 표현하였다.
![enter image description here](https://i.esdrop.com/d/AZTYUHU8Kp.jpg)
**Start_State**
- 게임 시작시 가장 먼저 보여주는 GameState이다.
- 키, 마우스 이벤트는 존재 하지 않는다.
- 객체는 로고 화면만 보여준다.

![enter image description here](https://i.esdrop.com/d/RD2MMuPjl5.jpg)
**Title_State**
- 게임 시작 및 게임 나가기를 선택할 수 있는 타이틀이다.
- 마우스 이벤트만 존재하며 마우스 왼쪽 클릭으로 진행한다.
- 객체는 타이틀 화면과 아이콘으로 구성된다.

![enter image description here](https://mblogthumb-phinf.pstatic.net/MjAxODA3MTZfMzEg/MDAxNTMxNzE5NjgwNDU1.hTAosRMRD48Piu20tVCIhQCVmVDQqKYtYObGH930ypEg.fUKvaX6RlbSEWsNVLcRUVU9QUJFr_HocLARLd8Tbcz8g.PNG.elancia_0/08.png?type=w800)
**Main_State**
- 게임의 핵심 메인 스테이트이다.
- 키 입력은 w, a, s, d 로 움직이고 마우스 왼쪽 클릭으로 도구를 사용하며, 오른쪽 클릭으로 상호작용한다. 그리고 마우스 휠로 아이템을 바꾼다.
- 시간, 돈 을 알려주는 UI와 아이템 목록 UI가 있다.
- 객체는 맵툴을 이용한 Tile로 구성된 맵과 오브젝트로 구성된다.
- 캐릭터들은 프레임과 sprite_sheet를 이용해 애니메이션으로 구현한다.

![enter image description here](https://postfiles.pstatic.net/MjAxODEwMzBfMTgy/MDAxNTQwODMzODA0NTY1.xfeNK24S0YWngGsdQ0dVLZIaG_ArgPlnJ245J6jiQisg.UCq8IpMkvzqsOshgYczpSqDTqezagpbA9yYD83JzBmgg.PNG.900pixel/image_6559740771540833773088.png?type=w773)
**Shop_State**
- 상점을 이용하는 State이다.
- 아이템을 사고 팔고 하는 공간이다.
- 마우스 이벤트만 존재하며, 마우스 왼쪽 클릭으로 상호작용한다.
- 객체는 아이템들과 TextBox로 구성된다.



![enter image description here](https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory2&fname=http://cfile27.uf.tistory.com/image/224E9E4858D638552E19B6)
**Menu_State**
- 아이템, 호감도, 종료 등 게임의 전반적인 캐릭터 상태, 시스템을 관리하는 시스템이다.
- 마우스 이벤트만 존재하며, 왼쪽 클릭으로 상호작용한다.
- TextBox, 아이템, 캐릭터, 아이콘 등 객체들로 이루어진다.

**Game State Diagram**
```mermaid
graph TD;
    Start_State--일정시간 지난 후-->Title_State;
    Title_State--종료 버튼-->Quit;
    Title_State--시작 버튼-->Main_State;
    Main_State--ESC 키-->Menu_State;
    Main_State--상점 이용-->Shop_State;
    Shop_State--나가기-->Main_State;
    Menu_State--ESC 키-->Main_State;
    Menu_State--종료 버튼-->Quit;
 ```
## 필요한 기술
**배운 기술**
- Map Tool
- Photoshop little Skill

**배울 것으로 기대되는 기술**
- Python version Map Tool
- Print Text, Font
- Play Sound

**요청할 기술**
![enter image description here](https://i.esdrop.com/d/o2au5X0yZQ.png)
![enter image description here](https://i.esdrop.com/d/zBMH6zuX0I.png)
- 머리카락이 이런 파일로 존재할 때 플레이가 원하는 색깔을 지정하면 그 색깔에 맞게 머리카락 색을 바꿔주는 스킬을 알고 싶습니다. 스킬 이름을 몰라 이렇게 예시로 설명했습니다.
- 예시로 머리카락을 들었지만 플레이어 피부색, 옷 색 뿐만 아니라 자동차 색들 다양한 방면에 사용할 수 있을 거 같아 꼭 배우고 싶습니다.
