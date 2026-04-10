from shop.translations import get_translation

def language_context(request):
    """
    Add language and translation function to all templates
    """
    try:
        language = request.LANGUAGE_CODE or 'bn'
    except:
        language = 'bn'
    
    try:
        return {
            'current_language': language,
            'get_translation': lambda text: get_translation(text, language),
        }
    except Exception as e:
        # Fallback if anything goes wrong
        return {
            'current_language': 'bn',
            'get_translation': lambda text: text,
        }
