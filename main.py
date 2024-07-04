import os
import requests
from bs4 import BeautifulSoup

def get_final_url(session, url):
    base_url = url
    response = session.get(base_url, allow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    heading = soup.find('h1', {'id': 'firstHeading'})
    if heading:
        title = heading.text.replace(' ', '_')
        return title
    else:
        raise Exception("Heading not found on the page")

def download_answer_keys(session, year, tenortwelve, aorb):
    currentDir = f"Problems/{year}/{aorb}"
    os.makedirs(currentDir, exist_ok=True)

    url = f"https://artofproblemsolving.com/wiki/index.php/{year}_AIME_{tenortwelve}{aorb}_Answer_Key"
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    li_elements = soup.find_all('li')

    for i, li in enumerate(li_elements[:15], start=1):
        answer = li.get_text().strip()
        os.makedirs(f"{currentDir}/{i}", exist_ok=True)  # Create directory for each problem
        with open(f"{currentDir}/{i}/Answer.txt", "w") as a:
            a.write(answer)

def download_problems(session, year, tenortwelve, aorb):
    download_answer_keys(session, year, tenortwelve, aorb)
    currentDir = f"Problems/{year}/{aorb}"
    os.makedirs(currentDir, exist_ok=True)

    for i in range(15):
        try:
            url = f"https://artofproblemsolving.com/wiki/index.php?title={year}_AIME_{tenortwelve}{aorb}_Problems/Problem_{i+1}"
            title = get_final_url(session, url)
            url = f"https://artofproblemsolving.com/wiki/index.php?title={title}&action=edit&section=1"
            response = session.get(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            textarea = soup.find('textarea', {'id': 'wpTextbox1'})

            if textarea:
                problem = textarea.get_text()
                os.makedirs(f"{currentDir}/{i+1}", exist_ok=True)  # Create directory for each problem
                with open(f"{currentDir}/{i+1}/Problem.txt", "w") as p:
                    p.write(problem)
            else:
                print(f"Problem text area not found for Problem {i+1}")
        except Exception as e:
            print(f"An error occurred while processing Problem {i+1}: {e}")

    for i in range(15):
        try:
            url = f"https://artofproblemsolving.com/wiki/index.php?title={year}_AIME_{tenortwelve}{aorb}_Problems/Problem_{i+1}"
            title = get_final_url(session, url)
            url = f"https://artofproblemsolving.com/wiki/index.php?title={title}&action=edit&section=2"
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            textarea = soup.find('textarea', {'id': 'wpTextbox1'})

            if textarea:
                solution = textarea.get_text()
                with open(f"{currentDir}/{i+1}/Solution.txt", "w") as s:
                    s.write(solution)
            else:
                print(f"Solution text area not found for Problem {i+1}")
        except Exception as e:
            print(f"An error occurred while processing Solution {i+1}: {e}")

def main():
    with requests.Session() as session:
        for year in range(2024, 2025):
            download_problems(session, year, "", "I")
            download_problems(session, year, "", "II")
            print(f"Finished downloading {year} AIME")

if __name__ == "__main__":
    main()
