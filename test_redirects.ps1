param([string]$Base = 'http://127.0.0.1:5000')
$Base = $Base.TrimEnd('/')
Add-Type -AssemblyName System.Net.Http
$h = New-Object System.Net.Http.HttpClientHandler
$h.AllowAutoRedirect = $false
$c = New-Object System.Net.Http.HttpClient($h)
$c.Timeout = [TimeSpan]::FromSeconds(90)
$fail = 0

function Check($ok, $msg) {
  if ($ok) { Write-Host "[PASS] $msg" -ForegroundColor Green }
  else { Write-Host "[FAIL] $msg" -ForegroundColor Red; $script:fail++ }
}

$r = $c.PostAsync("$Base/forgot-password", (New-Object System.Net.Http.FormUrlEncodedContent([System.Collections.Generic.Dictionary[string,string]]@{ email = 'nobody-test@example.com' }))).Result
$code = [int]$r.StatusCode
Check ($code -lt 500) "POST /forgot-password walang server error (code: $code)"

foreach ($p in '/uploads/test.jpg', '/api/file-url/test.jpg', '/admins', '/dashboard') {
  $r = $c.GetAsync("$Base$p").Result
  $code = [int]$r.StatusCode
  $loc = $r.Headers.Location
  Check ($code -in 301,302,303,307,401,403) "$p protektado kapag hindi naka-login (code: $code $loc)"
}

if ($fail -eq 0) { Write-Host 'LAHAT OK' -ForegroundColor Green } else { Write-Host "$fail FAIL" -ForegroundColor Red }
