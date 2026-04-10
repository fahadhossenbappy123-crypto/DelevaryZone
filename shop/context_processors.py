from shop.translations import get_translation

def language_context(request):
    """
    Add language and translation function to all templates
    """
    language = request.LANGUAGE_CODE or 'bn'
    
    return {
        'current_language': language,
        'get_translation': lambda text: get_translation(text, language),
    }
