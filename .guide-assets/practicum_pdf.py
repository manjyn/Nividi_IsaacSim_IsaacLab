from pathlib import Path
import re, json, html
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

d=Path(__file__).parent
refs=json.loads((d/'practicum-sources.json').read_text(encoding='utf8'))
sections=[s.splitlines() for s in re.split('^## ',(d/'practicum-content.txt').read_text(encoding='utf8'),flags=re.M)[1:]]
out='Isaac-Sim-6.2-Lab-3.0-Field-Guide-KO'
for f,p in [('K','malgun'),('B','malgunbd')]:
    pdfmetrics.registerFont(TTFont(f,'C:/Windows/Fonts/'+p+'.ttf'))
c=canvas.Canvas(out+'.pdf',pagesize=(595,842))
title='4족 로봇 시뮬레이션 실무 가이드'
c.setTitle(title)
color=HexColor
md=['# '+title,'','Isaac Sim 6.2.0 · Isaac Lab 3.0.0 · Windows PowerShell 및 ROS 2','']
def txt(x,y,s,size=10,font='K',ink='#243b42'):
    c.setFont(font,size);c.setFillColor(color(ink));c.drawString(x,y,s)
def pp(s,size=10.8,leading=17.4,font='K',ink='#20363c'):
    return Paragraph(s,ParagraphStyle('text',fontName=font,fontSize=size,leading=leading,textColor=color(ink),wordWrap='CJK'))
def draw(obj,top,gap=9):
    _,h=obj.wrap(507,1000);obj.drawOn(c,44,top-h);return top-h-gap
def footer(n):
    txt(44,26,'ISAAC SIM 6.2.0   /   ISAAC LAB 3.0.0',8,'B','#587574')
    txt(514,26,f'{n:02d} / {len(sections)+1:02d}',9)
def bookmark(n,label):
    c.bookmarkPage(n);c.addOutlineEntry(label,n)
bookmark('contents','목차')
txt(44,777,'현장 실습  /  Unity 개발자를 위한 후속편',12,'B','#007469')
txt(44,716,title,29,'B')
txt(44,681,'Isaac Sim 6.2.0    ·    Isaac Lab 3.0.0    ·    ROS 2',14)
draw(pp('로봇 모델을 인수한 날부터 관절과 센서를 검증하고 보행 시험 결과를 동료에게 넘길 때까지. 공식 예제에는 실행 명령과 확인 지점을, 팀별 설정에는 기록할 값과 실패 판별법을 붙였습니다.'),648)
txt(44,555,'실습 순서',15,'B')
for n,sec in enumerate(sections):
    y=522-n*30
    txt(44,y,f'{n+1:02d}',10,'B','#007469');txt(78,y,sec[0],11)
    c.linkRect('',f'p{n}',(42,y-5,552,y+13),thickness=0)
draw(pp('화면 자료는 NVIDIA·Isaac Lab·ROS 2 공식 문서 및 저장소에서 발췌했습니다. 공식 문서가 재사용한 이전 버전의 화면은 메뉴 위치가 다를 수 있습니다. 메뉴 경로는 본문의 6.2 표기를 기준으로 보세요.',9.3,15),130)
footer(1);c.showPage()
for n,sec in enumerate(sections):
    bookmark(f'p{n}',sec[0]);txt(44,796,f'실무 실습    /    {n+1:02d}',10,'B','#007469')
    txt(504,796,'목차 이동',9,'K','#007469');c.linkRect('','contents',(501,792,554,810),thickness=0)
    top=draw(pp(sec[0],21.7,28,'B'),768,16)
    md+=['## '+f'{n+1:02d} '+sec[0],'']
    i=1
    while i<len(sec):
        line=sec[i];i+=1
        if not line.strip():continue
        if line.startswith('!'):
            pattern,caption,ref=line[1:].split('|')
            pic=next((d/'practicum').glob(pattern));im=Image.open(pic)
            if getattr(im,'is_animated',False):im.seek(min(im.n_frames-1,574))
            ratio=min(507/im.width,200/im.height);w,h=im.width*ratio,im.height*ratio
            c.drawImage(ImageReader(im.convert('RGB')),44+(507-w)/2,top-h,w,h)
            c.linkURL(refs[ref],(44,top-h,551,top),thickness=0)
            top=draw(pp(html.escape(caption),9,13,'K','#476866'),top-h-6,10)
            md+=['!['+caption+'](.guide-assets/practicum/'+pic.name+')','',caption+' [화면 출처]('+refs[ref]+')','']
        elif line.startswith('@'):
            items=[v.split(' ',1) for v in line[1:].split(' |')]
            rich='공식 자료　'+'　·　'.join(f'<a href="{refs[k]}" color="#006e64"><u>{s}</u></a>' for k,s in items)
            top=draw(pp(rich,9,14),top-3)
            md+=['공식 자료　'+' · '.join(f'[{s}]({refs[k]})' for k,s in items),'']
        elif line.startswith('|'):
            rows=[line]
            while i<len(sec) and sec[i].startswith('|'):rows.append(sec[i]);i+=1
            cells=[[pp(html.escape(v),9.5,14,'B' if j==0 else 'K','#ffffff' if j==0 else '#23393b') for v in row[1:].split('|')] for j,row in enumerate(rows)]
            t=Table(cells,colWidths=[113,191,203]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),color('#19685f')),('ROWBACKGROUNDS',(0,1),(-1,-1),[color('#eef5f3'),color('#f7f9f8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            top=draw(t,top);md+=[rows[0]+'|','|---|---|---|']+[r+'|' for r in rows[1:]]+['']
        elif line.startswith('```'):
            code=[]
            while not sec[i].startswith('```'):code.append(sec[i]);i+=1
            i+=1;md+=['```']+code+['```','']
            wrapped=[]
            for cmd in code:
                while len(cmd)>91:
                    cut=cmd.rfind(' ',0,90);wrapped.append(cmd[:cut]+' '+chr(96));cmd='  '+cmd[cut+1:]
                wrapped.append(cmd)
            h=13*len(wrapped)+14;c.setFillColor(color('#edf4f2'));c.rect(44,top-h,507,h,fill=1,stroke=0)
            for j,s in enumerate(wrapped):txt(51,top-14-j*13,s,8.9,'Courier')
            top-=h+9
        elif line.startswith('### '):
            top=draw(pp(html.escape(line[4:]),12.5,19,'B'),top-3,5);md+=[line,'']
        else:
            top=draw(pp(html.escape(line)),top,8);md+=[line,'']
    if top<40:raise ValueError(f'Overflow page {n+2}: {top}')
    footer(n+2);c.showPage()
c.save()
Path(out+'.md').write_text('\n'.join(md),encoding='utf8')
