# Cloud Diff MCP Server - PR Screenshots

## 📸 Visual Examples Added to README

The README now includes comprehensive screenshots and visual examples showing the MCP server's output.

### What Was Added

1. **📸 Screenshots Section** (at line 5 of README.md)
   - Immediate visual preview of the tool's capabilities
   - Embedded Mermaid diagram showing color-coded infrastructure changes
   - Complete output example with all three sections

2. **Mermaid Diagram Visualization**
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

3. **Color Legend**
   - 🟢 Green solid = Resources being **created** (✨)
   - 🟡 Yellow solid = Resources being **updated** (📝)
   - 🔴 Red dashed = Resources being **deleted** (🗑️)
   - 🟣 Purple thick = Resources being **replaced** (🔄)
   - → Arrows = Dependency relationships

4. **Complete Output Example**
   - Change Summary showing counts
   - Infrastructure Diagram with visual representation
   - Risk Assessment with risk score, high-risk changes, and recommendations

### Additional Documentation Files

- `screenshots/OUTPUT_EXAMPLES.md` - Comprehensive examples including high-risk scenarios
- `screenshots/README_PREVIEW.md` - Visual preview of README changes
- `screenshots/readme-screenshot.txt` - Text-based visual representation

### Benefits

✅ **Immediate Visual Understanding** - Users see what the tool produces before installation  
✅ **Native GitHub Rendering** - Mermaid diagrams render directly on GitHub  
✅ **Complete Feature Preview** - All output sections displayed with real examples  
✅ **Professional Documentation** - Clear, visual, and easy to understand  

### Files Modified

- `README.md` - Added screenshots section with embedded Mermaid diagram
- `screenshots/OUTPUT_EXAMPLES.md` - Detailed examples and scenarios
- `screenshots/README_PREVIEW.md` - Documentation of changes
- `screenshots/readme-screenshot.txt` - Text-based visual representation

### Commit

Commit `0aa1fe9`: "Add screenshots and visual examples to README and documentation"

---

## How It Looks on GitHub

When viewed on GitHub:
1. The **Mermaid diagram renders as an interactive, color-coded graph**
2. **Green boxes** show resources being created
3. **Yellow boxes** show resources being updated
4. **Red dashed boxes** show resources being deleted
5. **Purple thick-border boxes** show resources being replaced
6. **Arrows** show dependencies between resources

The visual examples make it immediately clear how the MCP server visualizes Terraform infrastructure changes.
