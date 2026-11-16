from pathlib import Path
from html import escape
import json,re,math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image
from reportlab.lib.utils import ImageReader

d=Path(__file__).parent
sources=json.loads((d/'practicum-sources.json').read_text('utf8'))|json.loads((d/'research-links.txt').read_text('utf8'))
for name,file in [('Ko','malgun'),('Bold','malgunbd')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file+'.ttf'))
def paragraph(s,size=11.3,leading=18.6,font='Ko',ink='#21383d'):
    return Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=HexColor(ink),wordWrap='CJK'))
def put(obj,x,y,w):
    _,h=obj.wrap(w,2000);obj.drawOn(c,x,y-h)
    return y-h
def label(x,y,s,size=10,font='Ko',ink='#1b3a3f'):
    c.setFont(font,size);c.setFillColor(HexColor(ink));c.drawString(x,y,s)
def linesrc(line):
    pairs=[v.split(' ',1) for v in line[1:].split('|')]
    return '자료　'+'　·　'.join(f'<a color="#077067" href="{sources[k]}"><u>{escape(v)}</u></a>' for k,v in pairs)
def footer(page):
    label(42,26,book,8,ink='#497570');label(509,26,f'{page:02d} / {total:02d}',9)
def pagehead(n,title,key):
    c.bookmarkPage(key);c.addOutlineEntry(title,key)
    label(42,795,series+'    /    '+n,10,'Bold','#00776b')
    label(510,795,'목차 이동',9,ink='#00776b');c.linkRect('','start',(507,791,552,805),thickness=0)
    return put(paragraph(escape(title),22,30,'Bold'),42,767,511)-17
for glossary,src,filename,book in [(False,'pipeline-draft','Quadruped-Development-Pipeline-KO','4족 순찰 로봇 개발 파이프라인'),(True,'lexicon-draft','Robotics-Isaac-Glossary-KO','로봇 개발 용어집')]:
    body=(d/(src+'.txt')).read_text('utf8')
    sections=[x.strip().splitlines() for x in re.split('^## ',body,flags=re.M)[1:]]
    index=[]
    if glossary:
        for j,sec in enumerate(sections):
            for row in sec[1:]:
                if row.startswith('@') or '|' not in row:continue
                for term in row.split('|',1)[0].split(' / '):
                    index.append((term.split('(')[0].strip(),j))
        index=sorted(set(index),key=lambda r:r[0].lower())
    indexpages=math.ceil(len(index)/80)
    total=len(sections)+1+indexpages
    series='용어와 쓰임' if glossary else '입문 실습'
    c=canvas.Canvas(filename+'.pdf',pagesize=(595,842))
    c.setTitle(book);c.setAuthor('Isaac 프로젝트')
    c.bookmarkPage('start');c.addOutlineEntry('목차','start')
    label(42,773,'ISAAC SIM 6.2.0    /    ISAAC LAB 3.0.0',12,'Bold','#00776b')
    label(42,713,book,28,'Bold')
    intro=('용어를 영문 원어, 한글 발음, 현장에서의 의미로 정리했습니다. 같은 문단에 묶인 용어는 서로 비교해 읽으세요. 뒤쪽 영문 색인에서 항목을 누르면 해당 주제로 이동합니다.' if glossary else '공장 순찰 임무를 한 단계씩 완성합니다. 장면 파일부터 정책·센서 로그까지, 다음 담당자에게 무엇을 넘기고 어디까지 검증해야 하는지 따라가 보세요.')
    put(paragraph(intro),42,674,510);label(42,567,'목차',15,'Bold')
    for j,sec in enumerate(sections):
        y=531-j*26;label(42,y,f'{j+1:02d}',10,'Bold','#00776b');label(73,y,sec[0],11)
        label(514,y,str(j+2),10);c.linkRect('',f'g{j}',(40,y-5,550,y+13),thickness=0)
    if glossary:
        y-=30;label(73,y,'영문 찾아보기',11,'Bold');c.linkRect('','idx0',(65,y-4,550,y+12),thickness=0)
    put(paragraph('자료 확인일 2026년 11월 11일. 제품 기능은 버전 고정 공식 문서, 적용 사례는 NVIDIA 개발자 블로그, 일반 개념은 위키와 교육 자료를 참고했습니다. 각 장의 자료명을 누르면 원문을 열 수 있습니다.',9.7,15),42,128,510)
    footer(1);c.showPage()
    for j,sec in enumerate(sections):
        y=pagehead(f'{j+1:02d}',sec[0],f'g{j}')
        for row in sec[1:]:
            if not row:continue
            if row.startswith('@'):
                y=put(paragraph(linesrc(row),9.2,15),42,y-4,511)-4
            elif glossary:
                term,desc=row.split('|',1)
                y=put(paragraph(escape(term),10.5,14.6,'Bold','#00695f'),42,y,510)-1
                y=put(paragraph(escape(desc),10.2,15),42,y,511)-7
            elif row.startswith('### '):
                y=put(paragraph(escape(row[4:]),13.2,19,'Bold','#00695f'),42,y-5,510)-4
            elif row.startswith('>'):
                cmd=row[1:];ls=[]
                while len(cmd)>89:
                    cut=cmd.rfind(' ',0,88);ls.append(cmd[:cut]+' '+chr(96));cmd='  '+cmd[cut+1:]
                ls.append(cmd);h=13*len(ls)+9;c.setFillColor(HexColor('#edf3f2'));c.rect(42,y-h,511,h,fill=1,stroke=0)
                for k,s in enumerate(ls):label(49,y-13-13*k,s,9,'Courier')
                y-=h+3
            else:y=put(paragraph(escape(row)),42,y,511)-9
        if not glossary and j in (2,3,5,6,7) and y>178:
            pattern,cap,source={2:('edit-*move_cube.webp','Sim 기본 장면과 Stage 트리','edit'),3:('urdf-*gui_0.png','URDF 파일 선택과 가져오기 설정','urdf'),5:('lab-*.jpg','Lab의 병렬 장면 생성 예시','lab'),6:('anymal.jpg','ANYmal-D 평지 환경','anymal'),7:('rviz-official.png','RViz 기본 화면과 Fixed Frame 설정','rviz')}[j]
            pic=Image.open(next((d/'practicum').glob(pattern)));w,h=pic.size
            scale=min((y-73)/h,445/w,155/h);w*=scale;h*=scale
            c.drawImage(ImageReader(pic.convert('RGB')),42,y-h,w,h);label(42,y-h-14,'공식 예제 화면  /  '+cap,8.5);c.linkURL(sources[source],(42,y-h-16,42+w,y),thickness=0)
        if y<43:raise ValueError((book,j,y))
        footer(j+2);c.showPage()
    for n in range(indexpages):
        y=pagehead(f'{n+1} / {indexpages}','영문 찾아보기',f'idx{n}')
        for i,(s,j) in enumerate(index[80*n:80*(n+1)]):
            x=42+257*(i//40);yy=y-16.3*(i%40)
            label(x,yy,s,9.2);label(x+215,yy,str(j+2),9,ink='#00776b');c.linkRect('',f'g{j}',(x,yy-3,x+235,yy+10),thickness=0)
        footer(len(sections)+2+n);c.showPage()
    c.save();print(filename,total,len(index))
