for content in response_data.clues:
  content_data = ContentData(clue_text=content["francais"], position=(100,800), font_size=70 , color=(0,0,0), align="center", fonts="./fonts/Sans.ttf",language="fr",clue_number=content["numero"])
  create_template_clues(content_data)
