import requests
import os
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import zipfile

weburl = "https://cimiterium.cz/hrbitovy/detail/2087-krompach"
baseimageurl = "https://cimiterium.cz"
imageclass = "gallery"
imageurl = "href" # for example href or src

imageurls = []
soup = BeautifulSoup(requests.get(weburl).content, 'html.parser')
gallery_links = soup.find_all("a", class_=webclass)
for link in gallery_links:
    href = link.get(imageurl)
    if href:
        imageurls.append(baseimageurl+href)
        print(href)

directory = 'download'
if not os.path.exists(directory):
    os.makedirs(directory)

for url in tqdm(imageurls, desc='Downloading files', unit='file'):
    filename = url.split('/')[-1]
    file_path = os.path.join(directory, filename)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
    else:
        print(f"Failed to download {filename}")
print("All files downloaded successfully!")
zipinput = input("Do you want to zip these images: ")
if zipinput == "y" or zipinput == "yes":
    folder_path = 'download'
    zip_filename = 'downloaded_files.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, file)

    print(f"All files in '{folder_path}' have been zipped to '{zip_filename}'.")
