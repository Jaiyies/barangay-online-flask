param([string]$Base = 'http://127.0.0.1:5000')
$Base = $Base.TrimEnd('/')
$script:fail = 0

function Result($ok, $msg) {
  if ($ok) { Write-Host "[PASS] $msg" -ForegroundColor Green }
  else { Write-Host "[FAIL] $msg" -ForegroundColor Red; $script:fail++ }
}

function Get-Page($path, $method = 'GET', $body = $null) {
  $o = [pscustomobject]@{ Code = 0; Headers = $null; Body = '' }
  try {
    if ($method -eq 'POST') {
      $r = Invoke-WebRequest ($Base + $path) -Method Post -Body $body -UseBasicParsing -MaximumRedirection 0 -ErrorAction Stop
    } else {
      $r = Invoke-WebRequest ($Base + $path) -UseBasicParsing -MaximumRedirection 0 -ErrorAction Stop
    }
    $o.Code = [int]$r.StatusCode; $o.Headers = $r.Headers; $o.Body = [string]$r.Content
  } catch {
    $resp = $_.Exception.Response
    if ($resp) {
      $o.Code = [int]$resp.StatusCode; $o.Headers = $resp.Headers
      try { $sr = New-Object IO.StreamReader($resp.GetResponseStream()); $o.Body = $sr.ReadToEnd() } catch {}
    }
  }
  return $o
}

Write-Host "`n=== LIVE TESTS: $Base ===" -ForegroundColor Cyan

$r = Get-Page '/robots.txt'
Result ($r.Code -eq 200 -and $r.Body -match 'Disallow:\s*/') '/robots.txt = 200 at may Disallow: /'

foreach ($p in '/login', '/register', '/forgot-password') {
  $r = Get-Page $p
  Result ($r.Code -eq 200) "$p = 200 (nakuha: $($r.Code))"
  Result (([string]$r.Headers['X-Robots-Tag']) -match 'noindex') "$p may X-Robots-Tag noindex"
  Result ($r.Body -notmatch 'action="https?://') "$p walang form na nagpapadala sa ibang site"
  Result ($r.Body -notmatch 'gov\.ph|DILG|Republic of') "$p walang gov.ph/DILG/Republic of"
  if ($p -ne '/forgot-password') {
    Result ($r.Body -match '(?i)student project') "$p may 'Student Project'"
  }
}

$r = Get-Page '/forgot-password' 'POST' @{ email = 'nobody-test@example.com' }
Result ($r.Code -gt 0 -and $r.Code -lt 500) "POST /forgot-password walang server error (code: $($r.Code))"

foreach ($p in '/uploads/test.jpg', '/api/file-url/test.jpg', '/admins', '/dashboard') {
  $r = Get-Page $p
  Result ($r.Code -in 301, 302, 303, 307, 401, 403) "$p protektado kapag hindi naka-login (code: $($r.Code))"
}

if (Test-Path .\app.py) {
  Write-Host "`n=== REPO CHECKS ===" -ForegroundColor Cyan
  python -m py_compile app.py
  Result ($LASTEXITCODE -eq 0) 'app.py nag-compile'
  $tracked = git ls-files
  Result (-not ($tracked -match '(^|/)\.env$')) '.env hindi naka-track sa git'
  Result ((Test-Path requirements.txt) -and (Select-String -Path requirements.txt -Pattern 'gunicorn' -Quiet)) 'gunicorn nasa requirements.txt'
  $ext = Get-ChildItem templates -Recurse -Filter *.html | Select-String -Pattern 'action="https?://'
  Result (-not $ext) 'walang external form action sa templates'
  $gov = Get-ChildItem templates -Recurse -Filter *.html | Select-String -Pattern 'gov\.ph|DILG|Republic of'
  Result (-not $gov) 'walang gov.ph/DILG/Republic of sa templates'
  $n = (Get-ChildItem templates -Recurse -Filter *.html | Select-String -Pattern 'student-demo-notice' | Measure-Object).Count
  Result ($n -ge 2) 'demo notice nasa upload forms'
  $v = (Get-ChildItem templates\admin -Filter admin_court*_pending.html | Select-String -Pattern 'viewIdBtn' | Measure-Object).Count
  Result ($v -eq 8) "View ID nasa court1-4 (count: $v, dapat 8)"
}

Write-Host ""
if ($script:fail -eq 0) { Write-Host 'LAHAT OK' -ForegroundColor Green }
else { Write-Host "$($script:fail) ang FAIL, i-paste ang output" -ForegroundColor Red }
