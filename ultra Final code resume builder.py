from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib import enums

# ---------------- STYLES ----------------
styleN = ParagraphStyle(
    name="Normal",
    fontName="Helvetica",
    fontSize=10,
    alignment=enums.TA_CENTER,
)

styleWhite = ParagraphStyle(
    name="White",
    fontName="Helvetica-Bold",
    fontSize=10,
    textColor=colors.white,
    alignment=enums.TA_CENTER,
)

TABLE_WIDTH = 515
ROW_PAD = 7


def caps(t):
    return " ".join([w if w.isupper() else w.capitalize() for w in str(t).split()])


def circle_img(c, path, x, y, size):
    try:
        img = ImageReader(path)
        c.saveState()
        p = c.beginPath()
        p.circle(x + size/2, y + size/2, size/2)
        c.clipPath(p, stroke=0, fill=0)
        c.drawImage(img, x, y, size, size)
        c.restoreState()
    except:
        pass


def apply_table_style(table, blue_header=False, grey_header=False):
    style = [
        ("GRID", (0,0), (-1,-1), 1.2, colors.darkblue),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), ROW_PAD),
        ("BOTTOMPADDING", (0,0), (-1,-1), ROW_PAD),
    ]

    if blue_header:
        style += [
            ("SPAN", (0,0), (-1,0)),
            ("BACKGROUND", (0,0), (-1,0), colors.Color(0.06,0.32,0.62)),
        ]

    if grey_header:
        style += [
            ("BACKGROUND", (0,1), (-1,1), colors.lightgrey),
            ("FONTNAME", (0,1), (-1,1), "Helvetica-Bold"),
        ]

    table.setStyle(TableStyle(style))


def create(d):

    c = canvas.Canvas("Resume.pdf")
    page_w, page_h = c._pagesize

    # ---------------- HEADER ----------------
    bar_h = 120
    bar_y = page_h - bar_h
    blue = colors.Color(0.06,0.32,0.62)

    c.setFillColor(blue)
    c.rect(0, bar_y, page_w, bar_h, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(60, bar_y + 70, caps(d["name"]))

    c.setFont("Helvetica", 11)
    c.drawString(60, bar_y + 50, caps(d["address"]))
    c.drawString(60, bar_y + 34, caps(d["course"]))

    right_x = page_w - 330
    c.drawString(right_x, bar_y + 50, "Phone: " + d["phone"])
    c.drawString(right_x, bar_y + 34, "Email: " + d["email"])
    c.drawString(right_x, bar_y + 18, "LinkedIn: " + d["linkedin"])

    if d["img"]:
        circle_img(c, d["img"], page_w - 100, bar_y + 28, 75)

    y = bar_y - 25

    # ---------------- CAREER ----------------
    career = [
        [Paragraph("Career Objective", styleWhite)],
        [Paragraph(caps(d["obj"]), styleN)]
    ]
    t = Table(career, colWidths=[TABLE_WIDTH])
    apply_table_style(t, blue_header=True)
    t.wrapOn(c, 0, 0)
    t.drawOn(c, (page_w - TABLE_WIDTH)/2, y - t._height)
    y -= t._height + 10

    # ---------------- EDUCATION ----------------
    edu_data = [
        [Paragraph("Educational Details", styleWhite)],
        [
            Paragraph("S.No", styleN),
            Paragraph("Qualification", styleN),
            Paragraph("Board/University", styleN),
            Paragraph("Year", styleN),
            Paragraph("%", styleN),
        ]
    ]

    for i, r in enumerate(d["edu"], 1):
        edu_data.append([
            Paragraph(str(i), styleN),
            Paragraph(caps(r[0]), styleN),
            Paragraph(caps(r[1]), styleN),
            Paragraph(r[2], styleN),
            Paragraph(r[3], styleN),
        ])

    edu_table = Table(edu_data,
                      colWidths=[60,150,150,75,80])

    apply_table_style(edu_table, blue_header=True, grey_header=True)
    edu_table.wrapOn(c, 0, 0)
    edu_table.drawOn(c, (page_w - TABLE_WIDTH)/2, y - edu_table._height)
    y -= edu_table._height + 10

    # ---------------- PROFESSIONAL ----------------
    prof_data = [
        [Paragraph("Professional Details", styleWhite)],
        [Paragraph("Certifications", styleN), Paragraph(d["cert"], styleN)],
        [Paragraph("Skills", styleN), Paragraph(d["skills"], styleN)],
        [Paragraph("Projects", styleN), Paragraph(d["projects"], styleN)],
    ]

    prof_table = Table(prof_data,
                       colWidths=[TABLE_WIDTH/2, TABLE_WIDTH/2])

    apply_table_style(prof_table, blue_header=True)
    prof_table.wrapOn(c, 0, 0)
    prof_table.drawOn(c, (page_w - TABLE_WIDTH)/2, y - prof_table._height)
    y -= prof_table._height + 10

    # ---------------- PERSONAL ----------------
    personal_data = [
        [Paragraph("Personal Details", styleWhite)],
        [Paragraph("Father Name", styleN), Paragraph(caps(d["father"]), styleN)],
        [Paragraph("DOB", styleN), Paragraph(d["dob"], styleN)],
        [Paragraph("Languages", styleN), Paragraph(caps(d["lang"]), styleN)],
        [Paragraph("Gender", styleN), Paragraph(caps(d["gender"]), styleN)],
        [Paragraph("Nationality", styleN), Paragraph(caps(d["nation"]), styleN)],
        [Paragraph("Marital Status", styleN), Paragraph(caps(d["marital"]), styleN)],
    ]

    personal_table = Table(personal_data,
                           colWidths=[TABLE_WIDTH/2, TABLE_WIDTH/2])

    apply_table_style(personal_table, blue_header=True)
    personal_table.wrapOn(c, 0, 0)
    personal_table.drawOn(c, (page_w - TABLE_WIDTH)/2, y - personal_table._height)

    # ---------------- DECLARATION ----------------
    c.setFillColor(colors.black)

    decl_y = 150
    c.drawString(60, decl_y,
        "Declaration: I hereby declare that the above information is true and correct to the best of my knowledge.")

    # ---------------- DATE / PLACE ----------------
    c.drawString(60, 60, "Date: " + d["date"])
    c.drawString(60, 45, "Place: " + d["place"])

    # ---------------- SIGNATURE ----------------
    c.line(page_w - 220, 65, page_w - 60, 65)
    c.drawString(page_w - 200, 50, caps(d["name"]))

    c.save()
    print("PDF READY -> Resume.pdf")


# ---------------- INPUT ----------------
def get_edu():
    n = int(input("Education Records: "))
    rows = []
    for i in range(n):
        rows.append((
            input("Qualification: "),
            input("Board: "),
            input("Year: "),
            input("Percent/CGPA: ")
        ))
    return rows


if __name__ == "__main__":

    d = {}
    d["name"] = input("Name: ")
    d["address"] = input("Address: ")
    d["course"] = input("Course: ")

    d["phone"] = input("Phone: ")
    d["email"] = input("Email: ")
    d["linkedin"] = input("LinkedIn: ")

    d["obj"] = input("Career Objective: ")
    d["edu"] = get_edu()

    d["cert"] = input("Certifications: ")
    d["skills"] = input("Skills: ")
    d["projects"] = input("Projects: ")

    d["father"] = input("Father Name: ")
    d["dob"] = input("DOB: ")
    d["lang"] = input("Languages: ")
    d["gender"] = input("Gender: ")
    d["nation"] = input("Nationality: ")
    d["marital"] = input("Marital Status: ")

    d["date"] = input("Date: ")
    d["place"] = input("Place: ")

    d["img"] = input("Image Path (or blank): ")

    create(d)
