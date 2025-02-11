import os
from lxml import etree
from io import StringIO

def mathml2latex_yarosh(equation):
    """ MathML to LaTeX conversion with XSLT from Vasil Yaroshevich """
    script_base_path = os.path.dirname(os.path.realpath(__file__))
    xslt_file = os.path.join(script_base_path, 'mmltex.xsl')
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    
    # If equation is already an Element, use it directly
    if isinstance(equation, etree._Element):
        dom = equation
    else:
        # Otherwise, parse it as a string
        dom = etree.fromstring(equation)
    
    newdom = transform(dom)
    return str(newdom)

def convert_mathml_parts(input_string):
    # Parse the input as HTML to handle mixed content
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(input_string), parser)

    # Find all math elements
    math_elements = tree.xpath('//math')

    results = []
    for math_elem in math_elements:
        # Convert each math element to LaTeX
        latex = mathml2latex_yarosh(math_elem)
        results.append(latex)

    return results

# Your MathML input as a string
mathml_input = '<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle mathsize="18px"><mi>x</mi><mo>=</mo><mi>sin</mi><mi>θ</mi><mrow><mo>|</mo><mi>sin</mi><mi>θ</mi><mo>|</mo></mrow><mi>a</mi><mi>n</mi><mi>d</mi><mtext> </mtext><mi>y</mi><mo>=</mo><mi>cos</mi><mi>θ</mi><mrow><mo>|</mo><mi>cos</mi><mi>θ</mi><mo>|</mo></mrow></mstyle></math> </p><p>and <math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle mathsize="18px"><mfrac><mrow><mn>99</mn><mi>π</mi></mrow><mn>2</mn></mfrac><mo>&lt;</mo><mi>θ</mi><mo>&lt;</mo><mn>50</mn><mi>θ</mi><mo>,</mo></mstyle></math> then (y - x) is equal to</p></td><td><math xmlns="http://www.w3.org/1998/Math/MathML"><mo>−</mo><mn>1</mn></math></td></tr><tr><td>b)</td><td><math xmlns="http://www.w3.org/1998/Math/MathML"><mtable columnalign="left"><mtr><mtd><mfrac><mrow><mi>sin</mi><mrow><mo>(</mo><msup><mn>270</mn><mn>0</mn></msup><mo>+</mo><mi>x</mi><mo>)</mo></mrow><msup><mi>cos</mi><mn>3</mn></msup><mrow><mo>(</mo><msup><mn>720</mn><mn>0</mn></msup><mo>−</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><mi>sin</mi><mrow><mo>(</mo><msup><mn>270</mn><mn>0</mn></msup><mo>−</mo><mi>x</mi><mo>)</mo></mrow><msup><mi>sin</mi><mn>3</mn></msup><mrow><mo>(</mo><msup><mn>540</mn><mn>0</mn></msup><mo>+</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>sin</mi><mrow><mo>(</mo><msup><mn>90</mn><mn>0</mn></msup><mo>+</mo><mi>x</mi><mo>)</mo></mrow><mi>sin</mi><mrow><mo>(</mo><mo>−</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><msup><mi>cos</mi><mn>2</mn></msup><mrow><mo>(</mo><msup><mn>180</mn><mn>0</mn></msup><mo>−</mo><mi>x</mi><mo>)</mo></mrow></mrow></mfrac></mtd></mtr><mtr><mtd><mo>+</mo><mfrac><mrow><mi>cot</mi><mrow><mo>(</mo><msup><mn>270</mn><mn>0</mn></msup><mo>−</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>cos</mi><mi>e</mi><msup><mi>c</mi><mn>2</mn></msup><mrow><mo>(</mo><msup><mn>450</mn><mn>0</mn></msup><mo>+</mo><mi>x</mi><mo>)</mo></mrow></mrow></mfrac><mo>=</mo></mtd></mtr></mtable></math></td><td>0</td></tr><tr><td>c)</td><td><math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle mathsize="18px"><mtable columnalign="left"><mtr><mtd><mi>sin</mi><mrow><mo>(</mo><mo>−</mo><msup><mn>870</mn><mn>0</mn></msup><mo>)</mo></mrow><mo>+</mo><mtext>cosec</mtext><mrow><mo>(</mo><mo>−</mo><msup><mn>660</mn><mn>0</mn></msup><mo>)</mo></mrow><mo>+</mo><mi>tan</mi><mrow><mo>(</mo><mo>−</mo><msup><mn>855</mn><mn>0</mn></msup><mo>)</mo></mrow><mo>+</mo></mtd></mtr><mtr><mtd><mn>2</mn><mi>cot</mi><mrow><mo>(</mo><msup><mn>840</mn><mn>0</mn></msup><mo>)</mo></mrow><mo>+</mo><mi>cos</mi><mrow><mo>(</mo><msup><mn>480</mn><mn>0</mn></msup><mo>)</mo></mrow><mo>+</mo><mi>sec</mi><mrow><mo>(</mo><msup><mn>900</mn><mn>0</mn></msup><mo>)</mo></mrow><mo>=</mo></mtd></mtr></mtable></mstyle></math></td><td><math xmlns="http://www.w3.org/1998/Math/MathML"><mo>−</mo><mn>2</mn></math></td></tr><tr><td>d)</td><td><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>2</mn><mfrac><mrow><msup><mi>cos</mi><mn>3</mn></msup><mrow><mo>(</mo><mfrac><mi>π</mi><mn>2</mn></mfrac><mo>+</mo><mi>x</mi><mo>)</mo></mrow><mi>cot</mi><mrow><mo>(</mo><mn>3</mn><mi>π</mi><mo>+</mo><mi>x</mi><mo>)</mo></mrow><mtext>  </mtext><mi>sec</mi><mrow><mo>(</mo><mi>x</mi><mo>−</mo><mn>3</mn><mi>π</mi><mo>)</mo></mrow><mtext>cosec</mtext><mrow><mo>(</mo><mfrac><mrow><mn>3</mn><mi>π</mi></mrow><mn>2</mn></mfrac><mo>−</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>cot</mi><mi>x</mi><msup><mi>tan</mi><mn>2</mn></msup><mrow><mo>(</mo><mi>x</mi><mo>−</mo><mi>π</mi><mo>)</mo></mrow><mi>sin</mi><mrow><mo>(</mo><mi>x</mi><mo>−</mo><mn>2</mn><mi>π</mi><mo>)</mo></mrow></mrow></mfrac><mo>=</mo></math>'

# Convert MathML to LaTeX
latex_outputs = convert_mathml_parts(mathml_input)

# Print the results
for i, latex in enumerate(latex_outputs, 1):
    print(f"LaTeX output {i}:", latex)