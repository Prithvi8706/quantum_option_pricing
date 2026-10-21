# AUTHOR-ONLY: do not execute until root reviews/pins this script and issues READY.
# This is one local paired-loader queue, with no retry, overwrite, upload or push.
# READY is an immutable ROOT-local JSON with schema paired-local-continuation-ready-v1:
# ready/local_execution_authorized/registration_authorized=true;
# producer_receipt and audit_receipt are the fixed run002/audit_run002 ROOT keys;
# producer_preflight_filename=two_draw_loader_implementation_preflight_v2.json;
# fixture_module_basename=test_two_draw_loader_source_v2;
# source_sha256 pins all eight active paired v2/method files plus this driver and
# verify_two_draw_loader_receipts.py (additional original source pins are allowed);
# tools.python {path,sha256} pins the T0 interpreter; tools.ruff pins a local ruff.exe;
# verifier_limits={process_CPU_seconds:180,work_admission_CPU_seconds:150,
# wall_seconds:600,work_admission_wall_seconds:540,maximum_references:100000,
# maximum_union_bytes:8589934592}; next_action_after_pair is root-authored text;
# continuation_receipt/verification_receipt/registration_receipt are fresh direct
# children of results/limitation_program_20261001; c8_launches lists exact {pid,
# creation_utc} identities, including any additional admission attempt selected by
# root; c8_gate {kind,receipt,manifest_sha256,source_receipt,
# root_verified_all_receipt_SHA:true,root_verified_owned_jobs_zero:true} identifies
# either a sealed_receipt or a root_failure_diagnostic, never an unsealed success.
# commands has exact executable/arguments records for ruff, producer_prepare,
# producer_run,audit_prepare,audit_run,verify,register. Scientific arguments use
# '-B','-m',module,prepare|run,'--output',ABSOLUTE_NATIVE_RECEIPT in that order.
# Verifier arguments use '-B',ABSOLUTE_VERIFIER,verify|register,... and --ready.
# This driver records commands, exits and source pins. Only the independent root
# verifier may register metadata; component cost rejection remains a valid PASS.
# Process identities use UTC ticks truncated to the same DMTF microsecond
# precision for CIM CreationDate, initial ISO timestamps and .NET StartTime.
param(
    [Parameter(Mandatory = $true)][string]$ReadyPath,
    [long]$InitialC8Pid = 0,
    [string]$InitialC8CreationUtc = '',
    [ValidateRange(1, 72)][int]$MaximumWaitHours = 24
)
$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\prith\quantum_option_pricing'
$Program = Join-Path $Root 'results\limitation_program_20261001'
$Families = @{}
$WaitStarted = [DateTime]::UtcNow
$DriverReceipt = $null
$ReadyHash = $null
$NoNextCommand = $false

function Require([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}
function ObservableTicks([long]$Ticks) { return $Ticks - ($Ticks % [long]10) }
function UtcTicks($Value) { return ObservableTicks ([DateTimeOffset]::Parse([string]$Value).UtcDateTime.Ticks) }
function ProcessTicks($Value) { return ObservableTicks (([DateTime]$Value).ToUniversalTime().Ticks) }
function IsBlocker($Row) {
    return $Row.ProcessId -ne $PID -and
        ($Row.Name -match '^(python(?:w|[0-9.]*)?|pypy(?:[0-9.]*)?|ruff)\.exe$' -or
         $Row.CommandLine -match '(stage_c_day|c7_c8_cases|c2_timing|run_c8_supervised)')
}
function LocalPath([string]$Value, [bool]$MustExist = $true) {
    Require (-not $Value.StartsWith('\\')) 'UNC paths are outside this local queue'
    if (-not [IO.Path]::IsPathRooted($Value)) {
        Require ($Value -notmatch '\\' -and $Value -notmatch '(^|/)\.\.?(/|$)' -and $Value -notmatch '//') 'Canonical ROOT-relative key required'
        $Value = Join-Path $Root $Value
    }
    $Path = [IO.Path]::GetFullPath($Value)
    Require ($Path.StartsWith($Root + '\', [StringComparison]::OrdinalIgnoreCase)) 'Path escaped ROOT'
    $Cursor = $Path
    while ($Cursor -and $Cursor -ne $Root) {
        if (Test-Path -LiteralPath $Cursor) {
            $Item = Get-Item -LiteralPath $Cursor
            Require (($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) -eq 0) 'Reparse/alias paths are rejected'
        }
        $Cursor = [IO.Path]::GetDirectoryName($Cursor)
    }
    if ($MustExist) { Require (Test-Path -LiteralPath $Path) ('Required local path absent: ' + $Path) }
    return $Path
}
function RootKey([string]$Path) { return (LocalPath $Path $false).Substring($Root.Length + 1).Replace('\', '/') }
function ReadJson([string]$Path) {
    $Path = LocalPath $Path
    Require ((Get-Item -LiteralPath $Path).Length -le 33554432) 'Metadata file exceeds32MiB'
    return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}
function NewJson([string]$Path, $Value) {
    $Bytes = [Text.Encoding]::UTF8.GetBytes(($Value | ConvertTo-Json -Depth 32) + "`n")
    Require ($Bytes.Length -le 33554432) 'New metadata file exceeds32MiB'
    $Stream = [IO.File]::Open($Path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
    try { $Stream.Write($Bytes, 0, $Bytes.Length) } finally { $Stream.Dispose() }
}
function HashLocal([string]$Path) {
    $Path = LocalPath $Path
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function HashBytes([byte[]]$Bytes) {
    $Algorithm = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($Algorithm.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $Algorithm.Dispose() }
}
function CheckHash([string]$Path, [string]$Expected) {
    Require ($Expected -cmatch '^[0-9a-f]{64}$') 'Explicit SHA256 pin required'
    Require ((HashLocal $Path) -ceq $Expected) ('Root-reviewed SHA differs: ' + $Path)
}
function AddLaunch([long]$Id, [string]$Created) {
    Require ($Id -gt 0 -and $Created) 'PID plus creation time required'
    $Ticks = UtcTicks $Created
    $Families[[string]$Id + '|' + [string]$Ticks] = [pscustomobject]@{ pid = $Id; ticks = $Ticks }
}
function ObserveProcesses {
    $Rows = @(Get-CimInstance Win32_Process | Select-Object ProcessId, ParentProcessId, CreationDate, Name, CommandLine)
    $RawRows = $Rows
    $KnownIds = @{}
    foreach ($Family in $Families.Values) { $KnownIds[[string]$Family.pid] = $true }
    foreach ($Row in $Rows) {
        if ($null -eq $Row.CreationDate -and ($KnownIds.ContainsKey([string]$Row.ProcessId) -or $KnownIds.ContainsKey([string]$Row.ParentProcessId) -or (IsBlocker $Row))) {
            throw 'Owned/possibly owned/blocking process creation identity unavailable; clearance uncertified'
        }
    }
    # Idle/protected unrelated rows without creation time do not define a family.
    $Rows = @($Rows | Where-Object { $null -ne $_.CreationDate })
    $Live = @{}
    foreach ($Row in $Rows) { $Live[[string]$Row.ProcessId] = $Row }
    $Changed = $true
    while ($Changed) {
        $Changed = $false
        foreach ($Row in $Rows) {
            $Parent = $Live[[string]$Row.ParentProcessId]
            if ($null -eq $Parent) { continue }
            $ParentIdentity = [string]$Parent.ProcessId + '|' + [string](ProcessTicks $Parent.CreationDate)
            $Identity = [string]$Row.ProcessId + '|' + [string](ProcessTicks $Row.CreationDate)
            if ($Families.ContainsKey($ParentIdentity) -and -not $Families.ContainsKey($Identity)) {
                Require ((ProcessTicks $Row.CreationDate) -ge (ProcessTicks $Parent.CreationDate)) 'Invalid descendant creation ordering'
                $Families[$Identity] = [pscustomobject]@{ pid = [long]$Row.ProcessId; ticks = ProcessTicks $Row.CreationDate }
                $Changed = $true
            }
        }
    }
    # A newly discovered known-time parent can reveal a missing-time grandchild.
    # Recheck the unfiltered rows after complete family expansion.
    $KnownIds = @{}
    foreach ($Family in $Families.Values) { $KnownIds[[string]$Family.pid] = $true }
    foreach ($Row in $RawRows) {
        if ($null -eq $Row.CreationDate -and ($KnownIds.ContainsKey([string]$Row.ProcessId) -or $KnownIds.ContainsKey([string]$Row.ParentProcessId) -or (IsBlocker $Row))) {
            throw 'Discovered descendant/blocker creation identity unavailable; clearance uncertified'
        }
    }
    $OwnedLive = @($Rows | Where-Object { $Families.ContainsKey([string]$_.ProcessId + '|' + [string](ProcessTicks $_.CreationDate)) })
    # The observer runs as this PowerShell script. No Python/Ruff process is exempted.
    $Foreign = @($Rows | Where-Object { IsBlocker $_ })
    return [pscustomobject]@{ owned_live = $OwnedLive; blocking_live = $Foreign }
}
function QuietOrStop {
    $State = ObserveProcesses
    Require ($State.owned_live.Count -eq 0 -and $State.blocking_live.Count -eq 0) 'Process clearance changed; no next command authorized'
}
function FreshChild([string]$Value) {
    $Path = LocalPath $Value $false
    Require ([IO.Path]::GetDirectoryName($Path) -eq $Program -and -not (Test-Path -LiteralPath $Path)) 'Fresh direct program receipt required'
    return $Path
}
function CheckGate($Gate) {
    Require ($Gate.root_verified_all_receipt_SHA -is [bool] -and $Gate.root_verified_all_receipt_SHA -and $Gate.root_verified_owned_jobs_zero -is [bool] -and $Gate.root_verified_owned_jobs_zero) 'Root terminal integrity/containment admission required'
    $Owner = LocalPath ([string]$Gate.receipt)
    CheckHash (Join-Path $Owner 'manifest.json') ([string]$Gate.manifest_sha256)
    $Manifest = ReadJson (Join-Path $Owner 'manifest.json')
    Require ($Manifest.manifest_self_hash_excluded -eq $true) 'C8 admission manifest self-hash convention required'
    $Terminal = Join-Path $Owner 'summary.json'
    $TerminalKey = RootKey $Terminal
    $Pin = $Manifest.files.PSObject.Properties[$TerminalKey].Value
    CheckHash $Terminal ([string]$Pin)
    if ($null -ne $Manifest.PSObject.Properties['terminal_record']) { Require ($Manifest.terminal_record -ceq $TerminalKey) 'C8 terminal pointer differs' }
    $Summary = ReadJson $Terminal
    Require (([string]($Summary | ConvertTo-Json -Depth 32)) -notmatch 'TERMINATION_UNCERTIFIED') 'C8 containment remains uncertified'
    if ($Gate.kind -eq 'root_failure_diagnostic') {
        Require ($Summary.passed -eq $false -and $Summary.not_a_success_certificate -eq $true) 'Root C8 failure diagnostic required'
        Require ($Summary.source_receipt -eq $Gate.source_receipt -and $Summary.inventory_job_terminal_active_processes -eq 0) 'Root failure diagnostic source/job clearance differs'
        Require (@($Summary.visible_unrelated_Python_processes).Count -eq 0) 'Failure diagnostic Python clearance differs'
    } elseif ($Gate.kind -eq 'sealed_receipt') {
        foreach ($Name in @('FAILED_UNSEALED.json', 'failed_unsealed.json', 'failure_retention_unsealed.json')) {
            Require (-not (Test-Path -LiteralPath (Join-Path $Owner $Name))) 'Unsealed C8 packet is not terminal admission evidence'
        }
        Require ($Summary.passed -is [bool]) 'Sealed C8 terminal boolean required'
        if ($Summary.passed) { Require ($null -ne $Summary.PSObject.Properties['rates_process'] -and $null -ne $Summary.PSObject.Properties['timing_process']) 'Successful C8 packet requires both phase terminals' }
        foreach ($Name in @('rates_process', 'timing_process')) {
            $Phase = $Summary.PSObject.Properties[$Name]
            if ($null -ne $Phase) { Require ($Phase.Value.job_terminal.active_processes -eq 0) 'C8 phase job not terminal-zero' }
        }
    } else { throw 'Unknown root C8 terminal admission kind' }
}
function QuoteArg([string]$Value) {
    # Windows CommandLineToArgvW quoting; no shell expansion is involved.
    return '"' + [regex]::Replace([regex]::Replace($Value, '(\\*)"', '$1$1\"'), '(\\+)$', '$1$1') + '"'
}
function CheckCommand($Actual, [string]$Exe, [string[]]$Arguments) {
    Require ([IO.Path]::GetFullPath([string]$Actual.executable) -eq $Exe) 'Root READY command executable differs'
    Require ((@($Actual.arguments) | ConvertTo-Json -Compress) -ceq ($Arguments | ConvertTo-Json -Compress)) 'Root READY exact CLI differs'
}
function InvokeRecorded([string]$Name, $Command, [int]$ObservationLimit = 650) {
    QuietOrStop
    CheckHash $ReadyPath $ReadyHash
    foreach ($Pin in $Ready.source_sha256.PSObject.Properties) { CheckHash (LocalPath $Pin.Name) ([string]$Pin.Value) }
    CheckHash $Python ([string]$Ready.tools.python.sha256)
    Require ((Get-FileHash -LiteralPath $Ruff -Algorithm SHA256).Hash.ToLowerInvariant() -ceq [string]$Ready.tools.ruff.sha256) 'Pinned Ruff changed before queue command'
    $Before = [DateTime]::UtcNow
    $Arguments = (@($Command.arguments) | ForEach-Object { QuoteArg ([string]$_) }) -join ' '
    $Record = [ordered]@{ command = $Name; executable = $Command.executable; arguments = @($Command.arguments); started_utc = $Before.ToString('o'); no_retry = $true }
    NewJson (Join-Path $DriverReceipt ($Name + '_command.json')) $Record
    $Process = Start-Process -FilePath $Command.executable -ArgumentList $Arguments -WorkingDirectory $Root -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $DriverReceipt ($Name + '_stdout.txt')) -RedirectStandardError (Join-Path $DriverReceipt ($Name + '_stderr.txt'))
    $null = $Process.Handle  # Retain the exact owned root handle through exit/accounting.
    $Created = $Process.StartTime.ToUniversalTime().ToString('o')
    AddLaunch $Process.Id $Created
    NewJson (Join-Path $DriverReceipt ($Name + '_launched.json')) @{ pid = $Process.Id; creation_utc = $Created; identity_UTC_ticks_at_DMTF_microsecond_precision = UtcTicks $Created; no_foreign_pid_termination = $true }
    $null = ObserveProcesses
    $LastObservation = [DateTime]::UtcNow
    while (-not $Process.WaitForExit(1000)) {
        if (([DateTime]::UtcNow - $LastObservation).TotalSeconds -ge 30) {
            $null = ObserveProcesses
            $LastObservation = [DateTime]::UtcNow
        }
        if (([DateTime]::UtcNow - $Before).TotalSeconds -ge $ObservationLimit) {
            $script:NoNextCommand = $true
            NewJson (Join-Path $DriverReceipt ($Name + '_TERMINATION_UNCERTIFIED.json')) @{ passed = $false; owned_root_exit_not_observed = $true; no_next_command = $true; no_foreign_pid_termination = $true }
            throw 'Owned command has no observed terminal exit; queue stopped without killing any PID'
        }
    }
    $Process.Refresh()
    $ExitCode = $Process.ExitCode
    $CPU = $Process.TotalProcessorTime.TotalSeconds
    $State = ObserveProcesses
    if ($State.owned_live.Count -or $State.blocking_live.Count) {
        $script:NoNextCommand = $true
        throw 'Root exited with visible descendants or foreign compute; no next command or receipt verification'
    }
    NewJson (Join-Path $DriverReceipt ($Name + '_exit.json')) @{ pid = $Process.Id; creation_utc = $Created; exit_code = $ExitCode; observed_root_CPU_seconds = $CPU; observed_wall_seconds = ([DateTime]::UtcNow - $Before).TotalSeconds; visible_owned_descendants = 0; no_adoption_in_driver = $true }
    $Process.Dispose()
    return $ExitCode
}
function SealDriver($Summary) {
    QuietOrStop
    NewJson (Join-Path $DriverReceipt 'summary.json') $Summary
    $Owned = @{}
    $Bytes = [long]0
    foreach ($File in Get-ChildItem -LiteralPath $DriverReceipt -Recurse -File) {
        $Bytes += $File.Length
        Require ($Owned.Count -lt 128 -and $Bytes -le 1073741824) 'Bounded driver record inventory exceeded'
        $Owned[(RootKey $File.FullName)] = HashLocal $File.FullName
    }
    $Frozen = @{}
    foreach ($Pin in $Ready.source_sha256.PSObject.Properties) {
        CheckHash (LocalPath $Pin.Name) ([string]$Pin.Value)
        $Frozen[$Pin.Name] = [string]$Pin.Value
    }
    CheckHash $ReadyPath $ReadyHash
    $Frozen[(RootKey $ReadyPath)] = $ReadyHash
    $Frozen[(RootKey $Python)] = [string]$Ready.tools.python.sha256
    $Frozen[(RootKey (Join-Path (LocalPath $Ready.c8_gate.receipt) 'manifest.json'))] = [string]$Ready.c8_gate.manifest_sha256
    NewJson (Join-Path $DriverReceipt 'manifest.json') @{ files = $Owned; frozen_inputs = $Frozen; manifest_self_hash_excluded = $true; terminal_record = RootKey (Join-Path $DriverReceipt 'summary.json') }
}

$ReadyPath = LocalPath $ReadyPath $false
Require (($InitialC8Pid -eq 0) -eq (-not $InitialC8CreationUtc)) 'Initial C8 PID/time must be supplied together'
if ($InitialC8Pid) { AddLaunch $InitialC8Pid $InitialC8CreationUtc }
while ($true) {
    Require (([DateTime]::UtcNow - $WaitStarted).TotalHours -lt $MaximumWaitHours) 'Quiet/readiness wait expired; no command launched'
    $Candidate = $null
    if (Test-Path -LiteralPath $ReadyPath) {
        $Candidate = ReadJson $ReadyPath
        foreach ($Launch in @($Candidate.c8_launches)) { AddLaunch ([long]$Launch.pid) ([string]$Launch.creation_utc) }
    }
    $State = ObserveProcesses
    if ($State.owned_live.Count -eq 0 -and $State.blocking_live.Count -eq 0 -and $null -ne $Candidate -and $Candidate.ready -eq $true -and $Candidate.local_execution_authorized -eq $true -and $null -ne $Candidate.c8_gate) { break }
    # No Python, Ruff, compile, imports, source hash scans or numerical work here.
    Start-Sleep -Seconds 30
}

try {
    QuietOrStop
    Require ((Get-Item -LiteralPath $ReadyPath).Length -le 1048576) 'Root READY exceeds1MiB'
    $ReadyBytes = [IO.File]::ReadAllBytes($ReadyPath)
    $Ready = [Text.Encoding]::UTF8.GetString($ReadyBytes) | ConvertFrom-Json
    $ReadyHash = HashBytes $ReadyBytes
    CheckHash $ReadyPath $ReadyHash
    Require ($Ready.schema -eq 'paired-local-continuation-ready-v1' -and $Ready.ready -is [bool] -and $Ready.ready -and $Ready.local_execution_authorized -is [bool] -and $Ready.local_execution_authorized) 'Actual root READY release required'
    CheckGate $Ready.c8_gate
    $Producer = LocalPath 'results/limitation_program_20261001/A02_two_draw_loader_resource_run002' $false
    $Audit = LocalPath 'results/limitation_program_20261001/A02_two_draw_loader_resource_audit_run002' $false
    Require ($Ready.producer_receipt -ceq (RootKey $Producer) -and $Ready.audit_receipt -ceq (RootKey $Audit)) 'Only root-selected fresh paired v2 receipts supported'
    Require ($Ready.producer_preflight_filename -ceq 'two_draw_loader_implementation_preflight_v2.json' -and $Ready.fixture_module_basename -ceq 'test_two_draw_loader_source_v2') 'Fixed v2 preflight and32-fixture module required'
    $Limits = $Ready.verifier_limits
    Require ($Limits.process_CPU_seconds -eq 180 -and $Limits.work_admission_CPU_seconds -eq 150 -and $Limits.wall_seconds -eq 600 -and $Limits.work_admission_wall_seconds -eq 540 -and $Limits.maximum_references -eq 100000 -and $Limits.maximum_union_bytes -eq 8589934592) 'Prospectively reviewed verifier bounds required'
    Require (-not (Test-Path -LiteralPath $Producer) -and -not (Test-Path -LiteralPath $Audit)) 'No existing paired receipt may be retried or overwritten'
    $Required = @('two_draw_loader_source_v2.py', 'experiment_two_draw_loader_resource_v2.py', 'test_two_draw_loader_source_v2.py', 'audit_two_draw_loader_resource_v2.py', 'TWO_DRAW_LOADER_IMPLEMENTATION_PREFLIGHT_V2.md', 'two_draw_loader_implementation_preflight_v2.json', 'TWO_DRAW_LOADER_RESOURCE_PREFLIGHT.md', 'two_draw_loader_resource_preflight.json', 'verify_two_draw_loader_receipts.py', 'continue_after_c8.ps1')
    $Pins = @($Ready.source_sha256.PSObject.Properties)
    Require ($Pins.Count -le 64) 'Bounded exact source pin inventory required'
    foreach ($Name in $Required) { Require ($null -ne $Ready.source_sha256.PSObject.Properties['research/limitation_program_20261001/' + $Name]) ('Root READY missing source pin: ' + $Name) }
    foreach ($Pin in $Pins) {
        Require ($Pin.Name -ceq (RootKey (LocalPath $Pin.Name))) 'Source SHA keys must be canonical ROOT-relative'
        CheckHash (LocalPath $Pin.Name) ([string]$Pin.Value)
    }
    Require ((LocalPath $PSCommandPath) -eq (LocalPath 'research/limitation_program_20261001/continue_after_c8.ps1')) 'Executed driver path differs from reviewed source'
    $Python = LocalPath $Ready.tools.python.path
    Require ($Python -eq (LocalPath '.context/frontier_t0_env/Scripts/python.exe')) 'Pinned local T0 Python required'
    CheckHash $Python ([string]$Ready.tools.python.sha256)
    Require ([IO.Path]::IsPathRooted([string]$Ready.tools.ruff.path)) 'Ruff pin must use an explicit absolute local path'
    $Ruff = [IO.Path]::GetFullPath([string]$Ready.tools.ruff.path)
    Require (-not $Ruff.StartsWith('\\') -and [IO.Path]::GetFileName($Ruff) -eq 'ruff.exe') 'Pinned local Ruff executable required'
    Require ((Get-FileHash -LiteralPath $Ruff -Algorithm SHA256).Hash.ToLowerInvariant() -ceq [string]$Ready.tools.ruff.sha256) 'Root READY Ruff SHA differs'
    $VerifyFile = LocalPath 'research/limitation_program_20261001/verify_two_draw_loader_receipts.py'
    $VerifyReceipt = FreshChild $Ready.verification_receipt
    $RegisterReceipt = FreshChild $Ready.registration_receipt
    $DriverReceipt = FreshChild $Ready.continuation_receipt
    Require (@($Producer, $Audit, $VerifyReceipt, $RegisterReceipt, $DriverReceipt | Select-Object -Unique).Count -eq 5) 'Distinct fresh queue receipts required'
    $PyFiles = @($Required[0..3] | ForEach-Object { LocalPath ('research/limitation_program_20261001/' + $_) })
    CheckCommand $Ready.commands.ruff $Ruff (@('check', '--no-cache') + $PyFiles)
    $Modules = @{ producer = 'research.limitation_program_20261001.experiment_two_draw_loader_resource_v2'; audit = 'research.limitation_program_20261001.audit_two_draw_loader_resource_v2' }
    foreach ($Phase in @('prepare', 'run')) {
        CheckCommand $Ready.commands.PSObject.Properties['producer_' + $Phase].Value $Python @('-B', '-m', $Modules.producer, $Phase, '--output', $Producer)
        CheckCommand $Ready.commands.PSObject.Properties['audit_' + $Phase].Value $Python @('-B', '-m', $Modules.audit, $Phase, '--output', $Audit)
    }
    $VerifyArgs = @('-B', $VerifyFile, 'verify', '--producer', $Producer, '--audit', $Audit, '--output', $VerifyReceipt, '--ready', $ReadyPath)
    $RegisterArgs = @('-B', $VerifyFile, 'register', '--producer', $Producer, '--audit', $Audit, '--output', $RegisterReceipt, '--ready', $ReadyPath, '--verification', (Join-Path $VerifyReceipt 'summary.json'))
    CheckCommand $Ready.commands.verify $Python $VerifyArgs
    CheckCommand $Ready.commands.register $Python $RegisterArgs
    QuietOrStop
    CheckHash $ReadyPath $ReadyHash
    $null = New-Item -ItemType Directory -Path $DriverReceipt
    [IO.File]::WriteAllBytes((Join-Path $DriverReceipt 'root_READY_snapshot.json'), $ReadyBytes)
    CheckHash (Join-Path $DriverReceipt 'root_READY_snapshot.json') $ReadyHash
    NewJson (Join-Path $DriverReceipt 'admission.json') @{ root_READY_sha256 = $ReadyHash; fixed_source_sha256 = $Ready.source_sha256; c8_terminal_gate = $Ready.c8_gate; all_launch_identities_bound_to_PID_and_creation_time = $true; no_cloud_push_upload = $true; driver_does_not_adopt_or_count_fixtures = $true }
    Require ((InvokeRecorded 'ruff' $Ready.commands.ruff 120) -eq 0) 'Ruff rejected frozen new author files; no scientific launch'
    $NumericFailure = $false
    foreach ($Name in @('producer_prepare', 'producer_run', 'audit_prepare', 'audit_run')) {
        if ((InvokeRecorded $Name $Ready.commands.PSObject.Properties[$Name].Value) -ne 0) { $NumericFailure = $true; break }
    }
    $VerifyExit = InvokeRecorded 'verify' $Ready.commands.verify
    Require ($VerifyExit -eq 0) 'Root verifier rejected packet integrity; no registration'
    $Verified = ReadJson (Join-Path $VerifyReceipt 'summary.json')
    Require ($Verified.passed -eq $true -and $Verified.safe_to_register_progress -eq $true) 'Root verification is not complete'
    Require ($Ready.registration_authorized -is [bool] -and $Ready.registration_authorized) 'Root READY did not authorize reversible local metadata registration'
    Require ((InvokeRecorded 'register' $Ready.commands.register) -eq 0) 'Registration failed; preserved failure evidence requires root review'
    SealDriver @{ passed = $true; budget_censored = $false; new_test_credit = 0; numeric_nonzero_exit_preserved = $NumericFailure; root_verified_outcome = $Verified.pair.outcome; verified_producer_fixture_credit = $Verified.pair.producer_fixture_credit; audit_fixture_credit = 0; component_preference_from_independent_audit = $Verified.pair.component_preferred; full_financial_adoption = $false; quantum_advantage_claim = $false; no_retry_or_overwrite = $true; local_only = $true }
} catch {
    if ($DriverReceipt -and (Test-Path -LiteralPath $DriverReceipt)) {
        $Manifest = Join-Path $DriverReceipt 'manifest.json'
        if (Test-Path -LiteralPath $Manifest) { Move-Item -LiteralPath $Manifest -Destination (Join-Path $DriverReceipt 'manifest_invalid_after_failure.json') }
        $FailureFile = Join-Path $DriverReceipt 'FAILED_UNSEALED.json'
        if (-not (Test-Path -LiteralPath $FailureFile)) { NewJson $FailureFile @{ passed = $false; error = [string]$_; no_next_command = $true; fixture_credit_by_driver = 0; partial_files_preserved = $true; no_retry_or_overwrite = $true; metadata_updates_if_any_are_separate_verifier_evidence = $true; containment_uncertified = $NoNextCommand } }
    }
    throw
}
