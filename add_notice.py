import re, sys

BANNER = ('<div class="student-demo-notice" style="background:#fef3c7;border:1px solid #f59e0b;'
          'color:#92400e;padding:12px 16px;border-radius:10px;margin:0 0 18px;font-size:14px;line-height:1.5;">'
          '<strong>Student project demo.</strong> Please do not upload real IDs or personal documents. '
          'Use sample or dummy files only.</div>')

TARGETS = {
    r'templates\apply_permit.html': r'<form id="permitForm"[^>]*>',
    r'templates\request_document.html': r'<form id="clearanceForm"[^>]*>',
}

for path, pat in TARGETS.items():
    with open(path, 'r', encoding='utf-8', newline='') as f:
        s = f.read()
    if 'student-demo-notice' in s:
        print(path, ': SKIP (may na)'); continue
    m = list(re.finditer(pat, s))
    if len(m) != 1:
        print(path, ': HINDI GINALAW (nahanap', len(m), ')'); continue
    nl = '\r\n' if '\r\n' in s else '\n'
    end = m[0].end()
    s = s[:end] + nl + '    ' + BANNER + s[end:]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    print(path, ': OK')
