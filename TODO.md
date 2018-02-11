# To-do

## WordPress

- Use hashes of public files if feed check fails https://github.com/philipjohn/exploit-scanner-hashes.
    - Use the official core checksum endpoint to build a list of unique hashes for publicly-accessible files?
    - https://api.wordpress.org/core/checksums/1.0/?version=3.6.1
    - https://github.com/wp-cli/checksum-command/blob/e7e6128e6a5115fea4c3e1e497c7ace2286f358d/src/Checksum_Core_Command.php#L217

- Guess the feed URL if no link tags are found.

## Plugins

- Look for all `/plugins/(.*)` patterns.
- Find more caching plugins and their comment strings.

## Themes

- Make Genesis check non Genesis-specific; look for any parent theme.
- Best guess at the theme by grepping soup for 'themes/(.*)/' if no stylesheet found.


## DNS

- Detect sites using vanity Cloudflare nameservers.
