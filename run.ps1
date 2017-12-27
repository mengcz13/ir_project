python build.py
Set-Location -Path ir_frontend -PassThru
$env:FLASK_APP = "frontend.py"
python -m flask run