# .\experiments\by_dialect\4-cross_validation.ps1
$MODELS_PATH = Join-Path (Get-Location) "results\models_by_dialect"
$PREDICTIONS_PATH = Join-Path (Get-Location) "results\predictions_by_dialect"
$CROSS_VALIDATION_PATH = Join-Path (Get-Location) "data\cv_by_dialect"
$FEATURES_PATH = Join-Path (Get-Location) "data\features_by_dialect"

Push-Location ..\Literature_methods\HumorRecognitionPT

# ------------- FEATURE-BASED -------------

Get-ChildItem -Path $FEATURES_PATH -Recurse | Where-Object {$_.BaseName -Match "train"} | ForEach-Object {
    $feature_type = $_.Parent.Parent.Parent.Name
    $dialect = $_.Parent.Parent.Name
    $fold = $_.Parent.Name
    Write-Host $feature_type / $dialect / $fold -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v clemencio train `
    --input (Join-Path $_ "data.hdf5") `
    --output (Join-Path (Join-Path (Join-Path $MODELS_PATH $feature_type) $dialect) $fold) `
    --method "RandomForest"

    pipenv run python .\main.py -v clemencio test `
    --input (Join-Path $_.Parent "test\data.hdf5") `
    --output (Join-Path (Join-Path (Join-Path $PREDICTIONS_PATH $feature_type) $dialect) ($fold + ".json")) `
    --model (Join-Path (Join-Path (Join-Path $MODELS_PATH $feature_type) $dialect) $fold)
}

# ------------- BERTimbau -------------
Write-Host "BERTimbau" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Recurse | Where-Object {$_.Name -Match "train.json"} | ForEach-Object {
    $dialect = $_.Directory.Parent.Name
    $fold = $_.Directory.Name
    $checkpoint = If ($dialect -Match "PT_BR") {"checkpoint-2802"} Else {"checkpoint-510"}
    Write-Host $dialect / $fold -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v transformer fine-tune `
    --input $_ `
    --output (Join-Path (Join-Path (Join-Path $MODELS_PATH "bertimbau") $dialect) $fold) `

    pipenv run python .\main.py -v transformer test `
    --input (Join-Path $_.Directory "test.json") `
    --output (Join-Path (Join-Path (Join-Path $PREDICTIONS_PATH "bertimbau") $dialect) ($fold + ".json")) `
    --model (Join-Path (Join-Path (Join-Path (Join-Path $MODELS_PATH "bertimbau") $dialect) $fold) $checkpoint)
}

# ------------- ALBERTINA PT-* -------------
Write-Host "ALBERTINA PT-*" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Recurse | Where-Object {$_.Name -Match "train.json"} | ForEach-Object {
    $dialect = $_.Directory.Parent.Name
    $fold = $_.Directory.Name
    $checkpoint = If ($dialect -Match "PT_BR") {"checkpoint-4670"} Else {"checkpoint-850"}
    $model = If ($dialect -match "PT_BR") {"PORTULAN/albertina-ptbr-base"} Else {"PORTULAN/albertina-ptpt-base"}
    Write-Host $dialect / $fold -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n


    pipenv run python .\main.py -v transformer fine-tune `
    --input $_ `
    --output (Join-Path (Join-Path (Join-Path $MODELS_PATH "albertina_base") $dialect) $fold) `
    --model $model `
    --learning_rate 1e-6 `
    --epochs 5

    pipenv run python .\main.py -v transformer test `
    --input (Join-Path $_.Directory "test.json") `
    --output (Join-Path (Join-Path (Join-Path $PREDICTIONS_PATH "albertina_base") $dialect) ($fold + ".json")) `
    --model (Join-Path (Join-Path (Join-Path (Join-Path $MODELS_PATH "albertina_base") $dialect) $fold) $checkpoint)
}

Pop-Location