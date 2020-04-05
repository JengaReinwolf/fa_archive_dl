# FA Tor Archive Downloader

## Background

### What

This project downloads content from FurAffinity artists using the unofficial Tor-based FA Archive.

FA Tor Archive: <http://vj5pbopejlhcbz4n.onion/fa/> *(Not accessible except through Tor & Tor proxies)*

### Why

- Most furries are not interested in setting up Tor just to access the Tor FA Archive.
- Tor proxies are hit-or-miss and questionable in terms of privacy and reliability.
  - **NOTE:** This implementation has not been audited for privacy or security, it is simply a means of connectivity without relying on a proxy.

### How

This content utilizes Docker to spin-up a quick connection to the Tor network and programmatically download all content from a single artist.

## Usage

### Building

`docker build -t fa_archive_dl .`

### Running

Replace `<artist>` with the name of the artist you wish to download content from.

`docker run --rm -it -v$(pwd):/srv/fa_archive_dl/cwd/ fa_archive_dl <artist>`

### Permissions

#### Write Permissions

The script expects to be mounted in a directory writable by `everyone`.

You can resolve this by making the directory you intend to run it from world-writable: `chmod 777 <directory>`.

Another fix is to move to run from a directory that is already world-writable like `/tmp`.

Example: `cd /tmp`.

Do bear in mind that `/tmp` is not an acceptable directory for long-term storage as it is lost at reboot.

#### Downloads Permissions

The downloaded files will belong to UID 100.
You may want to take ownership of the files using `chown $USER:$USER -R downloads`

## Extra

### Flags

`--debug : Enables additional output`

### Known Issues

- Does not work with Docker Snap
  - The downloads are written to a volume instead of a mount, making them more cumbersome to access
