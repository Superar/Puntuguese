# .\experiments\classification\4-extract_features.ps1
$CROSS_VALIDATION_PATH = Join-Path (Get-Location) "data/cross_validation"
$CONTENT_FEATURES_PATH = Join-Path (Get-Location) "data/features/content_features"
$HUMOR_FEATURES_PATH = Join-Path (Get-Location) "data/features/humor_features"
$ALL_FEATURES_PATH = Join-Path (Get-Location) "data/features/all_features"

Push-Location ..\Literature_methods\HumorRecognitionPT

# Resources
$SENTLEX = ".\data\Lexica\SentiLex02.json"
$SLANG = ".\data\Lexica\termos_calao.json"
$ANTONYM_TRIPLES = ".\data\Lexica\antonyms.json"
$EMBEDDINGS = ".\data\Lexica\cbow_s300.txt"
$MWP = ".\data\Lexica\MWP.json"

# ------------- CONTENT FEATURES -------------
Write-Host "CONTENT FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Name | ForEach-Object {
    Write-Host $_ -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v feat `
        -i (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "train.json") `
        -o (Join-Path (Join-Path $CONTENT_FEATURES_PATH $_) "train") `
        --tfidf

    pipenv run python .\main.py -v feat `
        -i (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "test.json") `
        -o (Join-Path (Join-Path $CONTENT_FEATURES_PATH $_) "test") `
        --tfidf `
        --vectorizer (Join-Path (Join-Path $CONTENT_FEATURES_PATH $_) "train\vectorizer.pkl")
}

# ------------- HUMOR FEATURES -------------
Write-Host "HUMOR FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Name | ForEach-Object {
    Write-Host $_ -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v feat `
        -i (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "train.json") `
        -o (Join-Path (Join-Path $HUMOR_FEATURES_PATH $_) "train") `
        --sentlex $SENTLEX `
        --slang $SLANG `
        --alliteration `
        --antonym $ANTONYM_TRIPLES `
        --embeddings $EMBEDDINGS `
        --mwp $MWP `
        --ner `
        --ambiguity

    pipenv run python .\main.py -v feat `
        -i (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "test.json") `
        -o (Join-Path (Join-Path $HUMOR_FEATURES_PATH $_) "test") `
        --sentlex $SENTLEX `
        --slang $SLANG `
        --alliteration `
        --antonym $ANTONYM_TRIPLES `
        --embeddings $EMBEDDINGS `
        --mwp $MWP `
        --ner `
        --ambiguity
}

# ------------- ALL FEATURES -------------
Write-Host "ALL FEATURES" -ForegroundColor DarkGreen -BackgroundColor Red -NoNewline
Write-Output `n

Get-ChildItem -Path $CROSS_VALIDATION_PATH -Name | ForEach-Object {
    Write-Host $_ -ForegroundColor DarkGreen -BackgroundColor Cyan -NoNewline
    Write-Output `n

    pipenv run python .\main.py -v feat `
        -i (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "train.json") `
        -o (Join-Path (Join-Path $ALL_FEATURES_PATH $_) "train") `
        --tfidf `
        --sentlex $SENTLEX `
        --slang $SLANG `
        --alliteration `
        --antonym $ANTONYM_TRIPLES `
        --embeddings $EMBEDDINGS `
        --mwp $MWP `
        --ner `
        --ambiguity

    pipenv run python .\main.py -v feat `
        -i (Join-Path (Join-Path $CROSS_VALIDATION_PATH $_) "test.json") `
        -o (Join-Path (Join-Path $ALL_FEATURES_PATH $_) "test") `
        --tfidf `
        --vectorizer (Join-Path (Join-Path $ALL_FEATURES_PATH $_) "train\vectorizer.pkl") `
        --sentlex $SENTLEX `
        --slang $SLANG `
        --alliteration `
        --antonym $ANTONYM_TRIPLES `
        --embeddings $EMBEDDINGS `
        --mwp $MWP `
        --ner `
        --ambiguity
}

Pop-Location
