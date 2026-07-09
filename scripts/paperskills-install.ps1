param(
  [string]$Tool = "codex",
  [string]$Skills = "",
  [string]$Registry = "https://paperskills.com/api/registry",
  [switch]$Force
)

if ([string]::IsNullOrWhiteSpace($Skills)) {
  Write-Error "Missing -Skills"
  exit 2
}

switch ($Tool) {
  "claude" { $targetRoot = Join-Path $HOME ".claude\skills" }
  "codex" { $targetRoot = Join-Path $HOME ".codex\skills" }
  "opencode" { $targetRoot = Join-Path $HOME ".opencode\skills" }
  "cursor" { $targetRoot = Join-Path $HOME ".cursor\rules" }
  default {
    Write-Error "Unsupported tool: $Tool"
    exit 2
  }
}

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("paperskills-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmp | Out-Null

try {
  function Install-SkillDirectory {
    param(
      [string]$InstallId,
      [string]$SourceDir
    )

    $destination = Join-Path $targetRoot $InstallId
    if ((Test-Path $destination) -and -not $Force) {
      Write-Host "Skip existing $destination. Use -Force to replace it."
      return
    }

    if (Test-Path $destination) {
      Remove-Item -Recurse -Force $destination
    }
    Copy-Item -Recurse $SourceDir $destination
    Write-Host "Installed $InstallId"
  }

  $registryFile = Join-Path $tmp "registry.json"
  if ($Registry -match "^https?://") {
    Invoke-WebRequest -Uri $Registry -OutFile $registryFile
  } elseif (Test-Path $Registry) {
    Copy-Item $Registry $registryFile
  } else {
    Write-Error "Registry file not found: $Registry"
    exit 1
  }

  $registryJson = Get-Content $registryFile -Raw | ConvertFrom-Json
  $skillMap = @{}
  foreach ($skill in $registryJson.skills) {
    $skillMap[$skill.id] = $skill
  }
  $packMap = @{}
  foreach ($pack in $registryJson.packs) {
    $packMap[$pack.id] = $pack
  }

  $expanded = New-Object System.Collections.Generic.List[string]
  foreach ($raw in $Skills.Split(",")) {
    $id = $raw.Trim()
    if ([string]::IsNullOrWhiteSpace($id)) { continue }
    if ($packMap.ContainsKey($id)) {
      foreach ($skillId in $packMap[$id].skillIds) {
        $expanded.Add([string]$skillId)
      }
    } else {
      $expanded.Add($id)
    }
  }

  Write-Host "Installing PaperSkills into $targetRoot"
  New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

  $seen = @{}
  foreach ($skillId in $expanded) {
    if ($seen.ContainsKey($skillId)) { continue }
    $seen[$skillId] = $true

    if (-not $skillMap.ContainsKey($skillId)) {
      Write-Error "Unknown skill id: $skillId"
      exit 1
    }

    $skill = $skillMap[$skillId]
    $install = $skill.install
    $method = [string]$install.method
    $url = [string]$install.url
    $ref = if ($install.ref) { [string]$install.ref } else { "" }
    $sparsePath = if ($install.sparsePath) { [string]$install.sparsePath } elseif ($install.sparse_path) { [string]$install.sparse_path } else { "" }

    if ([string]::IsNullOrWhiteSpace($url)) {
      Write-Error "Missing install URL for $skillId"
      exit 1
    }

    $workdir = Join-Path $tmp ("checkout-" + $skillId)
    if ($method -eq "git-clone") {
      $cloneArgs = @("clone", "--depth", "1")
      if (-not [string]::IsNullOrWhiteSpace($ref)) {
        $cloneArgs += @("--branch", $ref)
      }
      $cloneArgs += @($url, $workdir)
      git -c http.version=HTTP/1.1 @cloneArgs | Out-Null
      $source = $workdir
    } elseif ($method -eq "sparse-checkout") {
      if ([string]::IsNullOrWhiteSpace($sparsePath)) {
        Write-Error "Missing sparsePath for $skillId"
        exit 1
      }
      $cloneArgs = @("clone", "--filter=blob:none", "--sparse", "--depth", "1")
      if (-not [string]::IsNullOrWhiteSpace($ref)) {
        $cloneArgs += @("--branch", $ref)
      }
      $cloneArgs += @($url, $workdir)
      git -c http.version=HTTP/1.1 @cloneArgs | Out-Null
      Push-Location $workdir
      git sparse-checkout set $sparsePath | Out-Null
      Pop-Location
      $source = Join-Path $workdir $sparsePath
    } else {
      Write-Error "Unsupported install method for $skillId`: $method"
      exit 1
    }

    if (Test-Path (Join-Path $source "SKILL.md")) {
      Install-SkillDirectory -InstallId $skillId -SourceDir $source
      continue
    }

    $collectionRoot = $source
    $skillsDir = Join-Path $source "skills"
    if (Test-Path $skillsDir) {
      $collectionRoot = $skillsDir
    }

    $skillFiles = Get-ChildItem -Path $collectionRoot -Filter "SKILL.md" -File -Recurse | Sort-Object FullName
    if ($skillFiles.Count -eq 0) {
      Write-Error "SKILL.md not found for $skillId at $source"
      exit 1
    }

    Write-Host "Installing collection $skillId ($($skillFiles.Count) skills)"
    foreach ($skillFile in $skillFiles) {
      $childSource = $skillFile.Directory.FullName
      $childId = Split-Path $childSource -Leaf
      Install-SkillDirectory -InstallId $childId -SourceDir $childSource
    }
  }

  if ($Tool -eq "cursor") {
    Write-Host "Cursor uses rules/prompt installation in this MVP. Review imported files under $targetRoot."
  }

  Write-Host "Done."
}
finally {
  Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}
