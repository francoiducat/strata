#!/bin/bash

# Colors for output
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
GRAY='\033[0;90m'
RESET='\033[0m'

echo -e "${BOLD}=== Python Installations Audit ===${RESET}\n"

# Function to determine source from path
get_source() {
    local path="$1"
    if [[ "$path" == *"Library/Frameworks/Python.framework"* ]]; then
        echo "python.org"
    elif [[ "$path" == *"/Cellar/python"* ]] || [[ "$path" == *"/opt/homebrew"* ]] || [[ "$path" == *"/usr/local/Cellar"* ]]; then
        echo "Homebrew"
    elif [[ "$path" == "/usr/bin/python3" ]]; then
        echo "macOS System"
    elif [[ "$path" == *".pyenv"* ]]; then
        echo "pyenv"
    elif [[ "$path" == *".asdf"* ]]; then
        echo "asdf"
    else
        echo "Unknown"
    fi
}

# Check default python3
if command -v python3 &> /dev/null; then
    DEFAULT_PATH=$(which python3)
    DEFAULT_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    DEFAULT_REAL=$(python3 -c "import sys; print(sys.executable)" 2>/dev/null)
    # Resolve to actual path if it's a symlink
    if [ -L "$DEFAULT_REAL" ]; then
        DEFAULT_REAL=$(realpath "$DEFAULT_REAL" 2>/dev/null || readlink -f "$DEFAULT_REAL" 2>/dev/null || echo "$DEFAULT_REAL")
    fi
    DEFAULT_SOURCE=$(get_source "$DEFAULT_REAL")

    echo -e "${GREEN}★${RESET} ${BOLD}Default python3${RESET}"
    echo -e "  Version:     ${BLUE}${DEFAULT_VERSION}${RESET}"
    echo -e "  Command:     ${GRAY}${DEFAULT_PATH}${RESET}"

    # Show symlink if it exists
    if [ -L "$DEFAULT_PATH" ]; then
        SYMLINK_TARGET=$(readlink "$DEFAULT_PATH")
        echo -e "  Symlink:     ${GRAY}${DEFAULT_PATH} -> ${SYMLINK_TARGET}${RESET}"
    fi

    echo -e "  Actual path: ${GRAY}${DEFAULT_REAL}${RESET}"
    echo -e "  Source:      ${YELLOW}${DEFAULT_SOURCE}${RESET}"
    echo ""
fi

# Check system Python
if [ -f "/usr/bin/python3" ]; then
    SYSTEM_VERSION=$(/usr/bin/python3 --version 2>&1 | awk '{print $2}')
    echo -e "${BOLD}macOS System Python${RESET}"
    echo -e "  Version:  ${BLUE}${SYSTEM_VERSION}${RESET}"
    echo -e "  Path:     ${GRAY}/usr/bin/python3${RESET}"
    echo ""
fi

# Find all python3.x versions
echo -e "${BOLD}Other Python Installations:${RESET}"
found_others=false

for cmd in python3.11 python3.12 python3.13 python3.10 python3.14; do
    if command -v "$cmd" &> /dev/null; then
        found_others=true
        VERSION=$($cmd --version 2>&1 | awk '{print $2}')
        PATH_LOC=$(which "$cmd")
        REAL_PATH=$($cmd -c "import sys; print(sys.executable)" 2>/dev/null)
        # Resolve to actual path if it's a symlink
        if [ -L "$REAL_PATH" ]; then
            REAL_PATH=$(realpath "$REAL_PATH" 2>/dev/null || readlink -f "$REAL_PATH" 2>/dev/null || echo "$REAL_PATH")
        fi
        SOURCE=$(get_source "$REAL_PATH")

        echo -e "  • ${BOLD}${cmd}${RESET}"
        echo -e "    Version:     ${BLUE}${VERSION}${RESET}"
        echo -e "    Command:     ${GRAY}${PATH_LOC}${RESET}"

        # Show symlink if it exists
        if [ -L "$PATH_LOC" ]; then
            SYMLINK_TARGET=$(readlink "$PATH_LOC")
            echo -e "    Symlink:     ${GRAY}${PATH_LOC} -> ${SYMLINK_TARGET}${RESET}"
        fi

        echo -e "    Actual path: ${GRAY}${REAL_PATH}${RESET}"
        echo -e "    Source:      ${YELLOW}${SOURCE}${RESET}"

        # Check for libexec/bin alternative (Homebrew keg-only versions)
        LIBEXEC_PATH="/opt/homebrew/opt/python@${cmd#python}/libexec/bin/python3"
        if [ -f "$LIBEXEC_PATH" ] && [ "$LIBEXEC_PATH" != "$REAL_PATH" ]; then
            echo -e "    ${GRAY}Note: Unversioned 'python3' also available at:${RESET}"
            echo -e "          ${GRAY}${LIBEXEC_PATH}${RESET}"
        fi
        echo ""
    fi
done

if [ "$found_others" = false ]; then
    echo -e "  ${GRAY}(none found)${RESET}\n"
fi

# Check Homebrew installations
echo -e "${BOLD}Homebrew Python Packages:${RESET}"
if command -v brew &> /dev/null; then
    BREW_PYTHONS=$(brew list 2>/dev/null | grep "^python" || echo "")
    if [ -n "$BREW_PYTHONS" ]; then
        echo "$BREW_PYTHONS" | while read -r pkg; do
            echo -e "  • ${GREEN}${pkg}${RESET}"
        done
    else
        echo -e "  ${GRAY}(none installed)${RESET}"
    fi
else
    echo -e "  ${GRAY}(Homebrew not installed)${RESET}"
fi
echo ""

# Check version managers
echo -e "${BOLD}Version Managers:${RESET}"
managers_found=false

if command -v pyenv &> /dev/null; then
    managers_found=true
    echo -e "  • ${GREEN}pyenv${RESET} installed"
    PYENV_VERSIONS=$(pyenv versions 2>/dev/null | grep -v "system" | sed 's/^[* ]*//' | head -5)
    if [ -n "$PYENV_VERSIONS" ]; then
        echo "$PYENV_VERSIONS" | while read -r ver; do
            echo -e "    - ${BLUE}${ver}${RESET}"
        done
    fi
fi

if command -v asdf &> /dev/null; then
    managers_found=true
    echo -e "  • ${GREEN}asdf${RESET} installed"
    ASDF_PYTHONS=$(asdf list python 2>/dev/null | sed 's/^[* ]*//' | head -5)
    if [ -n "$ASDF_PYTHONS" ]; then
        echo "$ASDF_PYTHONS" | while read -r ver; do
            echo -e "    - ${BLUE}${ver}${RESET}"
        done
    fi
fi

if [ "$managers_found" = false ]; then
    echo -e "  ${GRAY}(none detected)${RESET}"
fi

echo ""
echo -e "${BOLD}Legend:${RESET}"
echo -e "  ${GREEN}★${RESET} = Currently active default"
echo -e "  ${YELLOW}Source${RESET} = Where Python was installed from"
echo -e "  Command = Symlink in PATH directory"
echo -e "  Actual path = Real Python executable location"