import sys, re, glob, os

folder = sys.argv[1] if len(sys.argv) > 1 else os.path.join('templates', 'admin')
MARK = 'viewIdBtn'

TH_OLD = '<th>Requirement</th>'
TH_NEW = TH_OLD + '\n                        <th>Valid ID</th>'

TD_OLD = '<td><span class="status-badge">Pending</span></td>'
TD_NEW = '''<td>
                            {% if event.valid_id_path %}
                                <button class="btn-file btn-id" data-id-name="{{ event.valid_id_path|e }}">
                                    <i class="fas fa-id-card"></i> View ID
                                </button>
                            {% else %}
                                <span class="no-file">No ID</span>
                            {% endif %}
                        </td>
                        ''' + TD_OLD

MODAL_OLD = '<div class="remarks-box">'
MODAL_NEW = '''<div class="file-preview-section" id="validIdSection" style="display:none;">
                <h4><i class="fas fa-id-card"></i> Valid ID of Applicant</h4>
                <button class="btn-view-file-inline" id="viewIdBtn">
                    <i class="fas fa-id-card"></i> View Valid ID
                </button>
            </div>

            ''' + MODAL_OLD

SCRIPT = '''
<script>
// ===== VIEW VALID ID (admin only, signed URL) =====
(function () {
    var DATA = [];
    try { DATA = JSON.parse(document.getElementById('events-data').textContent); } catch (e) {}
    var currentIdName = null;

    function showIdViewer(name) {
        var modal = document.getElementById('fileViewerModal');
        var preview = document.getElementById('filePreviewContainer');
        modal.classList.add('active');
        preview.innerHTML = '<p>Loading ID...</p>';
        fetch('/api/file-url/' + encodeURIComponent(name), { credentials: 'same-origin' })
            .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
            .then(function (j) {
                var url = j.url || j.signed_url || j.file_url;
                if (!url) throw new Error('no url in response');
                var ext = name.split('?')[0].split('.').pop().toLowerCase();
                if (ext === 'pdf') {
                    preview.innerHTML = '<iframe src="' + url + '"></iframe><br><a href="' + url + '" target="_blank" rel="noopener" class="download-btn"><i class="fas fa-download"></i> Open PDF</a>';
                } else {
                    preview.innerHTML = '<img src="' + url + '" alt="Valid ID"><br><a href="' + url + '" target="_blank" rel="noopener" class="download-btn"><i class="fas fa-external-link-alt"></i> Open in New Tab</a>';
                }
            })
            .catch(function (err) {
                console.error('View ID error:', err);
                preview.innerHTML = '<p>Hindi ma-load ang ID.</p>';
            });
    }

    document.querySelectorAll('.btn-id').forEach(function (btn) {
        btn.addEventListener('click', function () {
            showIdViewer(this.getAttribute('data-id-name'));
        });
    });

    document.querySelectorAll('.btn-review').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var id = parseInt(this.getAttribute('data-event-id'));
            var ev = DATA.find(function (e) { return e.id === id; });
            var sec = document.getElementById('validIdSection');
            var old = document.getElementById('viewIdBtn');
            if (!sec || !old) return;
            var nb = old.cloneNode(true);
            old.parentNode.replaceChild(nb, old);
            if (ev && ev.valid_id_path) {
                currentIdName = ev.valid_id_path;
                sec.style.display = 'block';
                nb.addEventListener('click', function () { showIdViewer(currentIdName); });
            } else {
                currentIdName = null;
                sec.style.display = 'none';
            }
        });
    });
})();
</script>
'''

DATA_RE = re.compile(r'(\{\{\s*pending_events\s*\|\s*tojson\s*\|\s*safe\s*\}\}\s*</script>)')

def process(path):
    with open(path, 'r', encoding='utf-8', newline='') as f:
        s = f.read()
    crlf = '\r\n' in s
    s = s.replace('\r\n', '\n')
    if MARK in s:
        return 'SKIP (may na)'
    for old in (TH_OLD, TD_OLD, MODAL_OLD):
        if s.count(old) != 1:
            return 'HINDI GINALAW (anchor: %r, nahanap %d)' % (old, s.count(old))
    if len(DATA_RE.findall(s)) != 1:
        return 'HINDI GINALAW (hindi nahanap ang events-data script)'
    s = s.replace(TH_OLD, TH_NEW).replace(TD_OLD, TD_NEW).replace(MODAL_OLD, MODAL_NEW)
    s = DATA_RE.sub(lambda m: m.group(1) + '\n' + SCRIPT, s, count=1)
    if crlf:
        s = s.replace('\n', '\r\n')
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    return 'OK'

files = sorted(glob.glob(os.path.join(folder, 'admin_court*_pending.html')))
if not files:
    print('Walang nahanap na file sa', folder)
for p in files:
    print(os.path.basename(p) + ':', process(p))
