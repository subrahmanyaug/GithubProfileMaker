import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

def add_title(text, size=16, bold=True):
    pdf.set_font("Arial", 'B' if bold else '', size)
    pdf.cell(200, 10, text, ln=True, align='C')

def add_highlight(text, size=12):
    pdf.set_font("Arial", 'B', size)
    pdf.set_text_color(0, 0, 255) 
    pdf.cell(0, 10, text, ln=True)

def add_text(text, size=12):
    pdf.set_font("Arial", '', size)
    pdf.set_text_color(0, 0, 0)  
    pdf.cell(0, 10, text, ln=True)

name = input("Enter GitHub profile name: ")
url = f"https://github.com/{name}"
page = requests.get(url)
htmlContent = page.content
soup = BeautifulSoup(htmlContent, "html.parser")

try:
    full_name = soup.find("span", class_="p-name vcard-fullname d-block overflow-hidden").get_text().strip()

    nick_name = soup.find("span", class_="p-nickname vcard-username d-block").get_text().strip()

    image = soup.find("img", class_="rounded-2 avatar-user")
    pic_url = image['src']
    
    img_response = requests.get(pic_url)
    if img_response.status_code == 200:
        with open("profile_picture.jpg", "wb") as f:
            f.write(img_response.content)
        
        pdf.image("profile_picture.jpg", x=85, y=20, w=50, h=50)

    pdf.ln(80)


    add_title(full_name) 
    add_title(f"({nick_name})", size=14, bold=False)  
    
  
    follow = soup.find_all("span", class_="text-bold color-fg-default")
    followers = follow[0].get_text().strip() if len(follow) > 0 else "N/A"
    following = follow[1].get_text().strip() if len(follow) > 1 else "N/A"

  
    add_highlight("Followers & Following:")
    add_text(f"Followers: {followers}")
    add_text(f"Following: {following}")

    view_prj = soup.find_all("span", class_="repo")
    language_tags = soup.find_all('span', itemprop='programmingLanguage')

    add_highlight("Projects:")
    for project in view_prj:
        add_text(project.text.strip())

    add_highlight("Programming Languages Used:")
    used_languages = []
    for lang in language_tags:
        language = lang.get_text().strip()
        if language not in used_languages:
            used_languages.append(language)
            add_text(language)

    all_count = soup.find_all("span", class_="Counter")
    if len(all_count) >= 3:
        repositories = all_count[0].get_text().strip()
        stars = all_count[1].get_text().strip()
        add_highlight("Repositories & Stars:")
        add_text(f"Repositories: {repositories}")
        add_text(f"Stars: {stars}")
        
except Exception as e:
    add_text(f"Error: {e}")

pdf.output("github_profile.pdf")
