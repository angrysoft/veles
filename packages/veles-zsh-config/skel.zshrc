# Skeleton Zsh configuration file
test -d ~/.shell.d && for f in ~/.shell.d/*.zsh(N); do
  source "$f"
done