from pathlib import Path
import re
import html
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from PIL import Image

root=Path.cwd()
src=root/'Isaac-Sim-6.2-Unity-Guide-KO.md'
lines=src.read_text(encoding='utf-8').splitlines()
# Add the delimiter row required by Markdown tables.
out=[]
for i,line in enumerate(lines):
    out.append(line)
    if line.startswith('|') and not lines[i-1].startswith('|') and not lines[i+1].startswith('|---'):
        out.append('|'+'---|'*(line.count('|')-1))
src.write_text('\n'.join(out)+'\n',encoding='utf-8')
title=lines[0][2:]
intro=lines[2]
sections=re.split(r'^## ', '\n'.join(lines),flags=re.M)[1:]
for name,file in [('K','malgun.ttf'),('KB','malgunbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
import sys
pdf=root/(sys.argv[1] if len(sys.argv)>1 else 'Isaac-Sim-6.2-Unity-Guide-KO.pdf')
c=canvas.Canvas(str(pdf),pagesize=(595,842))
c.setTitle(title)
c.setAuthor('Isaac Sim 프로젝트')
def col(s):return HexColor(s)
width=507
def txt(x,y,s,size=10,font='K',ink='#192e34'):
    c.setFont(font,size);c.setFillColor(col(ink));c.drawString(x,y,s)
def para(s,size=11,font='K',leading=18,w=width,ink='#23383d'):
    return Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=col(ink),wordWrap='CJK'))
def flow(p,y,gap=8):
    _,h=p.wrap(width,1000)
    p.drawOn(c,44,y-h)
    return y-h-gap
def rich(s):
    return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2" color="#006e69"><u>\1</u></a>',html.escape(s))
def footer(n):
    txt(44,29,'ISAAC SIM 6.2.0   /   UNITY 개발자 가이드',8,ink='#567273')
    txt(520,29,f'{n:02d} / 18',8,ink='#567273')
c.bookmarkPage('contents');c.addOutlineEntry('목차','contents')
txt(44,778,'ROBOTICS    /    개발 가이드',11,'KB','#00786e')
txt(44,706,'Unity 개발자를 위한',26,'KB')
txt(44,661,'Isaac Sim 6.2.0 실무 가이드',30,'KB')
flow(para(intro),622)
txt(44,515,'목차',15,'KB')
for i,section in enumerate(sections):
    name=section.split('\n',1)[0]
    x=44+(i//9)*264;y=476-(i%9)*40
    txt(x,y,name[:2],10,'KB','#00786e')
    item=para(html.escape(name[3:]),10,'K',14,226)
    _,h=item.wrap(223,100);item.drawOn(c,x+24,y+9-h)
    c.linkRect('',f's{i}',(x,y-21,x+242,y+14),relative=0,thickness=0)
footer(1);c.showPage()
for idx,section in enumerate(sections):
    name,body=section.split('\n',1)
    c.bookmarkPage(f's{idx}');c.addOutlineEntry(name,f's{idx}')
    txt(44,789,'ISAAC SIM 6.2.0     /     '+name[:2],10,'KB','#00786e')
    txt(500,789,'목차로 이동',9,ink='#006e69');c.linkRect('','contents',(497,785,552,801),thickness=0)
    y=flow(para(html.escape(name[3:]),23,'KB',30),763,18)
    rows=body.splitlines();j=0
    while j<len(rows):
        line=rows[j];j+=1
        if not line.strip():continue
        if line.startswith('### '):
            y=flow(para(rich(line[4:]),13,'KB',20),y-5,5)
        elif line.startswith('|'):
            group=[line]
            while j<len(rows) and rows[j].startswith('|'):
                group.append(rows[j]);j+=1
            data=[]
            for k,line in enumerate(group):
                if line.startswith('|---'):continue
                data.append([para(rich(v.strip()),9.4,'KB' if k==0 else 'K',14,100,'#ffffff' if k==0 else '#21383b') for v in line.strip('|').split('|')])
            tab=Table(data,colWidths=[125,178,width-303])
            tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),col('#236561')),('ROWBACKGROUNDS',(0,1),(-1,-1),[col('#edf4f2'),col('#f8faf9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            y=flow(tab,y,10)
        elif line.startswith('!['):
            im=Image.open(root/'.guide-assets/move_cube.webp');im.seek(574)
            w=315;h=w*im.height/im.width
            c.drawImage(ImageReader(im.convert('RGB')),44,y-h,w,h)
            p=para('NVIDIA 기본 실습 화면<br/><br/>중앙의 큐브를 선택하면 오른쪽 Stage와 Property에서 같은 물체의 경로와 속성을 확인할 수 있습니다.',9,'K',15,163)
            _,hh=p.wrap(163,500);p.drawOn(c,375,y-hh);y-=h+10
        elif line.startswith('```'):
            code=[]
            while j<len(rows) and not rows[j].startswith('```'):
                code.append(rows[j]);j+=1
            j+=1;h=12*len(code)+16
            c.setFillColor(col('#edf4f2'));c.rect(44,y-h,width,h,fill=1,stroke=0)
            for n,l in enumerate(code):txt(52,y-15-n*12,l,9,'Courier')
            y-=h+9
        else:
            small=line.startswith('공식 자료')
            compact = name.startswith('04 ')
            size = 9 if small else (10 if compact else 10.7)
            leading = 14 if small else (15 if compact else 17.5)
            y=flow(para(rich(line),size,'K',leading),y,4 if compact else 7)
    if y<42:raise Exception(f'Page overflow {name}: {y}')
    footer(idx+2);c.showPage()
c.save()
