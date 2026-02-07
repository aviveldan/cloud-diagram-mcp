# Cloud Diff MCP

A Model Context Protocol (MCP) server for analyzing Terraform plans and visualizing infrastructure changes with Mermaid diagrams.

## Screenshot

```mermaid
graph TD
  subgraph aws_vpc["aws_vpc"]
    node0["✨ main"]
  end
  subgraph aws_subnet["aws_subnet"]
    node1["✨ public"]
  end
  subgraph aws_instance["aws_instance"]
    node2["✨ web"]
  end
  subgraph aws_security_group["aws_security_group"]
    node3["📝 web"]
  end
  subgraph aws_db_instance["aws_db_instance"]
    node4["🗑️ legacy"]
  end
  subgraph aws_s3_bucket["aws_s3_bucket"]
    node5["🔄 data"]
  end
  node0 --> node1
  node1 --> node2
  node3 --> node2
  node0 --> node3
  style node0 fill:#90EE90,stroke:#2E7D32,stroke-width:2px
  style node1 fill:#90EE90,stroke:#2E7D32,stroke-width:2px
  style node2 fill:#90EE90,stroke:#2E7D32,stroke-width:2px
  style node4 fill:#FFB6C1,stroke:#C62828,stroke-width:2px,stroke-dasharray: 5 5
  style node3 fill:#FFEB3B,stroke:#F57F17,stroke-width:2px
  style node5 fill:#E1BEE7,stroke:#6A1B9A,stroke-width:4px
```

**Legend:**
- 🟢 Green = Create
- 🟡 Yellow = Update
- 🔴 Red (dashed) = Delete
- 🟣 Purple (thick) = Replace

## Installation

```bash
npm install
npm run build
```

## Usage

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "cloud-diff": {
      "command": "node",
      "args": ["/path/to/cloud-diff-mcp/dist/index.js"]
    }
  }
}
```

## Tools

### `analyze_tf_plan`

Analyzes a Terraform plan JSON and generates a Mermaid diagram.

**Input:**
```json
{
  "plan": "<terraform-plan-json-string>"
}
```

**Output:**
- Change summary with counts
- Color-coded Mermaid diagram showing resources and dependencies

### `execute_tf_apply`

Simulates terraform apply execution (for demonstration).

## License

MIT