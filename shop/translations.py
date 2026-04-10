"""
Custom translation dictionary for English and Bengali
"""

TRANSLATIONS = {
    'en': {
        'Home': 'Home',
        'Service Area': 'Service Area',
        'Orders': 'Orders',
        'My Orders': 'My Orders',
        'Profile': 'Profile',
        'Logout': 'Logout',
        'Cart': 'Cart',
        'Login': 'Login',
        'Register': 'Register',
        'Menu': 'Menu',
        'Admin Panel': 'Admin Panel',
        'Manager Panel': 'Manager Panel',
        'Rider Panel': 'Rider Panel',
    },
    'bn': {
        'Home': 'হোম',
        'Service Area': 'সেবা এলাকা',
        'Orders': 'অর্ডার',
        'My Orders': 'আমার অর্ডার',
        'Profile': 'প্রোফাইল',
        'Logout': 'লগআউট',
        'Cart': 'কার্ট',
        'Login': 'লগইন',
        'Register': 'রেজিস্টার',
        'Menu': 'মেনু',
        'Admin Panel': 'Admin Panel',
        'Manager Panel': 'Manager Panel',
        'Rider Panel': 'Rider Panel',
    }
}

def get_translation(text, language='bn'):
    """Get translated text based on language"""
    if language not in TRANSLATIONS:
        language = 'bn'
    return TRANSLATIONS[language].get(text, text)
