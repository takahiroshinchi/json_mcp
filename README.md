# Grapes.js Component MCP Server

A Model Context Protocol (MCP) server for analyzing and querying Grapes.js project components and styles.

## 📋 Project Overview

This project provides an MCP server that can parse Grapes.js design files and extract component information, enabling AI assistants to understand and work with web component structures and styling information.

## 🗂️ Project Structure

```
gjson/
├── server.py                 # Main MCP server implementation
├── pyproject.toml           # Python project configuration
├── design_2.json            # Grapes.js project data (basic components)
├── design_3.json            # Grapes.js project data (with Swiper carousel)
├── CAROUSEL_ANALYSIS_REPORT.md  # Detailed carousel analysis report
└── README.md                # This file
```

## 🚀 Features

### MCP Tools Available

1. **`get_component_by_id`** - Retrieve a specific component by its ID
2. **`get_components_by_type`** - Get all components of a specific type (e.g., 'section', 'heading', 'text')
3. **`get_components_by_class`** - Get all components with a specific CSS class
4. **`get_project_structure`** - Returns an overview of the entire project structure
5. **`get_styles_for_selector`** - Get CSS styles for a specific selector

### Supported Component Types

- **Layout**: `wrapper`, `section`, `row`, `cell`
- **Content**: `text`, `heading`, `image`, `link`, `button`
- **Interactive**: `swiper-container`, `swiper-slide`, `input`, `form`
- **Navigation**: `navbar`, `menu-item`
- **Media**: `video`, `audio`

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- uv (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gjson
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure VS Code MCP Integration**
   
   Add to your VS Code settings.json:
   ```json
   {
     "mcp": {
       "servers": {
         "grapes-component-server": {
           "type": "stdio",
           "command": "uv",
           "args": [
             "--directory",
             "/path/to/your/gjson",
             "run",
             "server.py"
           ],
           "alwaysAllow": [
             "get_component_by_id",
             "get_components_by_type",
             "get_components_by_class",
             "get_project_structure",
             "get_styles_for_selector"
           ],
           "env": {
             "PYTHONUNBUFFERED": "1"
           }
         }
       }
     }
   }
   ```

## 🔧 Usage

### Running the Server

```bash
# Start the MCP server
uv run server.py
```

### Testing the Server

```bash
# Start the MCP server
uv run server.py
```

### Example API Calls

```python
# Get project structure
get_project_structure()

# Get all text components
get_components_by_type("text")

# Get component by specific ID
get_component_by_id("in43")

# Get styles for a selector
get_styles_for_selector("#i3y3")

# Get components with specific CSS class
get_components_by_class("_section")
```

## 📊 Data Format

### Grapes.js Project Structure

The server processes Grapes.js project files with the following structure:

```json
{
  "pages": [
    {
      "frames": [
        {
          "component": {
            "type": "wrapper",
            "components": [
              {
                "tagName": "section",
                "type": "section",
                "attributes": { "id": "unique-id" },
                "classes": ["css-class"],
                "components": [...]
              }
            ]
          }
        }
      ]
    }
  ],
  "styles": [
    {
      "selectors": ["#unique-id"],
      "style": {
        "padding": "10px",
        "margin": "20px"
      }
    }
  ]
}
```

## 🎠 Carousel (Swiper) Support

The server includes specialized support for Swiper.js carousel components:

- **Container Detection**: Identifies swiper-container components
- **Slide Analysis**: Extracts individual slide content and styling
- **Navigation Elements**: Detects pagination, scrollbar, and navigation buttons
- **Configuration Parsing**: Extracts Swiper settings and options

### Carousel Components Found

In `design_3.json`:
- 1 Swiper container (`ijg0h`)
- 2 image slides with Picsum photos
- Complete navigation set (prev/next, pagination, scrollbar)
- Auto-play and loop configuration

## 🧪 Testing

### Testing Methods

- **Manual Testing**: Direct server interaction via stdin/stdout
- **VS Code Integration**: Test through the MCP extension

### Test Coverage

- ✅ Server initialization and communication
- ✅ Tool registration and listing
- ✅ Component retrieval by ID, type, and class
- ✅ Style rule extraction
- ✅ Project structure analysis
- ✅ Swiper carousel detection and analysis

## 📁 Dependencies

```toml
[project]
dependencies = [
    "mcp",
    "fastmcp"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 🔍 VS Code Integration

This MCP server integrates with VS Code through the MCP extension, enabling:

- **AI Assistant Integration**: Ask questions about component structure
- **Code Analysis**: Analyze Grapes.js projects directly in VS Code
- **Design System Queries**: Query components by type, class, or ID
- **Style Information**: Get CSS styling information for any selector

## 🚀 Development

### Adding New Tools

1. Add new tool function with `@mcp.tool()` decorator
2. Update `alwaysAllow` list in VS Code settings
3. Test through VS Code MCP integration

### Extending Component Analysis

The recursive search functions can be extended to support:
- Custom component types
- Advanced filtering criteria
- Component relationship mapping
- Style inheritance analysis

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For issues and questions:
- Review the MCP protocol documentation
- Examine the Grapes.js project structure in the JSON files
- Test functionality through VS Code MCP integration

## 🔄 Recent Updates

- ✅ Added Swiper carousel component analysis
- ✅ Implemented comprehensive MCP tool set
- ✅ Enhanced VS Code integration
- ✅ Added detailed testing framework
- ✅ Created component analysis reporting