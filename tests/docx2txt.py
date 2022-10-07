from docx import Document

document = Document('F:\\VReality\\BurgerWeek\\BW_SC_6ta\\Menús BWSC6 en formato WEB-20221006T194836Z-001\\Menús BWSC6 en formato WEB\\7. Boulevardier.docx')
str = ""
for para in document.paragraphs:
    text_line = para.text.strip()
    if text_line == "*** Si no tiene opción 3 puede dejar en blanco los espacios":
        continue
    if text_line == "*** Separar direcciones/teléfonos/horarios distintos con saltos de línea":
        continue
    if text_line != "":
    	str+=text_line
print(str)
