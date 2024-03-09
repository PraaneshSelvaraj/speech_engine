from setuptools import setup, find_packages

setup(
    name='speech_engine',
    version='0.0.3',
    author='Praanesh',
    author_email='praaneshselvaraj2003@gmail.com',
    description='Python package for synthesizing text into speech',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PraaneshSelvaraj/speech_engine',
    packages=find_packages(),
    keywords=[
        'speech_engine',
        'text2speech',
        'text-to-speech',
        'TTS',
        'speech synthesis',
        'audio generation',
        'natural language processing',
        'language processing',
        'voice synthesis',
        'speech output',
        'speech generation',
        'language synthesis',
        'voice output',
        'audio synthesis',
        'voice generation',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'gtts',
        'playsound',
    ],
)
