# Stripe Agent Toolkit - TypeScript

The Stripe Agent Toolkit enables popular agent frameworks including LangChain and Vercel's AI SDK to integrate with Stripe APIs through function calling. It also provides tooling to quickly integrate metered billing for prompt and completion token usage.

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package run:

```
npm install @stripe/agent-toolkit
```

### Requirements

- Node 18+

## Usage

The library needs to be configured with your account's secret key which is available in your [Stripe Dashboard][api-keys]. Additionally, `configuration` enables you to specify the types of actions that can be taken using the toolkit.

```typescript
import {StripeAgentToolkit} from '@stripe/agent-toolkit/langchain';

const stripeAgentToolkit = new StripeAgentToolkit({
  secretKey: process.env.STRIPE_SECRET_KEY!,
  configuration: {
    actions: {
      paymentLinks: {
        create: true,
      },
    },
  },
});
```

### Tools

The toolkit works with LangChain and Vercel's AI SDK and can be passed as a list of tools. For example:

```typescript
import {AgentExecutor, createStructuredChatAgent} from 'langchain/agents';

const tools = stripeAgentToolkit.getTools();

const agent = await createStructuredChatAgent({
  llm,
  tools,
  prompt,
});

const agentExecutor = new AgentExecutor({
  agent,
  tools,
});
```

### Metered billing

For Vercel's AI SDK, you can use middleware to submit billing events for usage. All that is required is the customer ID and the input/output meters to bill.

```typescript
import {StripeAgentToolkit} from '@stripe/agent-toolkit/ai-sdk';
import {openai} from '@ai-sdk/openai';
import {
  generateText,
  experimental_wrapLanguageModel as wrapLanguageModel,
} from 'ai';

const stripeAgentToolkit = new StripeAgentToolkit({
  secretKey: process.env.STRIPE_SECRET_KEY!,
  configuration: {
    actions: {
      paymentLinks: {
        create: true,
      },
    },
  },
});

const model = wrapLanguageModel({
  model: openai('gpt-4o'),
  middleware: stripeAgentToolkit.middleware({
    billing: {
      customer: 'cus_123',
      meters: {
        input: 'input_tokens',
        output: 'output_tokens',
      },
    },
  }),
});
```

This works with both `generateText` and `generateStream` from the Vercel AI SDK.

[node-sdk]: https://github.com/stripe/stripe-node
[api-keys]: https://dashboard.stripe.com/account/apikeys