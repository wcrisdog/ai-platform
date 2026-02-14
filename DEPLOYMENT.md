# Travel Agent Deployment Guide

This guide explains how to deploy the Travel Agent so your family can use it.

## Prerequisites

1.  **Google Cloud Project**: You need a Google Cloud Project with Vertex AI enabled.
2.  **API Key**: Ensure you have a valid `GOOGLE_API_KEY` for Gemini.

## Local Testing

To test the agent locally:

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Set your API key:
    ```bash
    export GOOGLE_API_KEY='your_api_key_here'
    ```
3.  Run the web interface:
    ```bash
    streamlit run app.py
    ```

## Cloud Deployment (for Family Access)

To make this accessible to your family without them needing to install Python, deploy it to **Google Cloud Run**.

### Step 1: Build the Container

Open a terminal in this directory (`ai-platform`) and run:

```bash
# Replace PROJECT_ID with your actual project ID
gcloud builds submit --tag gcr.io/omega-healer-487316-e9/travel-agent .
```

### Step 2: Deploy to Cloud Run

```bash
gcloud run deploy travel-agent \
  --image gcr.io/omega-healer-487316-e9/travel-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=AIzaSyCkt_26_BrHghgGBSt3qgXJBW_eg8UjbPE
```

*Note: `--allow-unauthenticated` makes the URL public. If you want to restrict access to just your family, you can remove this flag and add their Google accounts to the Cloud Run invoker role.*

### Step 3: Share the URL

Once deployed, Google Cloud Run will give you a URL (e.g., `https://travel-agent-xyz.a.run.app`). Share this link with your family!

## Features

*   **Plan Travel**: Ask for flight, hotel, and attraction recommendations.
*   **Booking**: The agent can "book" (simulated) tickets but **only after you confirm**.
*   **Interactive UI**: Simple chat interface tailored for easy use.
