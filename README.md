# prjkt

`prjkt` is a [prm](https://github.com/EivindArvesen/prm) like utility but built in python. This is mainly a learning project for me, but if you find it usefull, please feel free to use it. If you hit a bug or have a feature request, please open an issue. I am not a developer by trade, so I am sure there are many things that could be done better.

## TLDR

`prjkt` is a utility to help manage multiple projects. It allows you to define a project based on a github repo and then invokes start and stop actions for interacting with the project.

## Prjkt commands

These are the planned commands for the `prjkt` utility.

### define

Use the `prjkt define` command to define/create a new ==project==. This will create a new directory/files in the appropriate **prjkt** path. 

```shell
prjkt define PROJECT_NAME --template GITHUBUSER/REPO [OPTIONS]
```
