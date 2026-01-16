# GitHub User Fetcher

Command-line utility built with Python to retrieve GitHub user profile data via the GitHub REST API, featuring token-based authentication, structured logging, and defensive error handling.

## Features

- Fetch GitHub user profile details
- Uses GitHub REST API
- Token-based authentication via environment variables
- Logs requests and errors to file
- Handles common API errors (404, 403, timeouts)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/retiredmonk/Github-User-Fetcher.git
cd Github-User-Fetcher
