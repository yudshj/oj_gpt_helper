import json
import random
import requests
from lxml import html
from utils.config import OPENJUDGE_COOKIE
from utils.t import SubmissionInfo, ProblemInfo

TEST_SUBMISSION_URL = [
    "http://wjpython.openjudge.cn/2022fallpractice/solution/37280630/",
    "http://wjpython.openjudge.cn/2022fallpractice/solution/37479275/",
    "http://wjpython.openjudge.cn/2022fallpractice/solution/37948350/",
    "http://wjpython.openjudge.cn/2022fallpractice/solution/37951227/",
]
COOKIE = OPENJUDGE_COOKIE

def get_problem_info(problem_url) -> ProblemInfo:
    response = requests.get(problem_url, cookies=COOKIE)
    xpath = html.fromstring(response.text)
    desc = xpath.xpath("/html/body/div[3]/div/div[3]/dl[2]/dd")
    problem_description = desc[0].text_content()
    input_description = desc[1].text_content()
    output_description = desc[2].text_content()
    sample_input_description = desc[3].text_content()
    sample_output_description = desc[4].text_content()

    return ProblemInfo(
        problem_description = problem_description,
        input_description = input_description,
        output_description = output_description,
        sample_input_description = sample_input_description,
        sample_output_description = sample_output_description
    )


def get_code_and_description(submission_url) -> SubmissionInfo:
    response = requests.get(submission_url, cookies=COOKIE)
    xpath = html.fromstring(response.text)

    problem_xpath_selector = "/html/body/div[3]/div/div[4]/div/dl/dd[2]/a"
    problem_url_suffix = xpath.xpath(problem_xpath_selector)[0].attrib['href']
    problem_url = "http://wjpython.openjudge.cn" + problem_url_suffix

    source_code_xpath_selector = "/html/body/div[3]/div/div[3]/pre"
    code = xpath.xpath(source_code_xpath_selector)[0].text_content()

    status_xpath_selector = "/html/body/div[3]/div/div[3]/p/a"
    status = xpath.xpath(status_xpath_selector)[0].text_content()

    username_xpath_selector = "/html/body/div[3]/div/div[4]/div/dl/dd[3]/a"
    username = xpath.xpath(username_xpath_selector)[0].text_content()

    language_xpath_selector = "/html/body/div[3]/div/div[4]/div/dl/dd[6]/a"
    language = xpath.xpath(language_xpath_selector)[0].text_content()

    # 这里不能用soup解析xpath
    return SubmissionInfo(
        source_code = code,
        problem_info = get_problem_info(problem_url),
        status = status,
        username = username,
        language = language
    )

def test():
    url = random.choice(TEST_SUBMISSION_URL)
    o = get_code_and_description(url)
    print(json.dumps(o, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    test()