# Token-efficient tool use

Claude Sonnet 3.7 is capable of calling tools in a token-efficient manner. Requests save an average of 14% in output tokens, up to 70%, which also reduces latency. Exact token reduction and latency improvements depend on the overall response shape and size.

<Info>
  Token-efficient tool use is a beta feature. Please make sure to evaluate your responses before using it in production.

  Please use [this form](https://forms.gle/iEG7XgmQgzceHgQKA) to provide feedback on the quality of the model responses, the API itself, or the quality of the documentation—we cannot wait to hear from you!
</Info>

<Tip>
  If you choose to experiment with this feature, we recommend using the [Prompt Improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver) in the [Console](https://console.anthropic.com/) to improve your prompt.
</Tip>

<Warning>
  Token-efficient tool use does not currently work with [`disable_parallel_tool_use`](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#disabling-parallel-tool-use).

  Claude 4 models (Opus and Sonnet) do not support this feature. The beta header `token-efficient-tools-2025-02-19` will not break an API request, but it will result in a no-op.
</Warning>

To use this beta feature, simply add the beta header `token-efficient-tools-2025-02-19` to a tool use request. If you are using the SDK, ensure that you are using the beta SDK with `anthropic.beta.messages`.

Here's an example of how to use token-efficient tools with the API:

<CodeGroup>
  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: token-efficient-tools-2025-02-19" \
    -d '{
      "model": "claude-3-7-sonnet-20250219",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": [
              "location"
            ]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Tell me the weather in San Francisco."
        }
      ]
    }' | jq '.usage'
  ```

  ```Python Python
  import anthropic

  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      max_tokens=1024,
      model="claude-3-7-sonnet-20250219",
      tools=[{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": [
            "location"
          ]
        }
      }],
      messages=[{
        "role": "user",
        "content": "Tell me the weather in San Francisco."
      }],
      betas=["token-efficient-tools-2025-02-19"]
  )

  print(response.usage)
  ```

  ```TypeScript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  const message = await anthropic.beta.messages.create({
    model: "claude-3-7-sonnet-20250219",
    max_tokens: 1024,
    tools: [{
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          }
        },
        required: ["location"]
      }
    }],
    messages: [{ 
      role: "user", 
      content: "Tell me the weather in San Francisco." 
    }],
    betas: ["token-efficient-tools-2025-02-19"]
  });

  console.log(message.usage);
  ```

  ```Java Java
  import java.util.List;
  import java.util.Map;

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  import static com.anthropic.models.beta.AnthropicBeta.TOKEN_EFFICIENT_TOOLS_2025_02_19;

  public class TokenEfficientToolsExample {

      public static void main(String[] args) {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          BetaTool.InputSchema schema = BetaTool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                          "location",
                          Map.of(
                                  "type", "string",
                                  "description", "The city and state, e.g. San Francisco, CA"
                          )
                  )))
                  .putAdditionalProperty("required", JsonValue.from(List.of("location")))
                  .build();

          MessageCreateParams params = MessageCreateParams.builder()
                  .model("claude-3-7-sonnet-20250219")
                  .maxTokens(1024)
                  .betas(List.of(TOKEN_EFFICIENT_TOOLS_2025_02_19))
                  .addTool(BetaTool.builder()
                          .name("get_weather")
                          .description("Get the current weather in a given location")
                          .inputSchema(schema)
                          .build())
                  .addUserMessage("Tell me the weather in San Francisco.")
                  .build();

          BetaMessage message = client.beta().messages().create(params);
          System.out.println(message.usage());
      }
  }
  ```
</CodeGroup>

The above request should, on average, use fewer input and output tokens than a normal request. To confirm this, try making the same request but remove `token-efficient-tools-2025-02-19` from the beta headers list.

<Tip>
  To keep the benefits of prompt caching, use the beta header consistently for requests you’d like to cache. If you selectively use it, prompt caching will fail.
</Tip>
