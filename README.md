# Code Smell Detector

A GitHub Action that automatically detects code smells in Java code using AI-powered analysis.

## Setup

1. Create a Google Cloud Project and enable the Vertex AI API
2. Create a service account and download the credentials JSON
3. Add the following secrets to your GitHub repository:
   - `GOOGLE_APPLICATION_CREDENTIALS`: The contents of your Google Cloud service account JSON
   - `GITHUB_TOKEN`: Automatically provided by GitHub Actions

## Features

- Full repository analysis (weekly or manual trigger)
- PR-specific analysis (automatic on PR creation/update)
- AI-powered code smell detection
- Automatic issue creation for findings
- PR comments for immediate feedback

## Usage

### For Pull Requests
The action will automatically run on any PR that modifies Java files.

### For Full Repository Analysis
You can:
1. Wait for the weekly scheduled run
2. Manually trigger the workflow from the Actions tab

## Configuration

The action works out of the box with Java files. No additional configuration needed.
