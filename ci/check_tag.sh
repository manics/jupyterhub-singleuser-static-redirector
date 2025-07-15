#!/usr/bin/bash
# If this is a git tag then check the pyproject.toml version has been updated
set -eu

if [[ "$GITHUB_REF" =~ ^refs/tags/ ]]; then
  GITHUB_TAG="${GITHUB_REF#refs/tags/}"
else
  echo "No tag detected"
  exit 0
fi

PYPROJECT_VERSION=$(grep '^version\s*=' pyproject.toml | sed -re 's|version\s*=\s*"([^"]+)"|\1|')

if [[ "$GITHUB_TAG" != "$PYPROJECT_VERSION" ]]; then
  echo "ERROR: pyproject.toml version '$PYPROJECT_VERSION' does not match GitHub tag: '$GITHUB_TAG'"
  exit 1
fi
