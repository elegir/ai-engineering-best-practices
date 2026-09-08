# Usage: powershell -File scripts/new-worktree.ps1 -Slug T-003-sso-signup [-Base main]
param(
  [Parameter(Mandatory=$true)][string]$Slug,
  [string]$Base = "main"
)
$ErrorActionPreference = "Stop"
$RepoDir  = (git rev-parse --show-toplevel).Trim()
$RepoName = Split-Path $RepoDir -Leaf
$WtDir    = Join-Path (Split-Path $RepoDir -Parent) "$RepoName-$Slug"

git -C $RepoDir fetch origin $Base 2>$null
try { git -C $RepoDir worktree add -b $Slug $WtDir "origin/$Base" } catch { git -C $RepoDir worktree add -b $Slug $WtDir $Base }

# Copy includes
$inc = Join-Path $RepoDir ".worktreeinclude"
if (Test-Path $inc) {
  Get-Content $inc | Where-Object { $_ -and -not $_.StartsWith("#") } | ForEach-Object {
    $src = Join-Path $RepoDir $_
    if (Test-Path $src) {
      $dst = Join-Path $WtDir $_
      New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
      Copy-Item -Recurse -Force $src $dst
    }
  }
}

# Deterministic port + DB name
$safe = ($Slug -replace '[^a-zA-Z0-9]', '_').ToLower()
$hash = 0; $Slug.ToCharArray() | ForEach-Object { $hash = ($hash * 31 + [int]$_) % 900 }
$port = <<3100>> + $hash
$db   = "<<appdb>>_$safe"

Add-Content (Join-Path $WtDir ".env") "`n# --- worktree overrides ($Slug) ---`nAPP_PORT=$port`nDATABASE_URL=<<postgres://app:app@localhost:5432/>>$db"

Set-Location $WtDir
<<npm ci>>
<<createdb $db 2>$null>>
<<npm run migrate>>
<<npm run seed>>

Write-Host "Worktree ready: $WtDir (branch $Slug, port $port, db $db)"
Write-Host "Start Claude Code here with: cd `"$WtDir`"; claude"
