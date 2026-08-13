filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    ('Download Scout Pass (PDF)', 'Download Scout Record (PDF)'),
    ('Download Scout Pass PDF', 'Download Scout Record (PDF)'),
    ('Scout Pass PDF downloaded successfully!', 'Scout Record PDF downloaded successfully!'),
    ('Preparing Scout Pass PDF...', 'Preparing Scout Record PDF...'),
    ('official Scout Pass PDF', 'official Scout Record PDF'),
    ('downloadRegisterScoutPassPdf', 'downloadRegisterScoutRecordPdf'),
    ('_Scout_Pass_SinglePage.pdf', '_Scout_Record_SinglePage.pdf')
]

for old, new in replacements:
    html = html.replace(old, new)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated "Scout Pass" -> "Scout Record" in mobile/register/index.html!')
