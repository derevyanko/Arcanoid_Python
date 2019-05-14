from distutils.core import setup

setup(
    name='Arcanoid',
    version='1.0.0',
    description='Simple python game',
    author='Derevyanko Oleg',
    author_email='trekol39042@gmail.com',
    url='https://github.com/derevyanko/project_game',
    requirments=[
        'pygame==1.9.4',
        'math',
    ],
    console=['main.py']
)
