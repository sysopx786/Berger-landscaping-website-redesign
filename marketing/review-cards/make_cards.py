import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
URL="https://search.google.com/local/writereview?placeid=ChIJr_SAVzWdPI8RdY2P9Uzbv8w"
SPRUCE,MOSS,PINE=HexColor("#2B3A42"),HexColor("#3E6A30"),HexColor("#5F6F73")
q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=0,box_size=20); q.add_data(URL); q.make(fit=True)
q.make_image(fill_color="#2B3A42",back_color="white").save("marketing/review-cards/berger-review-qr.png")
QR=ImageReader("marketing/review-cards/berger-review-qr.png"); LOGO=ImageReader("docs/assets/logo-horizontal.png")
W,H=3.5*inch,2*inch
def card(c,x,y):
    c.setFillColor(HexColor("#FFFFFF")); c.rect(x,y,W,H,stroke=0,fill=1)
    c.setFillColor(MOSS); c.rect(x,y,W,0.07*inch,stroke=0,fill=1)
    lw=1.25*inch; c.drawImage(LOGO,x+0.18*inch,y+H-0.18*inch-lw*443/781,lw,lw*443/781,mask='auto')
    qs=1.25*inch; qx=x+W-0.2*inch-qs; qy=y+0.33*inch
    c.drawImage(QR,qx,qy,qs,qs)
    c.setFillColor(PINE); c.setFont("Helvetica",6.3); c.drawCentredString(qx+qs/2,y+0.17*inch,"Scan with your phone camera")
    c.setFillColor(SPRUCE); c.setFont("Helvetica-Bold",12.5); c.drawString(x+0.2*inch,y+0.86*inch,"How did we do?")
    c.setFont("Helvetica",7.4); c.setFillColor(PINE)
    for i,t in enumerate(["Scan to leave a Google review.","It takes a minute and helps","a local family business."]):
        c.drawString(x+0.2*inch,y+0.68*inch-i*0.12*inch,t)
    c.setFillColor(SPRUCE); c.setFont("Helvetica-Bold",7.4); c.drawString(x+0.2*inch,y+0.17*inch,"Call or text (610) 420-3338")
# 1) single card, trim size
c=canvas.Canvas("marketing/review-cards/berger-review-card.pdf",pagesize=(W,H)); c.setTitle("Berger Landscaping review card"); card(c,0,0); c.showPage(); c.save()
# 2) 10-up letter sheet with crop marks
c=canvas.Canvas("marketing/review-cards/berger-review-cards-10up.pdf",pagesize=letter); c.setTitle("Berger Landscaping review cards (10 per sheet)")
mx,my=0.75*inch,0.5*inch
for r in range(5):
    for k in range(2):
        x,y=mx+k*W,my+r*H; card(c,x,y)
c.setStrokeColor(HexColor("#9AA9AA")); c.setLineWidth(0.3)
for k in range(3):
    X=mx+k*W; c.line(X,my-0.35*inch,X,my-0.1*inch); c.line(X,my+5*H+0.1*inch,X,my+5*H+0.35*inch)
for r in range(6):
    Y=my+r*H; c.line(mx-0.35*inch,Y,mx-0.1*inch,Y); c.line(mx+2*W+0.1*inch,Y,mx+2*W+0.35*inch,Y)
c.showPage(); c.save()
