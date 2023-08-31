# Qualys QSC Hands-on Training

Qualys QSC Hands-on Training is a `tool` that allows `administrators/trainers` to `provision accounts in a Qualys subscription`.

With these accounts provisioned, many customer accounts can be created and distributed in a short period of time, allowing the trainers to focus on the class and content rather than the setup behind the scenes.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- If any dependencies need to be installed ahead of time, list them here and include links to them
- List all supported Operating Systems
- Link to any external documentation that covers prerequisite information

## Installing

To install `Qualys QSC Hands-on Training`, follow these steps:

- Install all required libraries using the `requirements.txt` file and `pip3`:
`pip3 install requirements.txt`

- Create the credentials yaml file that is necessary:
Create a file in the same directory as `main.py` called `.creds.yaml`
Fill in the yaml file as:
credentials:
  username: ""
  password: ""

api:
  base_url: "qualysapi.qg4.apps.qualys.com/api"

You may want to update the base_url to match where your Qualys instance is

## Using

To use `Qualys QSC Hands-on Training`, follow these steps:

- To test your credentials, run the program like this:
`python3 main.py --test`

This will show you if your credentials are valid or need updating.

- To create users, run the program like this:
`python3 main.py --file /some/path/to/your/file.csv`

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

- Link to the Issues tab for this repo
- Link to the Asana form for this work

## License

This project uses the following license: [qualys_license].

## Sources

- https://github.com/scottydocs/README-template.md/blob/master/README.md
- https://choosealicense.com/
- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/