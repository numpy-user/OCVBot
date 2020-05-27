import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='ocvbot',
        version='0.1',

        packages=['ocvbot'],

        install_requires=
        [
            'Babel~=2.8.0'
            'Jinja2~=2.11.2',
            'Pillow~=6.2.1',
            'PyYAML~=5.3.1',
            'Pygments~=2.5.2',
            'alabaster~=0.7.12',
            'colorama~=0.4.3',
            'commonmark~=0.9.1',
            'imagesize~=1.2.0',
            'lxml~=4.5.0',
            'numpy~=1.18.3',
            'opencv-python~=4.2.0.34',
            'packaging~=20.3',
            'pyautogui~=0.9.50',
            'pytz~=2020.1',
            'recommonmark~=0.6.0',
            'requests~=2.23.0',
            'snowballstemmer~=2.0.0'
        ],

        extras_requires=
        {
            'all': [
                'Sphinx~=3.0.3',
                'docutils~=0.16',
                   ],
        },

        tests_requires=
        [
            'pytest~=5.4.1',
            'psutil~=5.7.0'
        ],

        #package_data={
            #'': ['*.html'],
        #},

        entry_points=
        {
            'distutils.commands':
                [
                    'ocvbot = ocvbot:main.py',
                ],
        },

        author='Austin Kelley',
        author_email='hxyz@protonmail.com',

        description='The OldSchool Runescape Computer Vision Bot',
        license='GPLv3'
    )

