# tools

## Installation Instructions

Run the following commands to install required Python packages and create
symbolic links in the local bin directory to the tools contained in this
repository:

```
$ python3 -m pip install --requirement requirements.txt
$ stow --ignore=requirements.txt \
> --target="$HOME/.local/bin" \
> bits \
> colore \
> fzyedit \
> fzyoink \
> git-fzfixup \
> git-quickfix \
> git-rmhooks \
> mkjournals \
> mkmd \
> qfvim \
> vicmd \
> vipe \
> yeet
```
