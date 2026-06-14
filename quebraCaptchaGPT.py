import base64

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



import nopecha

#Path to your image
image_path = r"G:\Meu Drive\Teste\teste.png"

#Getting the base64 string
base64_image = encode_image(image_path)

nopecha.api_key = 'REMOVED_FOR_GITHUB'

# Call the Recognition API
text = nopecha.Recognition.solve(
    type='textcaptcha',
    image_data=[base64_image],
)

# Print the text to type
print(text)