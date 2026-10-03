# Shell completion

Thumbforge can complete its commands, subcommands and options when you press `Tab`: `thumbforge ba` becomes `thumbforge batch`, `thumbforge thumb ge` becomes `thumbforge thumb generate`, and `thumbforge --ver` offers `--verbose` and `--version`. It works in bash, zsh, fish and PowerShell (PowerShell 7 and Windows PowerShell 5.1). Values such as video ids are not completed.

The `thumbforge` command must be on your `PATH`; [Getting started](../getting-started.md#install) covers that.

## Install

Run this **inside the shell** you want completion in:

```
thumbforge --install-completion
```

Thumbforge learns which shell you are in from the process that started it, so there is no shell argument: run the command from bash to set up bash, from zsh to set up zsh, and so on. Writing a shell name after it does not select that shell. If you use both PowerShell 7 and Windows PowerShell, run it once in each; they keep separate profiles.

To see what would be installed without changing anything, run `thumbforge --show-completion`. It prints the script for the current shell, ready to copy into your own configuration.

## What each shell gets

### bash

- The script is written to `~/.bash_completions/thumbforge.sh` and a `source` line for it is added to `~/.bashrc`, once, however often you run the command.
- Reload: open a new terminal, or run `source ~/.bashrc`.
- Undo: delete the script and the `source` line from `~/.bashrc`.

### zsh

- The script is written to `~/.zfunc/_thumbforge`. The line `fpath+=~/.zfunc; autoload -Uz compinit; compinit` is added to `~/.zshrc`, and so is `zstyle ':completion:*' menu select` if that file has no `zstyle` line yet.
- Reload: open a new terminal, or run `exec zsh`.
- Undo: delete `~/.zfunc/_thumbforge`. The lines added to `~/.zshrc` are generic; remove them only if nothing else of yours relies on them.

### fish

- The script is written to `~/.config/fish/completions/thumbforge.fish`; nothing else changes.
- Reload: open a new terminal, or run `exec fish`.
- Undo: delete that file.

### PowerShell

- The script is appended to your profile, the file `$PROFILE` names (`echo $PROFILE` prints the path). The command also runs `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` so the profile may load. If you would rather not change the execution policy, run `thumbforge --show-completion` and paste the output into your profile yourself.
- The script binds `Tab` to `MenuComplete`, so completion shows a menu of candidates for every command, not only Thumbforge.
- Running the install again appends a second copy of the script; install once.
- Reload: open a new terminal, or run `. $PROFILE`.
- Undo: delete the block from `$PROFILE`, from `Import-Module PSReadLine` down to the `Register-ArgumentCompleter` line that names `thumbforge`. The execution policy stays as it is.

## Check that it works

In a new terminal, type `thumbforge ba` and press `Tab`: it completes to `batch`.

Thumbforge's completion was tested in bash, PowerShell 7 and Windows PowerShell 5.1. The zsh and fish scripts come from the same generator but have not been run in a live shell yet.
