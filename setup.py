from setuptools import setup,find_packages
setup(
        name='sinaweibo',
        version='0.4',
        description='SinaWeibo',
        author='xjouyi@163.com',
        author_email='xjouyi@163.com',
        url='https://github.com/XJouYi/SinaWeibo',
        classifiers=[  # Optional
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Topic :: Software Development :: Build Tools',
                'License :: OSI Approved :: MIT License',

                # Specify the Python versions you support here. In particular, ensure
                # that you indicate whether you support Python 2, Python 3 or both.
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
        ],
        packages=['SinaWeibo'],
        include_package_data=True,
        zip_safe=True,
        install_requires=['requests', 'rsa','beautifulsoup4'],
)