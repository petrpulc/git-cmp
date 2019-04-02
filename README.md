# git-cmp
Simple git repository comparison tool based on pygit2 (written in Python).

Enables to compare two repositories on selected level:
 - *References* - checks if repositories contain the same references, no matter where they are pointing to
 - *Commits* - checks if repository commit structure is the same, no matter on the contents of individual commits
 - *Trees* - checks if each corresponding commit has same file structure inside, but does not care about contents of these files
 - *Blobs* - behaves like a regular diff, also compares contents of the files
 
## Reason
This application is developed for automated checks of Git repository structure against a given one. Originally for BI-GIT course on Faculty of Information Technology, Czech Technical University in Prague, Czech Republic.

## Usage
```
./gitcmp.py <original_repository> <new_repository>
```

Couple switches are supported:
 - `--level` (`-l`) selects the level of comparison: *ref*, *commit*, *tree*, *blob*
 - `--pedantic` (`-p`) forces a mutual check (new must not contain anything in excess)
 - `--author` (`-a`) also check name and email of the commit author (level must be greater than ref)
 - `-v` print a lot more information (spoilers)
