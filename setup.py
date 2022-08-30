from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'youtube_dl',
    'pathlib',
    'pandas'
]

setup(
    name='SpotifByDate',
    version='1.0',
    description='An application that gets your liked songs and albums released on a specific date',
    author='Matías Piña',
    author_email='mlpina@uc.cl',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)