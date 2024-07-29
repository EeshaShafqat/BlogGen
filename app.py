import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key, openai_api_key
import openai
from streamlit_carousel import carousel


genai.configure(api_key=google_gemini_api_key)

openai.api_key = openai_api_key


single_image = dict(
        title="",
        text="",
        img="",
    )



generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.0-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "title \"Mindful Moments \" and keywords \"health, mind, peace, travelling, books, music, minimalism\".  num_words = 200",
      ],
    },
    {
      "role": "model",
      "parts": [
        "## Mindful Moments: Cultivating Peace in a Fast-Paced World\n\nIn a world consumed by the relentless pursuit of \"more,\" finding moments of true peace can feel like an elusive dream. But what if peace isn't about escaping to a remote mountaintop, but about cultivating mindful moments within the everyday chaos? \n\n**Health** isn't just about our physical well-being, but also the state of our **mind**. When we're constantly bombarded with information and demands, our minds become cluttered, leaving us feeling stressed and depleted.  This is where mindful moments come in.\n\nImagine this: you're **traveling**, exploring a new city. Instead of rushing through a checklist of attractions, you pause, taking a moment to truly savor the aroma of freshly baked bread wafting from a local bakery. That's a mindful moment.\n\nOr, curled up with a captivating **book**, you silence your phone, letting the narrative transport you to another world.  The melody of your favorite **music** washing over you as you close your eyes, letting go of the day's anxieties – another mindful moment. \n\n**Minimalism** plays a key role too.  By simplifying our surroundings and prioritizing experiences over possessions, we create space for mindful moments to flourish. \n\nCultivating peace isn't about achieving a permanent state of zen. It's about incorporating small, intentional practices into our daily lives.  So, put down your phone, take a deep breath, and embrace the peace found in mindful moments. \n",
      ],
    },
  ]
)




st.set_page_config(page_title="BlogGen", layout="wide", initial_sidebar_state="expanded")

st.title('BlogGen: Your personal blog generator')
st.subheader("Create your blogs in no time with BlogGen")



# Sidebar elements
with st.sidebar:
    st.title("Blog Details")
    st.subheader("Enter Details of the Blog you want to generate:")

    blog_title = st.text_input("Blog Title")
    keywords = st.text_area("Keywords (comma separated)")
    num_words = st.slider("Number of words in Blog", min_value=100, max_value=500, step=100)
    

    prompt_parts = [
       f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" and keywords \" {keywords} \". Incorporate prompt into the blog post. Make the the blog post \"{num_words}\" words in length suitable to an online audience. Ensure the content is original, informative and maintains a consistent tone throughout."
    ]

    submit = st.button("Generate My Blog")

    num_images = st.number_input("Number of Images", min_value=1, max_value=3, step=1)

    submit2 = st.button("Generate My Images")

    
    
   

# Main content
if submit:

    response = chat_session.send_message(prompt_parts)
    st.title("Your Blog Post")
    st.write(response.text)

if submit2:

    

    images = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAgu-W1pqHzbnc3rwTxi13ARITgjFIN8oH-m-n6z5defji_Lfo3kslrwpFqgow3EE35sQ&usqp=CAU","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsPZosX64hKwu8chFdT2ojta338pVnpbZvWMHyXMNHER1pOiBh8xqQy0wPXkicItBbzJE&usqp=CAU","https://cdn.britannica.com/84/73184-050-05ED59CB/Sunflower-field-Fargo-North-Dakota.jpg"]
    images_gallery = []

    
   # for i in range(num_images):
   #     image_response = openai.images.generate(
   #     model="dall-e-3",
   #     prompt={blog_title},
   #     size="1024x1024",
   #     quality="standard",
   #     n=1,
   #     )

   #     images.append(image_response.data[0].url)
   #     image_url = image_response.data[0].url


   #     st.image(image_url, caption = "Generated Image(s)")

       

    for i in range(num_images):
        new_image = single_image.copy()
        new_image["title"] = f"Image {i+1}"
        new_image["text"] = blog_title
        new_image["img"] = images[i]
        images_gallery.append(new_image)


    st.title("your blog images: ")
    carousel(items=images_gallery, width=1)


    

