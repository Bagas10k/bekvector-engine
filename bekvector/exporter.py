"""
BekVector Exporter — Direct Frontend Component Generation.
Compiles procedural SVG vector code directly into React (.jsx/.tsx) or Vue (.vue) components.
"""

def to_react_component(svg_code: str, component_name: str = "VectorIcon", typescript: bool = False) -> str:
    """Converts SVG markup into a clean, reusable React component."""
    # Convert SVG attributes to camelCase
    jsx = svg_code.replace("stroke-width=", "strokeWidth=")
    jsx = jsx.replace("stroke-linecap=", "strokeLinecap=")
    jsx = jsx.replace("stroke-linejoin=", "strokeLinejoin=")
    jsx = jsx.replace("text-anchor=", "textAnchor=")
    jsx = jsx.replace("font-size=", "fontSize=")
    jsx = jsx.replace("font-family=", "fontFamily=")
    jsx = jsx.replace("letter-spacing=", "letterSpacing=")
    jsx = jsx.replace("stop-color=", "stopColor=")
    jsx = jsx.replace("viewBox=", "viewBox=")

    if typescript:
        header = "import React from 'react';\n\ninterface Props extends React.SVGProps<SVGSVGElement> {\n  className?: string;\n  style?: React.CSSProperties;\n}\n\n"
        sig = f"export const {component_name}: React.FC<Props> = ({{ className = '', style = {{}}, ...props }}) => (\n"
    else:
        header = ""
        sig = f"export const {component_name} = ({{ className = '', style = {{}}, ...props }}) => (\n"

    body = f"  <div className={{`bekvector-wrapper ${{className}}`}} style={{{{ display: 'inline-block', lineHeight: 0, ...style }}}} {{...props}}>\n    {jsx}\n  </div>\n);\n\nexport default {component_name};\n"

    return header + sig + body

def to_vue_component(svg_code: str, component_name: str = "VectorIcon") -> str:
    """Converts SVG markup into a Vue 3 SFC component."""
    return f"""<template>
  <div class="bekvector-wrapper" :class="customClass" :style="customStyle">
    {svg_code}
  </div>
</template>

<script setup>
defineProps({{
  customClass: {{ type: String, default: '' }},
  customStyle: {{ type: Object, default: () => ({{}}) }}
}});
</script>

<style scoped>
.bekvector-wrapper {{
  display: inline-block;
  line-height: 0;
}}
</style>
"""
