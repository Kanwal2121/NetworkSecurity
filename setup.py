from setuptools import find_packages,setup


from typing import List
def get_requirements()->List[str]:
    requirements_list:List[str]=[]
    try:
        with open("requirements.txt","r") as file:
            lines=file.readlines()
            for line in lines:
                req=line.strip()
                if req and req!= "-e .":
                    requirements_list.append(req)
        return requirements_list
                    
    except FileNotFoundError:
        print("requirements.txt  not found")

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Kanwalpreet Singh",
    author_email="singhkanwal2121@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()





)


