# ─── WealthFA 대시보드 배포 엔진 ──────────────────────────
# 이 파일은 배포하기.bat에 의해 자동으로 호출됩니다.
# ──────────────────────────────────────────────────────────

param(
    [string]$Token = "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"
)

$ErrorActionPreference = "Stop"
$src = "g:\내 드라이브\안티그래비티\TEST"
$remote = "https://$Token@github.com/kbj1057-a11y/wealthfa_Dashboard.git"
$tmp = Join-Path $env:TEMP ("wfa_deploy_" + [System.IO.Path]::GetRandomFileName().Replace(".",""))

try {
    Write-Host "[1/5] 임시 배포 환경 생성 중..."
    New-Item -ItemType Directory -Path $tmp | Out-Null
    New-Item -ItemType Directory -Path "$tmp\매일업데이트" | Out-Null

    Write-Host "[2/5] 파일 복사 중..."

    # dashboard.py
    $src_dash = Join-Path $src "dashboard.py"
    if (-not (Test-Path $src_dash)) { throw "dashboard.py 를 찾을 수 없습니다: $src_dash" }
    Copy-Item $src_dash "$tmp\" 
    Write-Host "  OK: dashboard.py"

    # requirements.txt
    "streamlit`npandas`nplotly`nopenpyxl`npytz" | Out-File "$tmp\requirements.txt" -Encoding utf8
    Write-Host "  OK: requirements.txt"

    # 26년종합.xlsx (핵심 데이터)
    $src_excel = Join-Path $src "매일업데이트\26년종합.xlsx"
    if (-not (Test-Path $src_excel)) { throw "26년종합.xlsx 를 찾을 수 없습니다: $src_excel" }
    Copy-Item $src_excel "$tmp\매일업데이트\"
    Write-Host "  OK: 매일업데이트/26년종합.xlsx"

    # README (선택)
    $src_readme = Join-Path $src "README.md"
    if (Test-Path $src_readme) { Copy-Item $src_readme "$tmp\" ; Write-Host "  OK: README.md" }

    Write-Host "[3/5] Git 초기화 중..."
    Set-Location $tmp
    git init | Out-Null
    git config user.email "deploy@wealthfa.com"
    git config user.name "WealthFA-Bot"
    git remote add origin $remote

    Write-Host "[4/5] 커밋 중..."
    git add -A
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "data-update: $date"
    if ($LASTEXITCODE -ne 0) { throw "커밋 실패 (변경사항 없음?)" }

    Write-Host "[5/5] GitHub 전송 중..."
    git branch -M main | Out-Null
    git push origin main --force
    $pushResult = $LASTEXITCODE

    Set-Location "C:\"
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue

    if ($pushResult -eq 0) {
        Write-Host ""
        Write-Host "=========================================="
        Write-Host "  배포 성공!"
        Write-Host ""
        Write-Host "  업로드 파일:"
        Write-Host "    - dashboard.py"
        Write-Host "    - 매일업데이트/26년종합.xlsx"
        Write-Host "    - requirements.txt"
        Write-Host ""
        Write-Host "  30초 후 확인:"
        Write-Host "    https://wealhfa.streamlit.app/"
        Write-Host "=========================================="
        exit 0
    } else {
        Write-Host "GitHub 전송 실패! 토큰을 확인하세요." -ForegroundColor Red
        exit 1
    }

} catch {
    Set-Location "C:\" -ErrorAction SilentlyContinue
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ""
    Write-Host "오류 발생: $_" -ForegroundColor Red
    exit 1
}
