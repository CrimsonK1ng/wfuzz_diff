import docker
import os

OPTIONS = {
    "image" : "leonjza/gowitness",
    "volumes" : {
        f"{os.getcwd()}/screenshots" : {"bind": "/screenshots", "mode": "rw"}
    },
    "auto_remove" : True,
    "command" : "file -s /screenshots/urls.txt"
}

def build_list(urls):
    if not os.path.exists(os.path.join(os.getcwd(), "screenshots")):
        os.mkdir("screenshots")

    if not os.path.exists(os.path.join(os.getcwd(), "screenshots", "urls.txt")):
        print("File exists (urls.txt) gonna overwrite")

    with open(os.path.join(os.getcwd(), "screenshots", "urls.txt"), "w") as f:
        for url in urls:
            f.write(url + "\n")

def run_container():
    client = docker.from_env()
    _ = client.containers.run(**OPTIONS)