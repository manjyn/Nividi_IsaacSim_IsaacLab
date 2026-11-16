from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
from pathlib import Path
D=Path(__file__).parent
pdfmetrics.registerFont(TTFont('K','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('B','C:/Windows/Fonts/malgunbd.ttf'))
c=canvas.Canvas('Isaac-Sim-Lab-Guide-KO.pdf',pagesize=(600,800))
c.setTitle('Isaac Sim과 Isaac Lab 첫 실습')
S='https://docs.isaacsim.omniverse.nvidia.com/5.1.0/'
L='https://isaac-sim.github.io/IsaacLab/v2.3.0/source/'
sim=S+'introduction/quickstart_isaacsim.html'
lab=L+'tutorials/02_scene/create_scene.html'
install=L+'setup/installation/binaries_installation.html'
def t(x,y,s,size=11,f='K',col='#192c32'):
 c.setFillColor(HexColor(col));c.setFont(f,size);c.drawString(x,y,s)
def page(n,k,title,sub):
 global y
 t(38,752,k,11,'B','#007269');t(38,706,title,25,'B');t(38,674,sub,11);y=641
 t(38,25,'ISAAC  /  입문 실습 노트',9,'B','#50706f');t(539,25,f'{n} / 5',9)
def line(s,size=11,f='K'):
 global y
 words=s.split();row=''
 for w in words:
  if pdfmetrics.stringWidth((row+' '+w).strip(),f,size)>520:
   t(38,y,row,size,f);y-=18;row=''
  row=(row+' '+w).strip()
 t(38,y,row,size,f);y-=19
def step(h,s):
 global y
 y-=9;line(h,13,'B');y-=1;line(s);y-=4
def link(s,u):
 global y
 t(38,y,s,9,'B','#007269');c.linkURL(u,(38,y-3,38+pdfmetrics.stringWidth(s,'B',9),y+10));y-=21
def code(s):
 global y
 c.setFillColor(HexColor('#eaf3f1'));c.rect(38,y-7,524,22,fill=1,stroke=0);t(47,y,s,9.4,'Courier');y-=25
def pic(name,idx,h,cap,u):
 global y
 im=Image.open(D/name)
 if idx: im.seek(idx)
 w=min(524,h*im.width/im.height);hh=w*im.height/im.width
 c.drawImage(ImageReader(im.convert('RGB')),38,y-hh,w,hh);y-=hh+14;link(cap,u)
def end():
 assert y>35,y
 c.showPage()
page(1,'시작하기     /     Windows 명령 프롬프트 기준','Isaac Sim과 Isaac Lab 첫 실습','큐브를 바닥에 떨어뜨린 뒤, 같은 시뮬레이터에서 여러 카트폴을 움직여 봅니다.')
step('두 도구는 어디에서 만나나요?','Isaac Sim에서는 장면을 열어 물체를 배치하고 움직임을 눈으로 확인합니다. Isaac Lab은 Python 코드에서 그 시뮬레이션을 제어하는 프레임워크입니다. 이 가이드의 Lab 실습에서는 명령을 입력하면 Sim 창이 열립니다.')
step('실습 기준 버전을 맞추세요','이 문서는 Isaac Sim 5.1.0과 Isaac Lab v2.3.0을 짝지어 설명합니다. 다른 버전의 메뉴나 명령은 다를 수 있습니다. 아래 링크에서 GPU·드라이버·메모리 요건을 먼저 비교하세요.')
link('공식 문서 열기  /  Isaac Sim 5.1 시스템 요구 사항',S+'installation/requirements.html')
step('Isaac Sim을 설치하고 실행하세요','워크스테이션 설치 안내의 Windows 절차에 따라 5.1.0 배포본을 설치합니다. 아래는 설치 폴더가 C:\\isaacsim인 경우입니다. 다른 위치라면 경로를 바꾸세요.')
link('공식 문서 열기  /  워크스테이션 설치',S+'installation/install_workstation.html')
code(r'cd /d C:\isaacsim');code('isaac-sim.selector.bat')
line('App Selector에서 Isaac Sim을 실행합니다. 첫 시작은 오래 걸릴 수 있습니다. 메뉴가 반응하면 File > New로 빈 장면을 엽니다.')
step('이 순서로 따라오세요','2쪽에서 화면을 읽고, 3쪽에서 큐브의 낙하를 확인합니다. 4쪽에서 Lab을 연결한 뒤, 5쪽에서 환경 개수를 바꿔 같은 실험을 여러 번 나란히 실행합니다.')
end()
page(2,'ISAAC SIM     /     화면 읽기','큐브 하나로 익히는 편집 화면','Create > Shape > Cube를 누르고 큐브를 선택하세요. 아래 네 곳을 차례로 짚어 봅니다.')
pic('move_cube.webp',574,286,'그림 1  /  NVIDIA 기본 사용 튜토리얼 · 큐브 조작 장면에서 발췌  ↗',sim)
step('가운데  |  Viewport','장면을 보는 곳입니다. 큐브를 클릭하고 W를 누르면 이동 도구가 나타납니다. 파란 화살표를 끌어 높이를 바꿔 보세요. E는 회전, R은 크기 조절입니다.')
step('오른쪽 위  |  Stage','장면의 항목(prim)을 트리로 표시합니다. World 아래 Cube를 선택하면 화면에서 클릭한 것과 같은 물체가 선택됩니다. 물체가 겹쳐 있을 때 유용합니다.')
step('오른쪽 아래  |  Property','선택한 항목의 속성을 읽고 바꿉니다. Transform에서 Translate의 Z를 2로 입력하세요. 손으로 끌지 않고도 큐브 중심의 높이를 정확하게 지정할 수 있습니다.')
step('아래쪽과 왼쪽  |  Content와 재생 도구','Content에서는 파일과 에셋을 찾습니다. 왼쪽의 Play는 시간을 흐르게 하고 Stop은 실행을 끝냅니다. 다음 실습을 시작하기 전에 Stop 상태로 두세요.')
end()
page(3,'ISAAC SIM     /     첫 물리 실험','무엇을 더하면 큐브가 떨어질까요','같은 큐브를 두 번 재생해 모양을 만드는 기능과 물리 계산을 켜는 기능을 구분합니다.')
pic('physics_property.webp',155,262,'그림 2  /  NVIDIA 기본 사용 튜토리얼 · 물리 속성 실습 장면에서 발췌  ↗',sim)
step('1   바닥과 빛을 준비합니다','앞 장의 큐브를 그대로 두고 Create > Physics > Ground Plane을 추가합니다. 조명이 없다면 Create > Lights > Distant Light를 추가하세요.')
step('2   물리 속성이 없는 상태로 재생합니다','큐브가 바닥 위에 떠 있는지 확인하고 Play를 누릅니다. 시간이 흘러도 큐브는 그 자리에 있어야 합니다. 결과를 확인한 뒤 Stop을 누르세요.')
step('3   같은 큐브에 강체와 충돌을 추가합니다','Stage에서 /World/Cube를 고른 뒤 Property의 + Add > Physics > Rigid Body with Colliders Preset을 선택합니다. 강체는 중력에 반응하게 하고, 충돌은 바닥과 맞닿았을 때 통과하지 않게 합니다.')
step('4   낙하를 확인하고 장면을 저장합니다','다시 Play를 누릅니다. 큐브가 내려와 바닥 위에 멈추면 성공입니다. 움직이지 않으면 선택한 큐브의 Rigid Body를, 바닥을 통과하면 Collider와 Ground Plane을 확인하세요. Stop 후 File > Save As로 cube_drop.usd를 저장합니다.')
end()
page(4,'ISAAC LAB     /     설치와 첫 실행','Python에서 빈 시뮬레이터 열기','Sim 창을 닫고 시작하세요. 이 예제는 앞에서 저장한 USD 파일을 사용하지 않습니다.')
step('1   예제 코드 받기','Git이 설치된 Windows에서 명령 프롬프트(cmd)를 엽니다. 쓰기 가능한 작업 폴더로 이동한 뒤 아래 두 줄을 실행하세요. 이후 명령의 시작 위치는 IsaacLab 폴더입니다.')
code('git clone --branch v2.3.0 https://github.com/isaac-sim/IsaacLab.git');code('cd IsaacLab')
step('2   Sim 설치 폴더 연결하기','관리자 권한의 명령 프롬프트에서 같은 IsaacLab 폴더로 이동한 뒤 다음 줄을 실행하세요. 두 번째 경로는 python.bat가 들어 있는 실제 Sim 설치 위치여야 합니다.')
code(r'mklink /D _isaac_sim C:\isaacsim')
step('3   실습에 필요한 패키지 설치하기','원래 명령 프롬프트의 IsaacLab 폴더에서 실행하세요. 여기서는 Sim에 포함된 Python을 사용합니다. none은 별도의 강화학습 라이브러리를 설치하지 않는 옵션입니다.')
code('isaaclab.bat --install none')
step('4   빈 장면으로 연결 확인하기','아래 예제는 AppLauncher로 앱을 띄우고 SimulationContext로 시간을 한 단계씩 진행합니다. 장면에 물체와 빛을 넣지 않았으므로 검은 Viewport가 정상입니다.')
code(r'isaaclab.bat -p scripts\tutorials\00_sim\create_empty.py')
line('확인 기준: Sim 창이 열리고 터미널에 Setup complete가 표시됩니다. 터미널에서 Ctrl+Break로 종료한 뒤 다음 장으로 넘어가세요.')
step('실행 파일을 찾을 수 없다면','dir isaaclab.bat로 현재 폴더를 확인하고, dir _isaac_sim\\python.bat로 연결을 확인하세요. 일반 Python 대신 위 명령을 사용해야 같은 환경에서 실행됩니다.')
link('공식 문서 열기  /  Isaac Lab 바이너리 설치 및 확인  ↗',install)
end()
page(5,'ISAAC LAB     /     병렬 환경','카트폴 한 대를 네 대로 늘리기','카트폴은 레일을 따라 움직이는 카트에 막대를 관절로 연결한 장치입니다.')
pic('lab.jpg',0,194,'그림 3  /  Isaac Lab 공식 Interactive Scene 예제 · 여러 카트폴의 실행 화면  ↗',lab)
step('1   한 대만 실행합니다','IsaacLab 폴더에서 다음 명령을 입력하세요. 레일 위 카트와 막대가 나타납니다. 예제는 관절에 무작위 힘을 주므로 막대가 흔들리는 것이 정상입니다.')
code(r'isaaclab.bat -p scripts\tutorials\02_scene\create_scene.py --num_envs 1')
step('2   네 대를 비교합니다','Ctrl+Break로 종료하고 마지막 숫자만 바꿔 다시 실행하세요. 한 창 안에 같은 구조의 장치가 여러 개 놓입니다. 그림은 더 많은 환경을 띄운 공식 예시입니다.')
code(r'isaaclab.bat -p scripts\tutorials\02_scene\create_scene.py --num_envs 4')
step('3   Python 코드와 화면을 연결해 보세요','create_scene.py에서 InteractiveSceneCfg는 바닥·조명·카트폴 구성을 정의합니다. scene.write_data_to_sim()은 지정한 힘을 전달하고, sim.step()은 물리 시간을 진행합니다. scene.update()는 그 결과를 읽을 수 있도록 상태를 갱신합니다.')
step('다음 단계  |  흔들기에서 균형 잡기로','이 예제는 정책을 학습하지 않습니다. 균형 잡기를 학습하려면 관찰값(막대 각도 등), 행동(카트에 줄 힘), 보상(균형을 유지했는지)을 갖춘 과제를 사용합니다.')
link('이어서 읽기  /  보상과 종료 조건이 있는 카트폴 환경  ↗',L+'tutorials/03_envs/create_manager_rl_env.html')
end();c.save()

