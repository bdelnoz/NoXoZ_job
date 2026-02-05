#!/bin/bash

################################################################################
# SCRIPT INFORMATION
################################################################################
# Script Name    : /home/claude/ollama-batch-download.sh
# Author         : Bruno DELNOZ
# Email          : bruno.delnoz@protonmail.com
# Version        : V1.0
# Date           : 2025-02-05
# Target Usage   : Download multiple Ollama models overnight within storage limit
#
# CHANGELOG:
# V1.0 - 2025-02-05 - Initial version
#   - Batch download of curated Ollama models
#   - Storage limit verification (50GB)
#   - Prerequisite checking and installation
#   - Dry-run simulation mode
#   - Detailed logging and progress tracking
#   - Model size estimation before download
################################################################################

# Default configuration
STORAGE_LIMIT_GB=50
LOG_DIR="./logs"
RESULTS_DIR="./results"
LOG_FILE="${LOG_DIR}/log.ollama-batch-download.v1.0.log"
MODELS_LIST="${RESULTS_DIR}/downloaded-models.ollama-batch-download.v1.0.txt"
SIMULATE=false

# Model list with estimated sizes (in GB)
declare -A MODELS=(
    ["mistral:latest"]=4.1
    ["mistral:7b"]=4.1
    ["llama3.2:latest"]=2.0
    ["llama3.2:3b"]=2.0
    ["codellama:7b"]=3.8
    ["gemma2:2b"]=1.6
    ["qwen2.5:3b"]=1.9
    ["deepseek-r1:7b"]=4.4
    ["deepseek-r1:8b"]=4.7
    ["phi3:mini"]=2.3
    ["phi3:medium"]=7.9
    ["orca-mini:3b"]=1.9
    ["neural-chat:7b"]=4.1
    ["starling-lm:7b"]=4.1
    ["solar:10.7b"]=6.1
)

################################################################################
# FUNCTIONS
################################################################################

log_message() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" | tee -a "$LOG_FILE"
}

create_directories() {
    log_message "Creating required directories"
    mkdir -p "$LOG_DIR" "$RESULTS_DIR"
    
    # Manage .gitignore
    if [[ ! -f .gitignore ]]; then
        log_message "Creating .gitignore file"
        cat > .gitignore << 'EOF'
# Section added automatically by ollama-batch-download.sh
/logs
/results
EOF
    else
        if ! grep -q "^/logs$" .gitignore; then
            echo -e "\n# Section added automatically by ollama-batch-download.sh\n/logs" >> .gitignore
            log_message "Added /logs to .gitignore"
        fi
        if ! grep -q "^/results$" .gitignore; then
            echo "/results" >> .gitignore
            log_message "Added /results to .gitignore"
        fi
    fi
}

show_help() {
    cat << 'EOF'
OLLAMA BATCH DOWNLOAD SCRIPT - HELP
====================================

Usage: ./ollama-batch-download.sh [OPTIONS]

OPTIONS:
  -h,  --help          Display this help message
  -exe, --exec         Execute the download process
  -pr,  --prerequis    Check prerequisites
  -i,   --install      Install missing prerequisites
  -s,   --simulate     Run in simulation mode (dry-run)
  -ch,  --changelog    Display changelog

EXAMPLES:
  # Check prerequisites
  ./ollama-batch-download.sh --prerequis

  # Install missing prerequisites
  ./ollama-batch-download.sh --install

  # Simulate download (no actual downloads)
  ./ollama-batch-download.sh --simulate

  # Execute actual download
  ./ollama-batch-download.sh --exec

  # Combine simulation with prerequisite check
  ./ollama-batch-download.sh --prerequis --simulate

DESCRIPTION:
  This script downloads multiple Ollama models optimized for a 50GB storage limit.
  It includes models from Mistral, Llama, CodeLlama, Gemma, Qwen, DeepSeek, Phi3, and others.

STORAGE MANAGEMENT:
  - Total storage limit: 50GB
  - Automatic calculation of total model sizes
  - Warning if total exceeds limit
  - Individual model size estimation before download

MODELS INCLUDED:
  - mistral:latest (4.1GB) - General purpose French/English
  - mistral:7b (4.1GB) - Mistral 7B base
  - llama3.2:latest (2.0GB) - Latest Llama 3.2
  - llama3.2:3b (2.0GB) - Compact Llama 3.2
  - codellama:7b (3.8GB) - Code generation
  - gemma2:2b (1.6GB) - Compact efficient model
  - qwen2.5:3b (1.9GB) - Qwen latest compact
  - deepseek-r1:7b (4.4GB) - DeepSeek reasoning
  - deepseek-r1:8b (4.7GB) - DeepSeek reasoning 8B
  - phi3:mini (2.3GB) - Microsoft Phi-3 mini
  - phi3:medium (7.9GB) - Microsoft Phi-3 medium
  - orca-mini:3b (1.9GB) - Compact conversational
  - neural-chat:7b (4.1GB) - Optimized chat
  - starling-lm:7b (4.1GB) - High quality chat
  - solar:10.7b (6.1GB) - Advanced reasoning

EOF
}

show_changelog() {
    cat << 'EOF'
CHANGELOG - OLLAMA BATCH DOWNLOAD SCRIPT
=========================================

Version V1.0 - 2025-02-05
-------------------------
Initial Release:
  - Batch download functionality for 15 curated models
  - Storage limit verification (50GB default)
  - Prerequisite checking (ollama command)
  - Automatic installation option
  - Dry-run simulation mode
  - Detailed progress logging
  - Model size estimation and tracking
  - .gitignore automatic management
  - Comprehensive help and examples
  - Support for Mistral, Llama, DeepSeek, Phi3, and other popular models

EOF
}

check_prerequisites() {
    log_message "Checking prerequisites"
    local missing=0
    
    # Check if ollama is installed
    if ! command -v ollama &> /dev/null; then
        log_message "ERROR: ollama command not found"
        echo "Ollama is not installed. Please install it first."
        echo "Visit: https://ollama.ai/download"
        missing=1
    else
        log_message "SUCCESS: ollama is installed ($(ollama --version 2>&1 | head -n1))"
    fi
    
    # Check if ollama service is running
    if ! pgrep -x "ollama" > /dev/null; then
        log_message "WARNING: ollama service may not be running"
        echo "Consider starting ollama service: ollama serve"
    else
        log_message "SUCCESS: ollama service is running"
    fi
    
    return $missing
}

install_prerequisites() {
    log_message "Installing prerequisites"
    echo "Ollama installation must be done manually."
    echo "Please visit: https://ollama.ai/download"
    echo ""
    echo "For Linux:"
    echo "  curl -fsSL https://ollama.ai/install.sh | sh"
    echo ""
    echo "After installation, start the service:"
    echo "  ollama serve"
}

calculate_total_size() {
    local total=0
    for size in "${MODELS[@]}"; do
        total=$(echo "$total + $size" | bc)
    done
    echo "$total"
}

download_models() {
    log_message "Starting model download process"
    
    local total_size=$(calculate_total_size)
    log_message "Total estimated size: ${total_size}GB (Limit: ${STORAGE_LIMIT_GB}GB)"
    
    if (( $(echo "$total_size > $STORAGE_LIMIT_GB" | bc -l) )); then
        log_message "WARNING: Total size exceeds storage limit!"
        echo "WARNING: Estimated total size (${total_size}GB) exceeds limit (${STORAGE_LIMIT_GB}GB)"
        echo "Some models may not download. Continue? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            log_message "Download cancelled by user"
            return 1
        fi
    fi
    
    echo "" > "$MODELS_LIST"
    local downloaded=0
    local failed=0
    local skipped=0
    
    for model in "${!MODELS[@]}"; do
        local size=${MODELS[$model]}
        
        if [[ "$SIMULATE" == true ]]; then
            log_message "[SIMULATE] Would download: $model (${size}GB)"
            echo "$model (${size}GB) - SIMULATED" >> "$MODELS_LIST"
            ((downloaded++))
        else
            log_message "Downloading: $model (${size}GB)"
            
            if ollama pull "$model" 2>&1 | tee -a "$LOG_FILE"; then
                log_message "SUCCESS: $model downloaded"
                echo "$model (${size}GB) - SUCCESS" >> "$MODELS_LIST"
                ((downloaded++))
            else
                log_message "ERROR: Failed to download $model"
                echo "$model (${size}GB) - FAILED" >> "$MODELS_LIST"
                ((failed++))
            fi
        fi
    done
    
    log_message "Download summary: $downloaded downloaded, $failed failed, $skipped skipped"
    
    echo ""
    echo "==================================================================="
    echo "DOWNLOAD SUMMARY"
    echo "==================================================================="
    echo "Total models processed: ${#MODELS[@]}"
    echo "Successfully downloaded: $downloaded"
    echo "Failed: $failed"
    echo "Skipped: $skipped"
    echo ""
    echo "Detailed results saved to: $MODELS_LIST"
    echo "Full log saved to: $LOG_FILE"
    echo "==================================================================="
}

################################################################################
# MAIN EXECUTION
################################################################################

# Create directories and initialize
create_directories

# Parse arguments
if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

# Process arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -ch|--changelog)
            show_changelog
            exit 0
            ;;
        -pr|--prerequis)
            check_prerequisites
            exit $?
            ;;
        -i|--install)
            install_prerequisites
            exit 0
            ;;
        -s|--simulate)
            SIMULATE=true
            log_message "Simulation mode enabled"
            shift
            ;;
        -exe|--exec)
            if ! check_prerequisites; then
                echo "Prerequisites not met. Run with --install to install."
                exit 1
            fi
            download_models
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
    shift
done
