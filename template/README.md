## Github Actions workshop

Hopefully this guide and the links provided will teach you about Github Actions. If you already have experience with Github Actions then go to [task 1](#task-1).

### What are Github Actions

Best descibed in the [github documentation](https://docs.github.com/en/actions/getting-started-with-github-actions/overview)

> GitHub Actions help you automate your software development workflows in the same place you store code and collaborate on pull requests and issues. You can write individual tasks, called actions, and combine them to create a custom workflow. Workflows are custom automated processes that you can set up in your repository to build, test, package, release, or deploy any code project on GitHub.


Essentailly we can think of this as doing the same job as teamcity (for some of our repos), just with a nicer interface and coupled with our code so it's much easier to see everything in one place.

### When would we use Github Actions over teamcity

The main use case of Github Actions within our organisation right now is for deploying NuGet packages, and running tests. Theoretically we could deploy internal serivces through GitHub Actions by [hosting our own runner](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) but more research needs to be done into this as there could be potential [security concerns](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners#self-hosted-runner-security-with-public-repositories) with public repos.

### How do you set up a Github Workflow

A workflow encomposes one or more actions or tasks. A workflow is a single file stored in `.github/workflows` folder within your repository. You can name the file anything. It must be in `yml` format. You can have multiple workflows for a single repository. See the [github documentation](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions) for a full guide on workflow syntax.

You can create a workflow file using your favorite editor or go to the `Actions` tab within your github repository and press `set up a workflow yourself` this should give you a template for a workflow file that you can edit. Whichever way you choose you can then push these changes to a new branch on your repository.

Here is an example of a script that would buld a dotnet project and run the tests for that project
```yml
name: Test
on:
  push:
    branches:
        - develop 
jobs:
  publish:
    name: build, pack & publish
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup dotnet
        uses: actions/setup-dotnet@v1
        with:
            dotnet-version: '3.1.x'

      - run: dotnet build
      - run: dotnet test
```

You may have noticed the `uses` keyword. This is one of the many reasons Github Actions is so great - you can use other organizations/peoples actions. Github provide a `Verified Creator` tag for different actions so you know you can trust them. Take a look at the [github marketplace](https://github.com/marketplace?type=actions) for available actions.

The two actions used above do the following:
-  `actions/checkout@v2` : This action checks-out your repository under $GITHUB_WORKSPACE [(default environment variable)](https://docs.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables), so your workflow can access it.
-  `actions/setup-dotnet@v1` : This action sets up a dotnet core cli environment for use in actions by:
    - optionally downloading and caching a version of dotnet by SDK version and adding to PATH
    - registering problem matchers for error output
    - setting up authentication to private package sources like GitHub Packages

Becuase we have setup the dotnet cli we can then perform commands like `dotnet build`, `dotnet test`, and `dotnet nuget push...`. 

Do you feel like you could create a workflow file now?
- No, read through the following:
    - [GitHub documentation](https://docs.github.com/en/actions)
    - [Quickstart guide](https://dev.to/rickedb/quickstart-with-github-actions-42pi)
    - [Pimp your repo guide](http://www.michalbialecki.com/2020/01/30/pimp-your-repo-with-github-actions/)
    - [Example of deploying NuGet package](https://lukelowrey.com/use-github-actions-to-publish-nuget-packages/)
- Yes, [go to task 1](#task-1)

## Task 1

Your task is too create one or more workflow files that do the following:
- when a pull request to `develop` branch is performed a NuGet package is published with the version `W.X.Y-prerealse-Z`. Where `W` is the major version, `X` is the minor version, `Y` is the patch, and `Z` prerealse number.
- when a pull request to `master` branch is performed a NuGet package is published with the version `W.X.Y`. Where `W` is the major version, `X` is the minor version, and `Y` is the patch.

Once you have deployed your NuGet package and you can see it on on NuGet.org go to [task 2](#task-2).

### Guide

The creation of a workflow file can be broke into the following steps:
1. First clone your repo and checkout to a new branch called `workflows`, by default your repo should have a `master` and `develop` branch already (if my script has worked correctly😅). However, the repo will not have any rules applied to these branches so you can directly push to them - but don't. I want to encourage you to use pull request - not only here but when writing code for any of our projects.
2. The folder for adding workflow files should already exist. Go to this folder `.github/workflow`. Create a new file called `publish-prerelease.yml`. This workflow is going to publish a prerelease version of the NuGet package. 
3. Add the following to the `publish-prerelease.yml` file. See the [documentation links](#how-do-you-set-up-a-github-workflow) for more information.
    1. `name: x` - the name of the workflow, this will be show in the actions tab when running the workflow.
    2. `on: x` - this is what will trigger the workflow to run, e.g pull-request or push on `develop` branch.
    3. `jobs: x` - jobs that we will execute in this workflow, see example below.
        ```yml
        jobs:
            publish: # you can choose the naming of this, it will contain all the requried actions to do this specifc job - you can have multiple jobs if you want.
                name: # naming the job - this appears in the job that runs
                runs-on: # target machine to run the job on e.g [ubuntu-latest][windows-latest][macos-latest] - for this task we can use just use ubuntu-latest
                steps: # this contians all the steps to the job - e.g. any `uses`, `runs`
        ```
4. You now need to add the following tasks to your list of steps:
    1. The checkout action
    2. The dotnet cli setup action
    3. Build the dotnet project
    4. Test the dotnet project - SKIP this, I never added tests to the project, feel free to add your own and add this step 
    5. Pack the project with the Release configuration and with the following `--version-suffix prerelease-$GITHUB_RUN_NUMBER` this appends the run number to the version. There is many ways of accomplishing this but this is probably the simplest.
    6. Publish the package to nuget.org - **WARNING: DO NOT PUBLISH THE PACAKGE TO STOCKPORTS NUGET ACCOUNT** - A test NuGet account has been made, this has a new api key you can use - ask for the key. (This is so the test NuGet account can be deleted after this COP and all your packages deleted with them)
5. Add, and Commit to your branch
6. The folder for adding workflow files should already exist. Go to this folder `.github/workflow`. Create a new file called `publish.yml`. This workflow is going to publish a prerelease version of the NuGet package. 
7. Add the following to the `publish.yml` file. See the [documentation links](#how-do-you-set-up-a-github-workflow) for more information.
    1. `name: x` - the name of the workflow, this will be show in the actions tab when running the workflow.
    2. `on: x` - this is what will trigger the workflow to run, e.g pull-request or push on `master` branch.
    3. `jobs: x` - jobs that we will execute in this workflow, see example below.
        ```yml
        jobs:
            publish: # you can choose the naming of this, it will contain all the requried actions to do this specifc job - you can have multiple jobs if you want.
                name: # naming the job - this appears in the job that runs
                runs-on: # target machine to run the job on e.g [ubuntu-latest][windows-latest][macos-latest] - for this task we can use just use ubuntu-latest
                steps: # this contians all the steps to the job - e.g. any `uses`, `runs`
        ```
8. You now need to add the following tasks to your list of steps:
    1. The checkout action
    2. The dotnet cli setup action
    3. Build the dotnet project
    4. Test the dotnet project - SKIP this, I never added tests to the project, feel free to add your own and add this step 
    5. Pack the project with the Release configuration.
    6. Publish the package to nuget.org - **WARNING: DO NOT PUBLISH THE PACAKGE TO STOCKPORTS NUGET ACCOUNT** - A test NuGet account has been made, this has a new api key you can use - ask for the key. (This is so the test NuGet account can be deleted after this COP and all your packages deleted with them)
9. Add, and Commit to your branch
10. Ensure the .csproj is correct for deploying a NuGet packge. The following details are requried:
    ```xml
	<Authors>YOUR NAME</Authors>
	<PackageDescription>Testing the github actions!</PackageDescription>

    <!-- this is the version of the package, if you deploy a prerelease the version in this case would be 1.0.0-prerelease-1 -->
	<VersionPrefix>1.0.0</VersionPrefix>

    <!-- unquie ID for the pacakge -->
    <PackageId>template</PackageId>

    <!-- the demo organization -->
	<Company>COPGithubActionsDemoOrganization</Company>
    ```
11. Add, and Commit any changes to the .csproj.
12. Push your commits to the `workflow` branch you previously created.
13. Create a pull-request from `workflow` to `develop`. When the pull-request is accepted you should be able go to the *Actions* tab on your repo and watch the Github Action run.
14. If the previous step was sunccessful and your package was deployed then do a pull-request from `develop` to `master`. Again go to the *Actions* tab and watch the Github Action run.

Now you have finsihed task 1 go to [task 2](#task-2).
  

## Task 2

Your task is too create one or more workflow files that do the same as [task 1](#task-1) following - but this time you can use the organisation templates.

You have to use the GitHub interface for this step. 

Github Action Organisation Templates are created by members of the organisation and stored in the `.github` repo. The workflows are stored within `/workflow-templates` folder and must contain a `[workflow-name].properties.json` and a `[workflow-name].yml`.

`[workflow-name].properties.json` format:
```jsonc
{
  "name": "Deploy really great package", // name of the action template
  "description": "A real great package for deploying something great", // description
  "iconName": "smbc-icon", // svg icon stored in same directory
  "categories": ["C#"] // optional
}
```

`[workflow-name].yml` format (just a normal workflow file that can be changed per usage):
```yml
name: Publish
on:
  push:
    branches:
      - master # Default release branch
jobs:
  publish:
    name: build, pack & publish
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup dotnet
        uses: actions/setup-dotnet@v1
        with:
          dotnet-version: '3.1.x'

      # Build
      - name: Build project
        run: dotnet build

      # Test
      - name: Test project
        run: dotnet test
        
      # Pack
      - name: Package project
        run: dotnet pack --configuration Release

      # Publish
      - name: Publish project
        run: dotnet nuget push src/bin/Release/*.nupkg -k ${{ secrets.NUGET_API_KEY }} -s https://nuget.org
```

### Guide

The creation of a workflow file can be broke into the following steps:
1. Remove the workflow files created in *task 1*. Push removal to develop and master.
2. Go to your github repo in a browser.
3. Go to the *Actions* tab.
4. Navigate to the "Workflows created by COPGithubActionsDemoOrganization"
5. Press the "Set up this workflow" button for the `PRERELEASE-TEMPLATE`
6. Edit the template as required. Then commit it to a new branch.
7. Repeat step 5 & 6 for `RELEASE-TEMPLATE`. Commit to same branch.
8. Do a pull request from your new branch to `develop`
8. If successfuly deployed, do a pull request from `develop` to `master`

Now you have finsihed task 2 go to [bonus task](#bonus-task).

## Bonus Task

So far we have looked at deploying packages to the NuGet.org registry using Github Actions. GitHub have there own package registry called, you guessed it, **Github Package Registry**. We are going to look at using this instead of NuGet Registry.

**BUT WHY SHOULD WE USE THIS?**

> Your packages, at home with their code

Simply put, speed. Github Registry is a modern package registry, and similarly to npm it deploys packages instantly. It also couples up the registry, code, and pipeline in one place making one source of truth for the developer.

The following section will outline the key changes you would need to make to your workflow files to have a package deploy to github registry, and any setup you must do on your computer to consume that package.

1. Firstly we need to add additional parameters to the `actions/setup-dotnet@v1`, we essential need to add the github nuget registry to the nuget sources when setting up the dotnet cli. We also need to provide the access token which is setup by default by github. See below:
    ```yml
    - uses: actions/setup-dotnet@v1
      with:
        dotnet-version: '3.1.x'
        source-url: https://nuget.pkg.github.com/COPGithubActionsDemoOrganization/index.json
      env:
        NUGET_AUTH_TOKEN: ${{secrets.GITHUB_TOKEN}}
    ```
2. Remove the `-s https://nuget.org` from your `dotnet nuget push` command. See below:
    ```yml
    - run: dotnet nuget push "bin/Release/*.nupkg"
    ```
3. Add the following to your .csproj
    ```xml
    <RepositoryUrl>https://github.com/COPGithubActionsDemoOrganization/[your_package_name]</RepositoryUrl>
    ```
4. Add, Commit, and Push to a branch.
5. Do a pull-request from `your-feature-branch` to `develop` to `master`
6. If you go to your repo "home page", on the right hand side there is a `Packages` side bar, you should now be able to see your package.

That should be all the changes you need to make to deploy the package to Github Package Registry. But how do you consume this package. The steps todo so are outlined below.

1. Navigate to your users NuGet.config - `%AppData%/Nuget/NuGet.Config`
2. Add the following source. Replacing `[your-github-username]` with your github username, and `[your-github-access-token]` with your generated github access token. To generate a access token go to `Settings > Developer settings > Personal access tokens > Generate new token`.
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <configuration>
      <packageSources>
        <add key="nuget.org" value="https://api.nuget.org/v3/index.json"    protocolVersion="3" />
        <add key="github" value="https://nuget.pkg.github.com/COPGithubActionsDemoOrganization/index.json" />
      </packageSources>
      <packageSourceCredentials>
        <github>
            <add key="Username" value="[your-github-username]" />
            <add key="ClearTextPassword" value="[your-github-access-token]" />
          </github>
      </packageSourceCredentials>
    </configuration>
    ```
3. You should be ready to use your package. Create a new project, open Nuget Package Manager, and see if any packages apear for your new source.