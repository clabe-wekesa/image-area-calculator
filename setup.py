import setuptools

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setuptools.setup(
    name="image_area_calculator",  # Update the name to reflect your package
    version="0.1.0",
    description="A package to calculate real-world areas of contours in images using a image of known length for scaling.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Clabe Wekesa",  # Replace with your name
    author_email="simiyu86wekesa@gmail.com",  # Replace with your email
    url="https://github.com/clabe-wekesa/image-area-calculator",  # Replace with your GitHub URL
    keywords=['image processing', 'contours', 'area calculation', 'opencv'],
    install_requires=[
        'Click',
        'opencv-python',
        'numpy',
        'pdf2image',
    ],
    python_requires='>=3.6',
    packages=['image_area_calculator'],  # The name of the directory containing your script
    package_dir={'image_area_calculator': 'image_area_calculator'},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'calculate-areas = image_area_calculator.image_area_calculator:calculate_real_world_areas',
        ],
    },
    scripts=[],
)

