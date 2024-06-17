# Qualys QSC Hands-on Training

Qualys QSC Hands-on Training is a `tool` that allows `administrators/trainers` to `provision accounts in a Qualys subscription`.

With these accounts provisioned, many customer accounts can be created and distributed in a short period of time, allowing the trainers to focus on the class and content rather than the setup behind the scenes.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Install all requirements from `requirements.txt` in the Installing section
- Supported Operating Systems:
  - Debian 11/12
  - Ubuntu 20.04/22.04 LTS
  - Zorin OS 16+
- Supported Python3 versions:
  - Python 3.8.10+

## Installing

To install `Qualys QSC Hands-on Training`, follow these steps:

- Install all required libraries using the `requirements.txt` file and `pip3`:
`pip3 install -r requirements.txt`

- Create the credentials yaml file that is necessary:
Create a file in the same directory as `main.py` called `.creds.yaml`
Fill in the yaml file as:
```
credentials:
  username: someuser
  password: somepassword
  host: qualysapi.qg4.apps.qualys.com
```

You may want to update the base_url to match where your Qualys instance is

## Configuration

- mailmerge_server.conf: Please add at least one SMTP server configuration in this file for the `mailmerge` utility to work properly. There are examples for all types of SMTP servers present in the file and commented out, simply pick the example that best matches the SMTP server you are going to use.

- mailmerge_template.txt: Please configure this template to match the email format you would like the `mailmerge` utility to send.

## Using

There are two switches that are necessary to know:
1. `-c/--create`: This will taken the given CSV file and create a user for each record in the CSV
2. `-r/--reset-password`: This will ask for a set of usernames (or a single username) and reset the password of that user

NOTE: Please ensure that each email address is on a separate line, one email address per line!

To use `Qualys QSC Hands-on Training`, follow these steps:

- To test your credentials, run the program like this:
`python3 main.py --test --credentials /path/to/credentials.yaml`

This will show you if your credentials are valid or need updating.

- To create users, run the program like this:
`python3 main.py --create /path/to/users.csv --credentials /path/to/credentials.yaml`

- To create and tag users, run the program like this:
`python3 main.py --create-and-tag /path/to/users.csv --credentials /path/to/credentials.yaml`

- To reset a user's password, you can do something like this:
`python3 main.py --reset-password quays1234 quays2345 quays3456 --credentials /path/to/credentials.yaml`

## Contributing to Qualys QSC

To contribute to `Qualys QSC Hands-on Training`, follow these steps:

1. Fork this repository
2. Create a branch: `git checkout -b <branch_name>`
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the Pull Request

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

- [@benowe1717](https://github.com/benowe1717)

## Contact

For help or support on this repository, follow these steps:

- Fill out an issue [here](https://github.com/benowe1717/qualys-qsc/issues).

## License

This project uses the following license: [GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## Sources

- https://github.com/scottydocs/README-template.md/blob/master/README.md
- https://choosealicense.com/
- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/
