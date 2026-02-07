# Integration Guide

This guide shows how to integrate the Cloud Diff MCP server with MCP clients.

## Claude Desktop Integration

1. **Locate your Claude Desktop config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the server configuration:**

```json
{
  "mcpServers": {
    "cloud-diff": {
      "command": "node",
      "args": ["/absolute/path/to/cloud-diff-mcp/dist/index.js"]
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Use the server:**

In Claude, you can now ask questions like:
- "Analyze this Terraform plan: [paste JSON]"
- "What are the risks in this infrastructure change?"
- "Show me a diagram of these Terraform changes"

## Other MCP Clients

The server uses the standard MCP protocol and can be integrated with any MCP-compatible client.

### Connection Details

- **Transport:** stdio (standard input/output)
- **Protocol Version:** 2024-11-05
- **Capabilities:** tools

### Available Tools

#### 1. analyze_tf_plan

**Description:** Analyze a Terraform plan JSON and generate a visual Mermaid diagram with risk summary

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "plan": {
      "type": "string",
      "description": "Terraform plan JSON as a string"
    }
  },
  "required": ["plan"]
}
```

**Example Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "analyze_tf_plan",
    "arguments": {
      "plan": "{\"format_version\":\"1.2\",\"terraform_version\":\"1.6.0\",\"resource_changes\":[...]}"
    }
  }
}
```

**Example Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "# Terraform Plan Analysis\n\n## Change Summary\n\n- ✨ Create: 3\n- 📝 Update: 1\n..."
      }
    ]
  }
}
```

#### 2. execute_tf_apply

**Description:** Execute terraform apply command (simulated for safety)

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "planId": {
      "type": "string",
      "description": "Optional plan ID for tracking"
    },
    "autoApprove": {
      "type": "boolean",
      "description": "Auto-approve the apply",
      "default": false
    }
  }
}
```

**Example Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "execute_tf_apply",
    "arguments": {
      "planId": "plan-001",
      "autoApprove": false
    }
  }
}
```

## Programmatic Usage

You can also use the server programmatically:

```javascript
import { spawn } from 'child_process';

// Start the server
const server = spawn('node', ['dist/index.js'], {
  stdio: ['pipe', 'pipe', 'pipe']
});

// Send requests via stdin
server.stdin.write(JSON.stringify({
  jsonrpc: '2.0',
  id: 1,
  method: 'tools/call',
  params: {
    name: 'analyze_tf_plan',
    arguments: {
      plan: tfPlanJson
    }
  }
}) + '\n');

// Read responses from stdout
server.stdout.on('data', (data) => {
  const response = JSON.parse(data.toString());
  console.log(response);
});
```

## Generating Terraform Plan JSON

To generate a Terraform plan in JSON format:

```bash
# Generate a plan file
terraform plan -out=tfplan

# Convert to JSON
terraform show -json tfplan > plan.json
```

Then use the contents of `plan.json` with the `analyze_tf_plan` tool.

## Security Considerations

⚠️ **Important Security Notes:**

1. **Simulated Apply**: The `execute_tf_apply` tool is currently a simulation and does not execute actual Terraform commands. This is a safety feature.

2. **Production Deployment**: For production use, implement:
   - Authentication and authorization
   - Approval workflows
   - State locking mechanisms
   - Rollback capabilities
   - Comprehensive audit logging
   - Network isolation
   - Secret management

3. **Plan Validation**: Always validate Terraform plans before analysis:
   - Check for unauthorized changes
   - Verify resource configurations
   - Review security group rules
   - Confirm IAM policy changes

4. **Sensitive Data**: Terraform plans may contain sensitive information:
   - Credentials
   - API keys
   - Private IP addresses
   - Internal infrastructure details
   
   Ensure proper data handling and access controls.

## Troubleshooting

### Server Not Starting

Check that:
- Node.js version is 18 or higher
- Dependencies are installed: `npm install`
- Code is built: `npm run build`
- Path in configuration is absolute

### No Response from Server

Verify:
- JSON-RPC request format is correct
- Server stderr shows "Cloud Diff MCP Server running on stdio"
- Client is using stdio transport
- Requests end with newline character

### Invalid Plan Error

Ensure:
- Plan is valid JSON
- Plan follows Terraform JSON format
- Plan is generated with `terraform show -json`

## Support

For issues, feature requests, or contributions:
- GitHub: https://github.com/aviveldan/cloud-diff-mcp
- Create an issue with details about your setup and the problem
