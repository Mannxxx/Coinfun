import base64

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def is_allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

def convert_to_writable(filepath):
    try:
        # This function expects the filepath of the image to be converted
        file = open(filepath,'rb').read()   # Open a file in binary mode
        file = base64.b64encode(file) # We must encode the file to get base64 string
        return file             # use decode() to get a string for chats
    except:
        raise Exception("ConversionToBase64StringFailed!")