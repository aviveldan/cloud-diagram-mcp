# Interactive HTML Visualization Demo

This document demonstrates the interactive features of the Terraform plan visualization HTML page.

## Overview

The interactive HTML page (`terraform-diffs/terraform_plan_interactive.html`) provides a browser-based interface for exploring Terraform plan changes. No special tools or server required - just open in any modern web browser.

## Layout

The page consists of three main sections:

### 1. Header Section
- **Title**: "🏗️ Terraform Plan Visualization"
- **Instructions**: "Click on any resource in the diagram to view its configuration and changes"
- **Gradient background**: Purple to pink gradient for visual appeal

### 2. Main Diagram (Left Panel)
- **Interactive SVG**: The full architecture diagram with all resources
- **Hover effects**: Resource names change color on hover
- **Click handlers**: Each resource is clickable
- **Connections**: Gray dashed arrows showing dependencies between resources
- **Color-coded clusters**: Resources grouped by action type

### 3. Details Sidebar (Right Panel)
- **Placeholder state**: Shows "👆 Click on a resource in the diagram to view its details" by default
- **Resource details**: Displays when a resource is clicked
- **Legend**: Color-coded legend showing action types

## Interactive Features

### When You Click a Resource

#### For CREATE Actions (New Resources)
**Example: Clicking on "web_az2" instance**

The sidebar shows:
```
[Green Border Card]
✨ web_az2
aws_instance

CREATING

New Configuration:
- ami: "ami-0c55b159cbfafe1f0"
- instance_type: "t3.small"
- subnet_id: "subnet-private-az2"
- tags:
  - Name: "web-server-az2"
  - Tier: "web"
  - Version: "2.0"
```

#### For UPDATE Actions (Modified Resources)
**Example: Clicking on "primary" database**

The sidebar shows:
```
[Orange Border Card]
📝 primary
aws_db_instance

UPDATING

Changes:
- engine_version
  - "13.7"
  + "14.5"

- multi_az
  - false
  + true
```

#### For DELETE Actions (Resources Being Removed)
**Example: If there was a resource being deleted**

The sidebar shows:
```
[Red Border Card]
🗑️ legacy
aws_db_instance

DELETING

Resource will be destroyed
```

#### For REPLACE Actions (Create + Delete)
**Example: Clicking on "www" Route53 record**

The sidebar shows:
```
[Purple Border Card]
🔄 www
aws_route53_record

REPLACING

Changes:
- alias.name
  - "old-alb.amazonaws.com"
  + "production-cdn.cloudfront.net"
```

## Visual Features

### Color Coding
- **Green**: Create actions (#C8E6C9 background, #2E7D32 text)
- **Orange**: Update actions (#FFF9C4 background, #F57F17 text)
- **Red**: Delete actions (#FFCDD2 background, #C62828 text)
- **Purple**: Replace actions (#E1BEE7 background, #6A1B9A text)

### Typography
- **Resource names**: Large, bold, 18px
- **Resource types**: Monospace font, 14px, gray
- **Change details**: Courier New for configuration values
- **Before values**: Red with strikethrough
- **After values**: Green highlighting

### Interactivity
- **Hover**: Resource names turn purple (#764ba2) on hover
- **Click**: Resource names are blue (#667eea) indicating they're clickable
- **Smooth transitions**: CSS transitions for all interactive elements

## Benefits

1. **No Installation Required**: Works in any modern web browser
2. **Offline**: Fully functional without internet connection
3. **Detailed View**: See exact configuration changes, not just summaries
4. **Easy Navigation**: Click to explore, visual feedback on hover
5. **Professional UI**: Clean, modern design with proper spacing and colors
6. **Accessible**: Clear labels, good contrast, keyboard-navigable

## Use Cases

- **Review Changes**: Click through resources to understand what will change
- **Present to Team**: Share the HTML file for infrastructure review meetings
- **Documentation**: Archive plan visualizations for audit purposes
- **Learning**: Understand Terraform's plan structure and resource dependencies
- **Debugging**: Identify unexpected changes before applying

## Technical Details

- **Pure HTML/CSS/JavaScript**: No frameworks required
- **Embedded SVG**: Diagram is fully embedded in the HTML
- **Responsive Design**: Works on different screen sizes
- **JSON Data**: Resource configurations embedded as JavaScript objects
- **Event Handlers**: Click events attached to SVG text elements
- **File Size**: ~200-300KB depending on plan complexity
