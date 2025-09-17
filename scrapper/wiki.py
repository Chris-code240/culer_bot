import wikipedia
import re
wikipedia.set_lang("en")

links = ["https://en.wikipedia.org/wiki/History_of_FC_Barcelona", "https://en.wikipedia.org/wiki/List_of_FC_Barcelona_records_and_statistics",
         "https://en.wikipedia.org/wiki/FC_Barcelona_Femen%C3%AD", "https://en.wikipedia.org/wiki/FC_Barcelona",
         "https://en.wikipedia.org/wiki/List_of_FC_Barcelona_players","https://en.wikipedia.org/wiki/List_of_FC_Barcelona_Femen%C3%AD_players",
         "https://en.wikipedia.org/wiki/List_of_FC_Barcelona_seasons","https://en.wikipedia.org/wiki/List_of_FC_Barcelona_Femen%C3%AD_seasons",
         ]



# Pages we want
pages = [
    "FC Barcelona",
    "History of FC Barcelona",
    "List of FC Barcelona records and statistics",
    "List of FC Barcelona players"
]
corpus_file = "barca_corpus.txt"

# Sections to drop
drop_sections = ["See also", "References", "External links", "Further reading", "Notes", "Bibliography"]

def clean_content(text):
    """
    Cleans Wikipedia content by removing unwanted sections.
    """
    # Split into sections
    sections = re.split(r"\n==+ .* ==+\n", text)

    cleaned_sections = []
    for section in sections:
        # Skip if section contains drop keywords
        if any(drop.lower() in section.lower() for drop in drop_sections):
            continue
        cleaned_sections.append(section.strip())

    # Remove multiple newlines
    cleaned_text = re.sub(r"\n{2,}", "\n\n", "\n".join(cleaned_sections))
    return cleaned_text.strip()


with open(corpus_file, "w", encoding="utf-8") as f:
    for title in pages:
        try:
            page = wikipedia.page(title, auto_suggest=False)
            content = clean_content(page.content)
            if content:
                f.write(f"### {page.title} ###\n")
                f.write(content + "\n\n")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation for {title}: {e.options}")
        except wikipedia.exceptions.PageError:
            print(f"Page not found: {title}")

print(f"✅ Clean corpus saved to {corpus_file}")