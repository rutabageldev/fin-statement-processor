#!/bin/bash

set -e  # Exit on error

# -----------------------
# 🧭 Usage Instructions
# -----------------------

usage() {
    echo "Usage: $0 [--venv] [--cache] [--pytest] [--all] [--dry-run] [-h|--help]"
    echo ""
    echo " --venv       Remove .venv directory"
    echo " --cache      Remove __pycache__, .pyc/,pyo files, mypy_cache and .coverage"
    echo " --pytest     Remove .pytest cache directory"
    echo " --all        Run all cleanup setps"
    echo " --dry-run    Show what would be deleted, but don't delete"
    echo " -h, --help   Show this help message"
}
# -----------------------
# 🛠️ Defaults
# -----------------------
CLEAN_VENV=false
CLEAN_CACHE=false
CLEAN_PYTEST=false
DRY_RUN=false

# Prevent running outside a project directory
if [[ "$PWD" == "$HOME" || "$PWD" == "/" ]]; then
  echo "❌ Refusing to run clean.sh in $PWD — unsafe root-level directory."
  exit 1
fi


# --- Colorized Logging ---
log_info()    { echo -e "🔹 $1"; }
log_success() { echo -e "\033[32m✅ $1\033[0m"; }
log_warn()    { echo -e "\033[33m⚠️  $1\033[0m"; }
log_delete()  { echo -e "\033[31m🧹 $1\033[0m"; }
log_dryrun()  { echo -e "🔍 Would delete: $1"; }

# -----------------------
# 🔍 Parse Arguments
# -----------------------
for arg in "$@"; do
    case $arg in
        --venv) CLEAN_VENV=true ;;
        --cache) CLEAN_CACHE=true ;;
        --pytest) CLEAN_PYTEST=true ;;
        --all) CLEAN_VENV=true; CLEAN_CACHE=true; CLEAN_PYTEST=true ;;
        --dry-run) DRY_RUN=true ;;
        -h|--help) usage; exit 0 ;;
        *) echo "❌ Unknown option: $arg"; usage; exit 1 ;;
    esac
done

# -----------------------
# 🧽 Delete Helper
# -----------------------
delete() {
    if [ "$DRY_RUN" = true ]; then
        log_dryrun "$1"
    else
        log_delete "$1"
        rm -rf "$1"
    fi
}

# -----------------------
# 🚫 Clean .venv directory
# -----------------------
# Perform cleanup
if [ "$CLEAN_VENV" = true ]; then
    log_info "Cleaning virtual environment..."
    delete .venv
fi

# -----------------------
# 🚫 Clean Python cache
# -----------------------
if [ "$CLEAN_CACHE" = true ]; then
    log_info "Cleaning python cache files..."

    # __pycache__ directories
    while IFS= read -r -d '' dir; do
        delete "$dir"
    done < <(find . -type d -name "__pycache__" -print0)

    # .pyc and .pyo files
    while IFS= read -r -d '' file; do
        delete "$file"
    done < <(find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -print0)

    # .mypy_cache and .coverage
    delete .mypy_cache
    delete .coverage
fi

# -----------------------
# 🚫 Clean .pytest_cache
# -----------------------
if [ "$CLEAN_PYTEST" = true ]; then
    log_info "Cleaning pytest cache..."
    delete .pytest_cache
fi

log_success "✅ Cleanup complete!"
