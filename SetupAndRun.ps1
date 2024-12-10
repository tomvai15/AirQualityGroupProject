Write-Output "Checking if Python is installed..."
$python = Get-Command python -ErrorAction SilentlyContinue

if (-Not $python) {
    Write-Error "Python is not installed or not available in PATH. Please install Python and try again."
    exit 1
} else {
    Write-Output "Python is installed: $($python.Path)"
}

# Define virtual environment name
$envName = "venv"

# Create a virtual environment if it doesn't exist
if (-Not (Test-Path -Path $envName)) {
    Write-Output "Creating virtual environment..."
    python -m venv $envName
    if (-Not (Test-Path -Path $envName)) {
        Write-Error "Failed to create virtual environment."
        exit 1
    }
    Write-Output "Virtual environment '$envName' created."
} else {
    Write-Output "Virtual environment '$envName' already exists."
}

$activatePath = ".\$envName\Scripts\Activate.ps1"

if (-Not (Test-Path -Path $activatePath)) {
    Write-Error "Failed to find activation script for virtual environment: $activatePath"
    exit 1
}

Write-Output "Activating virtual environment..."
& $activatePath

# Install dependencies
if (-Not (Test-Path -Path "requirements.txt")) {
    Write-Error "requirements.txt not found. Please create one and list your dependencies."
    exit 1
}

Write-Output "Installing dependencies..."
& "$envName/Scripts/pip.exe" install -r requirements.txt | Select-String -NotMatch "already satisfied"

if ($LastExitCode -ne 0) {
    Write-Error "Failed to install dependencies."
    exit 1
}

Write-Output "Dependencies installed."

# Start the Streamlit app
Write-Output "Starting the app..."
& "$envName/Scripts/python.exe" -m streamlit run main.py

if ($LastExitCode -ne 0) {
    Write-Error "Failed to start the Streamlit app."
    exit 1
}
