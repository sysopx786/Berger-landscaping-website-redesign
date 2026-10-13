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

# ---- page 2: what's in the kit ----
from reportlab.platypus import Frame, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
LW,LH=letter
st=lambda **k: ParagraphStyle("x",fontName=k.get("f","Helvetica"),fontSize=k.get("s",10),leading=k.get("l",14),textColor=k.get("c",SPRUCE),spaceAfter=k.get("a",4))
H1,H2,B,SM=st(f="Helvetica-Bold",s=20,l=24,a=6),st(f="Helvetica-Bold",s=12,l=16,c=MOSS,a=3),st(),st(s=8.5,l=11.5,c=PINE)
def bl(items): return [Paragraph("&bull;&nbsp; "+t,B) for t in items]
LINK='<font color="#3E6A30">search.google.com/local/writereview?placeid=ChIJr_SAVzWdPI8RdY2P9Uzbv8w</font>'
story=[Paragraph("Your Google review kit",H1),
 Paragraph("Prepared for Drew Berger, Berger Landscaping LLC. Google counts your reviews when it decides who shows up in Maps searches around Pottstown. Everything below points customers to the same place: your Google review box, one tap away.",B),Spacer(1,8),
 Paragraph("1. On your new website",H2)]+bl([
 "<b>Leave a review</b> button on the Home page and the Reviews page. It opens your Google review box directly; no searching for your listing.",
 "Your Google reviews (5.0, 5 reviews) shown on the Home and Reviews pages, with your replies, so new customers see them right away.",
 "The site is in preview now. The button goes live on bergerlandscaping.net at launch; the cards and texts below work today."])+[Spacer(1,6),
 Paragraph("2. Review cards (page 1 of this file)",H2)]+bl([
 "10 business-card-size cards per sheet. Print on card stock and cut along the marks.",
 "Hand one over with every invoice, or leave one at the door after the job. Customers scan the QR code with their phone camera.",
 "A single-card file is included for a print shop, plus the QR code alone for invoices or a truck magnet."])+[Spacer(1,6),
 Paragraph("3. After-job text messages",H2),
 Paragraph("<b>Same day as the job:</b> &ldquo;Hi [Name], this is Drew from Berger Landscaping. Thanks for having us out today! If you have a minute, a Google review really helps a small local business like mine: [link] Thanks again, and call or text anytime.&rdquo;",B),
 Paragraph("<b>Recurring customer:</b> &ldquo;Hi [Name], Drew from Berger Landscaping here. Thanks for sticking with us this season! If you&rsquo;ve got a minute, would you leave us a quick Google review? It makes a big difference for a small business: [link]&rdquo;",B),
 Paragraph("<b>Your review link:</b> "+LINK,B),Spacer(1,6),
 Paragraph("4. A few rules that keep reviews working",H2)]+bl([
 "<b>Ask every customer</b>, not only the happy ones. Google does not allow asking only customers you expect to be positive.",
 "<b>No discounts or freebies for reviews.</b> Google removes incentivized reviews.",
 "<b>Ask the same day</b>, while the job is fresh in the customer's mind.",
 "<b>Reply to every review</b> on Google, good or bad. Customers read the replies."])+[Spacer(1,10),
 Paragraph("Questions or more cards: Mujtaba Valli &middot; mujtaba@barikillc.com",SM)]
c2=canvas.Canvas("marketing/review-cards/_kit_p2.pdf",pagesize=letter)
c2.setFillColor(MOSS); c2.rect(0,LH-0.18*inch,LW,0.18*inch,stroke=0,fill=1)
lw2=1.6*inch; c2.drawImage(LOGO,LW-0.75*inch-lw2,LH-0.45*inch-lw2*443/781,lw2,lw2*443/781,mask='auto')
Frame(0.75*inch,0.6*inch,LW-1.5*inch,LH-1.35*inch-lw2*443/781+0.6*inch,showBoundary=0,leftPadding=0,rightPadding=0).addFromList(story,c2)
c2.showPage(); c2.save()
from pypdf import PdfReader, PdfWriter
w=PdfWriter()
for f in ["marketing/review-cards/berger-review-cards-10up.pdf","marketing/review-cards/_kit_p2.pdf"]:
    for pg in PdfReader(f).pages: w.add_page(pg)
w.add_metadata({"/Title":"Berger Landscaping Google review kit"})
import os; w.write("marketing/review-cards/berger-review-cards-10up.pdf"); os.remove("marketing/review-cards/_kit_p2.pdf")
