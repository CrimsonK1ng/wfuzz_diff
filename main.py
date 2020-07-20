#! /usr/bin/env python

import wfuzz
import selenium
import sys
import os
from bs4 import BeautifulSoup as Soup
import argparse
import requests
from nlp import *
from screenshot import *
from images import *

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.critical("ASDASD")
"""
This program is just a deep inspection tool for wfuzz.

Start function
    - enable deep inspection
        - Run NLP comparison on each url content returned
        - Run screenshot comparison on each url returnedk

1. Run wfuzz as normal
2. Parse each response for either
    a. Only NLP
        * Find statistically significant results of url data returned
    b. Only images
        * Take screenshots of all pages and then compare each image to find significant differences
    c. Both NLP -> Images
3. Present data to user in nice fashion

"""

def parse():
    """Parse input. Allow deep inspection of return values. 

    Returns:
        Dict - values
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("method", choices=["none", "nlp", "img", "both"], default="none")
    parser.add_argument("--baseline", dest="baseline", type=str, default=None)
    parser.add_argument("wfuzz", type=str, nargs=argparse.REMAINDER)

    return parser.parse_args()

def get_baseline(url):
    """Baseline request that we will compare all others too

    Args:
        url (str): url you would like to base comparison on  

    Returns:
        str: content of web page 
    """
    res = requests.get(url).content
    return  Soup(res, features="html.parser").text

def run_wfuzz(wfuzz_opts):
    """Execute the wfuzz function (with standard output) and gather the results for later

    Args:
        wfuzz_opts (Dict): Input to the wfuzz application
    
    Returns:
        results (Dict): Dict of dictionary responses containing urls, code, content
    """
    results = dict()
    ind = 0
    with wfuzz.FuzzSession(**wfuzz_options) as wf:
        for r in wf.fuzz():
            data = dict()
            print(r)
            data["code"] = r.code
            data["url"] = r.url
            data["content"] = Soup(r.content, features="html.parser").text
            results[ind] = data
            ind += 1

    return results

def run_nlp(docs, threshold=0.5):
    """Get all indices where threshold value is met (meaning files are significantly different)

    Args:
        docs (List): List of documents (Content of Urls)
        threshold (Int): Value {0,1} where you want files to be less than (different = 0, similar=1)

    Returns:
        List: List of indices where document meets criteria
    """
    tokenized  = get_tokens(docs)
    dictionary = get_dictionary(tokenized)
    corpus     = get_corpus(dictionary, tokenized)
    model      = get_model(corpus)
    index      = get_sim(model, corpus)
    results    = get_comp_to_base(index, model, corpus)
    results    = results[1:]
    index_results = list()
    for ind, res in enumerate(results):
        if res < threshold:
            index_results.append(ind)
    
    return index_results


if __name__ == "__main__":
    """Main function to start off the program
    """
    args = parse()
    # Run wfuzz
    logger.info(f"Baseline set to: tada")
    wfuzz_options = wfuzz.ui.console.clparser.CLParser(["wfuzz"] + args.wfuzz).parse_cl()
    wfuzz_res = run_wfuzz(wfuzz_options)

    baseline = args.baseline
    if not baseline:
        base_url = wfuzz_options["url"].replace("FUZZ", '')

    print(logger.level)
    logger.debug(f"base url set to: {base_url}")

    base_data = get_baseline(base_url)

    logger.info(f"Base data set to: {base_data}")
    
    print()
    if args.method == "nlp":
        docs =  [base_data] + [v["content"] for _, v in wfuzz_res.items()] 
        print(len(docs))
        significant_index = run_nlp(docs)
        print(significant_index)
        for i in significant_index:
            print(wfuzz_res[i].get("url"))

    if args.method == "img":
        all_urls = [base_url] + [v["url"] for _, v in wfuzz_res.items()]
        build_list(all_urls)
        run_container()

        base_img = None
        domain = base_url.replace("https://", "")
        domain = domain.replace("http://", "")
        domain = domain.replace("com/", "com.png")
        print(domain)
        for root, _, files in os.walk(os.path.join(os.getcwd(), "screenshots")):
            for _file in files:
                filepath = os.path.join(root, _file)
                if os.path.splitext(filepath)[1] == ".png":
                    if domain in _file and base_img is None:
                        print("found")
                        base_img = filepath
                        break

            if base_img is None:
                break

            for _file in files:
                filepath = os.path.join(root, _file)
                if os.path.splitext(filepath)[1] == ".png":
                    if filepath is not base_img:
                        print(base_img)
                        print(filepath)
                        diff(base_img, filepath)



