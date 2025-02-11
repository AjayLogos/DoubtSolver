import re

#removing html/css tags from the question/option/solution text

def remove_html_css_tag(text):
    html_tag_pattern = r'</?(?!math|mi|mn|mo|mrow|mfrac|msup|msub|msqrt|msubsup)[a-z]*\b[^>]*>|&nbsp;|\n|\r'
    extracted_data = re.sub(html_tag_pattern, '', text)
    return extracted_data


#removes tags from option list
def process_options(options_list):
    if options_list == 'null' or len(options_list)==0:
        return []  # Return empty list if options_list is empty or contains None values
    else:
        processed_options = [remove_html_css_tag(option) for option in options_list]  # Example: Convert options to uppercase
        return processed_options