# Code execution tool

The code execution tool allows Claude to execute Python code in a secure, sandboxed environment.
Claude can analyze data, create visualizations, perform complex calculations, and process uploaded
files directly within the API conversation.

<Note>
  The code execution tool is currently in beta.

  This feature requires the [beta header](/en/api/beta-headers): `"anthropic-beta": "code-execution-2025-05-22"`
</Note>

## Supported models

The code execution tool is available on:

* Claude Opus 4.1 (`claude-opus-4-1-20250805`)
* Claude Opus 4 (`claude-opus-4-20250514`)
* Claude Sonnet 4 (`claude-sonnet-4-20250514`)
* Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`)
* Claude Haiku 3.5 (`claude-3-5-haiku-latest`)

## Quick start

Here's a simple example that asks Claude to perform a calculation:

<CodeGroup>
  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: code-execution-2025-05-22" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-1-20250805",
          "max_tokens": 4096,
          "messages": [
              {
                  "role": "user",
                  "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
              }
          ],
          "tools": [{
              "type": "code_execution_20250522",
              "name": "code_execution"
          }]
      }'
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-4-1-20250805",
      betas=["code-execution-2025-05-22"],
      max_tokens=4096,
      messages=[{
          "role": "user",
          "content": "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
      }],
      tools=[{
          "type": "code_execution_20250522",
          "name": "code_execution"
      }]
  )

  print(response)
  ```

  ```typescript TypeScript
  import { Anthropic } from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  async function main() {
    const response = await anthropic.beta.messages.create({
      model: "claude-opus-4-1-20250805",
      betas: ["code-execution-2025-05-22"],
      max_tokens: 4096,
      messages: [
        {
          role: "user",
          content: "Calculate the mean and standard deviation of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        }
      ],
      tools: [{
        type: "code_execution_20250522",
        name: "code_execution"
      }]
    });

    console.log(response);
  }

  main().catch(console.error);
  ```
</CodeGroup>

## How code execution works

When you add the code execution tool to your API request:

1. Claude evaluates whether code execution would help answer your question
2. Claude writes and executes Python code in a secure sandbox environment
3. Code execution may occur multiple times throughout a single request
4. Claude provides results with any generated charts, calculations, or analysis

## Tool definition

The code execution tool requires no additional parameters:

```json JSON
{
  "type": "code_execution_20250522",
  "name": "code_execution"
}
```

## Response format

Here's an example response with code execution:

```json
{
  "role": "assistant",
  "container": {
    "id": "container_011CPR5CNjB747bTd36fQLFk",
    "expires_at": "2025-05-23T21:13:31.749448Z"
  },
  "content": [
    {
      "type": "text",
      "text": "I'll calculate the mean and standard deviation for you."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01A2B3C4D5E6F7G8H9I0J1K2",
      "name": "code_execution",
      "input": {
        "code": "import numpy as np\ndata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nmean = np.mean(data)\nstd = np.std(data)\nprint(f\"Mean: {mean}\")\nprint(f\"Standard deviation: {std}\")"
      }
    },
    {
      "type": "code_execution_tool_result",
      "tool_use_id": "srvtoolu_01A2B3C4D5E6F7G8H9I0J1K2",
      "content": {
        "type": "code_execution_result",
        "stdout": "Mean: 5.5\nStandard deviation: 2.8722813232690143\n",
        "stderr": "",
        "return_code": 0
      }
    },
    {
      "type": "text",
      "text": "The mean of the dataset is 5.5 and the standard deviation is approximately 2.87."
    }
  ],
  "id": "msg_01BqK2v4FnRs4xTjgL8EuZxz",
  "model": "claude-opus-4-1-20250805",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 45,
    "output_tokens": 187,
  }
}
```

### Results

Code execution results include:

* `stdout`: Output from print statements and successful execution
* `stderr`: Error messages if code execution fails
* `return_code` (0 for success, non-zero for failure)

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_01ABC123",
  "content": {
    "type": "code_execution_result",
    "stdout": "",
    "stderr": "NameError: name 'undefined_variable' is not defined",
    "return_code": 1
  }
}
```

### Errors

If there is an error using the tool there will be a `code_execution_tool_result_error`

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_01VfmxgZ46TiHbmXgy928hQR",
  "content": {
    "type": "code_execution_tool_result_error",
    "error_code": "unavailable"
  }
}
```

Possible errors include

* `unavailable`: The code execution tool is unavailable
* `code_execution_exceeded`: Execution time exceeded the maximum allowed
* `container_expired`: The container is expired and not available

#### `pause_turn` stop reason

The response may include a `pause_turn` stop reason, which indicates that the API paused a long-running turn. You may
provide the response back as-is in a subsequent request to let Claude continue its turn, or modify the content if you
wish to interrupt the conversation.

## Working with Files in Code Execution

Code execution can analyze files uploaded via the Files API, such as CSV files, Excel files, and other data formats.
This allows Claude to read, process, and generate insights from your data. You can pass multiple files per request.

<Note>
  Using the Files API with Code Execution requires two beta headers: `"anthropic-beta": "code-execution-2025-05-22,files-api-2025-04-14"`
</Note>

### Supported file types

The Python environment is capable of working with but not limited to the following file types

* CSV
* Excel (.xlsx, .xls)
* JSON
* XML
* Images (JPEG, PNG, GIF, WebP)
* Text files (.txt, .md, .py, etc)

### Loading files for code execution

1. **Upload your file** using the [Files API](/en/docs/build-with-claude/files)
2. **Reference the file** in your message using a `container_upload` content block
3. **Include the code execution tool** in your API request

<CodeGroup>
  ```bash Shell
  # First, upload a file
  curl https://api.anthropic.com/v1/files \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: files-api-2025-04-14" \
      --form 'file=@"data.csv"' \

  # Then use the file_id with code execution
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: code-execution-2025-05-22,files-api-2025-04-14" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-1-20250805",
          "max_tokens": 4096,
          "messages": [{
              "role": "user",
              "content": [
                  {"type": "text", "text": "Analyze this CSV data"},
                  {"type": "container_upload", "file_id": "file_abc123"}
              ]
          }],
          "tools": [{
              "type": "code_execution_20250522",
              "name": "code_execution"
          }]
      }'
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  # Upload a file
  file_object = client.beta.files.upload(
      file=open("data.csv", "rb"),
  )

  # Use the file_id with code execution
  response = client.beta.messages.create(
      model="claude-opus-4-1-20250805",
      betas=["code-execution-2025-05-22", "files-api-2025-04-14"],
      max_tokens=4096,
      messages=[{
          "role": "user",
          "content": [
              {"type": "text", "text": "Analyze this CSV data"},
              {"type": "container_upload", "file_id": file_object.id}
          ]
      }],
      tools=[{
          "type": "code_execution_20250522",
          "name": "code_execution"
      }]
  )
  ```

  ```typescript TypeScript
  import { Anthropic } from '@anthropic-ai/sdk';
  import { createReadStream } from 'fs';

  const anthropic = new Anthropic();

  async function main() {
    // Upload a file
    const fileObject = await anthropic.beta.files.create({
      file: createReadStream("data.csv"),
    });

    // Use the file_id with code execution
    const response = await anthropic.beta.messages.create({
      model: "claude-opus-4-1-20250805",
      betas: ["code-execution-2025-05-22", "files-api-2025-04-14"],
      max_tokens: 4096,
      messages: [{
        role: "user",
        content: [
          { type: "text", text: "Analyze this CSV data" },
          { type: "container_upload", file_id: fileObject.id }
        ]
      }],
      tools: [{
        type: "code_execution_20250522",
        name: "code_execution"
      }]
    });

    console.log(response);
  }

  main().catch(console.error);
  ```
</CodeGroup>

### Retrieving files created by code execution

When Claude creates files during code execution (e.g., saving matplotlib plots, generating CSVs), you can retrieve these files using the Files API:

<CodeGroup>
  ```python Python
  from anthropic import Anthropic

  # Initialize the client
  client = Anthropic()

  # Request code execution that creates files
  response = client.beta.messages.create(
      model="claude-opus-4-1-20250805",
      betas=["code-execution-2025-05-22", "files-api-2025-04-14"],
      max_tokens=4096,
      messages=[{
          "role": "user",
          "content": "Create a matplotlib visualization and save it as output.png"
      }],
      tools=[{
          "type": "code_execution_20250522",
          "name": "code_execution"
      }]
  )

  # Extract file IDs from the response
  def extract_file_ids(response):
      file_ids = []
      for item in response.content:
          if item.type == 'code_execution_tool_result':
              content_item = item.content
              if content_item.get('type') == 'code_execution_result':
                  for file in content_item.get('content', []):
                      file_ids.append(file['file_id'])
      return file_ids

  # Download the created files
  for file_id in extract_file_ids(response):
      file_metadata = client.beta.files.retrieve_metadata(file_id)
      file_content = client.beta.files.download(file_id)
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript
  import { Anthropic } from '@anthropic-ai/sdk';
  import { writeFileSync } from 'fs';

  // Initialize the client
  const anthropic = new Anthropic();

  async function main() {
    // Request code execution that creates files
    const response = await anthropic.beta.messages.create({
      model: "claude-opus-4-1-20250805",
      betas: ["code-execution-2025-05-22", "files-api-2025-04-14"],
      max_tokens: 4096,
      messages: [{
        role: "user",
        content: "Create a matplotlib visualization and save it as output.png"
      }],
      tools: [{
        type: "code_execution_20250522",
        name: "code_execution"
      }]
    });

    // Extract file IDs from the response
    function extractFileIds(response: any): string[] {
      const fileIds: string[] = [];
      for (const item of response.content) {
        if (item.type === 'code_execution_tool_result') {
          const contentItem = item.content;
          if (contentItem.type === 'code_execution_result' && contentItem.content) {
            for (const file of contentItem.content) {
              fileIds.push(file.file_id);
            }
          }
        }
      }
      return fileIds;
    }

    // Download the created files
    const fileIds = extractFileIds(response);
    for (const fileId of fileIds) {
      const fileMetadata = await anthropic.beta.files.retrieveMetadata(fileId);
      const fileContent = await anthropic.beta.files.download(fileId);

      // Convert ReadableStream to Buffer and save
      const chunks: Uint8Array[] = [];
      for await (const chunk of fileContent) {
        chunks.push(chunk);
      }
      const buffer = Buffer.concat(chunks);
      writeFileSync(fileMetadata.filename, buffer);
      console.log(`Downloaded: ${fileMetadata.filename}`);
    }
  }

  main().catch(console.error);
  ```
</CodeGroup>

## Containers

The code execution tool runs in a secure, containerized environment designed specifically for Python code execution.

### Runtime environment

* **Python version**: 3.11.12
* **Operating system**: Linux-based container
* **Architecture**: x86\_64 (AMD64)

### Resource limits

* **Memory**: 1GiB RAM
* **Disk space**: 5GiB workspace storage
* **CPU**: 1 CPU

### Networking and security

* **Internet access**: Completely disabled for security
* **External connections**: No outbound network requests permitted
* **Sandbox isolation**: Full isolation from host system and other containers
* **File access**: Limited to workspace directory only
* **Workspace scoping**: Like [Files](/en/docs/build-with-claude/files), containers are scoped to the workspace of the API key
* **Expiration**: Containers expire 1 hour after creation

### Pre-installed libraries

The sandboxed Python environment includes these commonly used libraries:

* **Data Science**: pandas, numpy, scipy, scikit-learn, statsmodels
* **Visualization**: matplotlib
* **File Processing**: pyarrow, openpyxl, xlrd, pillow
* **Math & Computing**: sympy, mpmath
* **Utilities**: tqdm, python-dateutil, pytz, joblib

## Container reuse

You can reuse an existing container across multiple API requests by providing the container ID from a previous response.
This allows you to maintain created files between requests.

### Example

<CodeGroup>
  ```python Python
  import os
  from anthropic import Anthropic

  # Initialize the client
  client = Anthropic(
      api_key=os.getenv("ANTHROPIC_API_KEY")
  )

  # First request: Create a file with a random number
  response1 = client.beta.messages.create(
      model="claude-opus-4-1-20250805",
      betas=["code-execution-2025-05-22"],
      max_tokens=4096,
      messages=[{
          "role": "user",
          "content": "Write a file with a random number and save it to '/tmp/number.txt'"
      }],
      tools=[{
          "type": "code_execution_20250522",
          "name": "code_execution"
      }]
  )

  # Extract the container ID from the first response
  container_id = response1.container.id

  # Second request: Reuse the container to read the file
  response2 = client.beta.messages.create(
      container=container_id,  # Reuse the same container
      model="claude-opus-4-1-20250805",
      betas=["code-execution-2025-05-22"],
      max_tokens=4096,
      messages=[{
          "role": "user",
          "content": "Read the number from '/tmp/number.txt' and calculate its square"
      }],
      tools=[{
          "type": "code_execution_20250522",
          "name": "code_execution"
      }]
  )
  ```

  ```typescript TypeScript
  import { Anthropic } from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  async function main() {
    // First request: Create a file with a random number
    const response1 = await anthropic.beta.messages.create({
      model: "claude-opus-4-1-20250805",
      betas: ["code-execution-2025-05-22"],
      max_tokens: 4096,
      messages: [{
        role: "user",
        content: "Write a file with a random number and save it to '/tmp/number.txt'"
      }],
      tools: [{
        type: "code_execution_20250522",
        name: "code_execution"
      }]
    });

    // Extract the container ID from the first response
    const containerId = response1.container.id;

    // Second request: Reuse the container to read the file
    const response2 = await anthropic.beta.messages.create({
      container: containerId,  // Reuse the same container
      model: "claude-opus-4-1-20250805",
      betas: ["code-execution-2025-05-22"],
      max_tokens: 4096,
      messages: [{
        role: "user",
        content: "Read the number from '/tmp/number.txt' and calculate its square"
      }],
      tools: [{
        type: "code_execution_20250522",
        name: "code_execution"
      }]
    });

    console.log(response2.content);
  }

  main().catch(console.error);
  ```

  ```bash Shell
  # First request: Create a file with a random number
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: code-execution-2025-05-22" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-1-20250805",
          "max_tokens": 4096,
          "messages": [{
              "role": "user",
              "content": "Write a file with a random number and save it to \"/tmp/number.txt\""
          }],
          "tools": [{
              "type": "code_execution_20250522",
              "name": "code_execution"
          }]
      }' > response1.json

  # Extract container ID from the response (using jq)
  CONTAINER_ID=$(jq -r '.container.id' response1.json)

  # Second request: Reuse the container to read the file
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: code-execution-2025-05-22" \
      --header "content-type: application/json" \
      --data '{
          "container": "'$CONTAINER_ID'",
          "model": "claude-opus-4-1-20250805",
          "max_tokens": 4096,
          "messages": [{
              "role": "user",
              "content": "Read the number from \"/tmp/number.txt\" and calculate its square"
          }],
          "tools": [{
              "type": "code_execution_20250522",
              "name": "code_execution"
          }]
      }'
  ```
</CodeGroup>

## Streaming

With streaming enabled, you'll receive code execution events as they occur:

```javascript
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "code_execution"}}

// Code execution streamed
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"code\":\"import pandas as pd\\ndf = pd.read_csv('data.csv')\\nprint(df.head())\"}"}}

// Pause while code executes

// Execution results streamed
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "code_execution_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": {"stdout": "   A  B  C\n0  1  2  3\n1  4  5  6", "stderr": ""}}}
```

## Batch requests

You can include the code execution tool in the [Messages Batches API](/en/docs/build-with-claude/batch-processing). Code execution tool calls through the Messages Batches API are priced the same as those in regular Messages API requests.

## Usage and pricing

The code execution tool usage is tracked separately from token usage. Execution time is a minimum of 5 minutes.
If files are included in the request, execution time is billed even if the tool is not used due to files being preloaded onto the container.

**Pricing**: \$0.05 per session-hour.
