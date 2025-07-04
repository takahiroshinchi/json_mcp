# server.py
import asyncio
import sys
import json
import os
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP

# Create an MCP server with debug enabled
mcp = FastMCP("grapes-component-server", debug=True)

# Load the Grapes.js project data
def load_grapes_data() -> Dict[str, Any]:
    """Load design_3.json file"""
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, "design_3.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {json_path} not found", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return {}

# Recursive component search function
def find_component_by_id(components: List[Dict], target_id: str) -> Optional[Dict]:
    """Recursively search for a component by its ID"""
    for component in components:
        # Check if this component has the target ID
        if component.get('attributes', {}).get('id') == target_id:
            return component
        
        # Recursively search in nested components
        if 'components' in component:
            result = find_component_by_id(component['components'], target_id)
            if result:
                return result
    
    return None

def find_components_by_type(components: List[Dict], target_type: str) -> List[Dict]:
    """Recursively search for components by their type"""
    results = []
    
    for component in components:
        # Check if this component matches the target type
        if component.get('type') == target_type:
            results.append(component)
        
        # Recursively search in nested components
        if 'components' in component:
            results.extend(find_components_by_type(component['components'], target_type))
    
    return results

def find_components_by_class(components: List[Dict], target_class: str) -> List[Dict]:
    """Recursively search for components by their CSS class"""
    results = []
    
    for component in components:
        # Check if this component has the target class
        if target_class in component.get('classes', []):
            results.append(component)
        
        # Recursively search in nested components
        if 'components' in component:
            results.extend(find_components_by_class(component['components'], target_class))
    
    return results

@mcp.tool()
def get_component_by_id(component_id: str) -> Dict[str, Any]:
    """Get a specific component by its ID from the Grapes.js project
    
    Args:
        component_id: The ID of the component to retrieve
        
    Returns:
        The component data or an error message
    """
    data = load_grapes_data()
    
    if not data:
        return {"error": "Failed to load Grapes.js project data"}
    
    # Search in pages
    if 'pages' in data:
        for page in data['pages']:
            if 'frames' in page:
                for frame in page['frames']:
                    if 'component' in frame:
                        # Search in the main component
                        if frame['component'].get('attributes', {}).get('id') == component_id:
                            return frame['component']
                        
                        # Search in nested components
                        if 'components' in frame['component']:
                            result = find_component_by_id(frame['component']['components'], component_id)
                            if result:
                                return result
    
    return {"error": f"Component with ID '{component_id}' not found"}

@mcp.tool()
def get_components_by_type(component_type: str) -> Dict[str, Any]:
    """Get all components of a specific type from the Grapes.js project
    
    Args:
        component_type: The type of components to retrieve (e.g., 'section', 'heading', 'text')
        
    Returns:
        List of components matching the type or an error message
    """
    data = load_grapes_data()
    
    if not data:
        return {"error": "Failed to load Grapes.js project data"}
    
    results = []
    
    # Search in pages
    if 'pages' in data:
        for page in data['pages']:
            if 'frames' in page:
                for frame in page['frames']:
                    if 'component' in frame:
                        # Check main component
                        if frame['component'].get('type') == component_type:
                            results.append(frame['component'])
                        
                        # Search in nested components
                        if 'components' in frame['component']:
                            results.extend(find_components_by_type(frame['component']['components'], component_type))
    
    return {
        "type": component_type,
        "count": len(results),
        "components": results
    }

@mcp.tool()
def get_components_by_class(css_class: str) -> Dict[str, Any]:
    """Get all components with a specific CSS class from the Grapes.js project
    
    Args:
        css_class: The CSS class to search for (e.g., '_section', '_heading', '_text')
        
    Returns:
        List of components with the specified class or an error message
    """
    data = load_grapes_data()
    
    if not data:
        return {"error": "Failed to load Grapes.js project data"}
    
    results = []
    
    # Search in pages
    if 'pages' in data:
        for page in data['pages']:
            if 'frames' in page:
                for frame in page['frames']:
                    if 'component' in frame:
                        # Check main component
                        if css_class in frame['component'].get('classes', []):
                            results.append(frame['component'])
                        
                        # Search in nested components
                        if 'components' in frame['component']:
                            results.extend(find_components_by_class(frame['component']['components'], css_class))
    
    return {
        "class": css_class,
        "count": len(results),
        "components": results
    }

@mcp.tool()
def get_project_structure() -> Dict[str, Any]:
    """Get the overall structure of the Grapes.js project
    
    Returns:
        Overview of the project structure including styles count, pages count, etc.
    """
    data = load_grapes_data()
    
    if not data:
        return {"error": "Failed to load Grapes.js project data"}
    
    structure = {
        "styles_count": len(data.get('styles', [])),
        "pages_count": len(data.get('pages', [])),
        "total_components": 0,
        "component_types": {},
        "available_ids": [],
        "available_classes": set()
    }
    
    # Analyze components
    if 'pages' in data:
        for page in data['pages']:
            if 'frames' in page:
                for frame in page['frames']:
                    if 'component' in frame:
                        def analyze_component(comp):
                            structure["total_components"] += 1
                            
                            # Count component types
                            comp_type = comp.get('type', 'unknown')
                            structure["component_types"][comp_type] = structure["component_types"].get(comp_type, 0) + 1
                            
                            # Collect IDs
                            comp_id = comp.get('attributes', {}).get('id')
                            if comp_id:
                                structure["available_ids"].append(comp_id)
                            
                            # Collect classes
                            classes = comp.get('classes', [])
                            structure["available_classes"].update(classes)
                            
                            # Recursively analyze nested components
                            if 'components' in comp:
                                for nested_comp in comp['components']:
                                    analyze_component(nested_comp)
                        
                        analyze_component(frame['component'])
    
    # Convert set to list for JSON serialization
    structure["available_classes"] = list(structure["available_classes"])
    
    return structure

@mcp.tool()
def get_styles_for_selector(selector: str) -> Dict[str, Any]:
    """Get CSS styles for a specific selector from the Grapes.js project
    
    Args:
        selector: The CSS selector to search for (e.g., '#i3y3', '.section')
        
    Returns:
        The style rules for the selector or an error message
    """
    data = load_grapes_data()
    
    if not data:
        return {"error": "Failed to load Grapes.js project data"}
    
    if 'styles' not in data:
        return {"error": "No styles found in project data"}
    
    for style_rule in data['styles']:
        if selector in style_rule.get('selectors', []):
            return {
                "selector": selector,
                "style": style_rule.get('style', {})
            }
    
    return {"error": f"No styles found for selector '{selector}'"}

# Add this part to run the server
if __name__ == "__main__":
    try:
        # stdioトランスポートを使用
        print("Starting Grapes.js Component MCP server in stdio mode", file=sys.stderr)
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)